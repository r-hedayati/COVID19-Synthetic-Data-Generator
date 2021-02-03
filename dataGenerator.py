import pandas as pd, numpy as np
import random,requests
#from bs4 import BeautifulSoup
from faker import Faker
from random import randint

# Data frame printing configuration
desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',12)

# Initialize Faker
fake=Faker()
Faker.seed(3210) # it is possible to ignore this if we want to have different dataset after each run

# Define list of symptoms and demographics
names=[]
#birthdate=[]
age=[]
gender=[]
address=[]
COVID_results=[]
n_people=20

# Create gender based on name
def first_name_and_gender():
   g = 'Male' if random.randint(0,1) == 0 else 'Female'
   n = fake.first_name_male() if g=='Male' else fake.first_name_female()
   return {'gender':g,'first_name':n}

# Create required columns data
for n in range(n_people):
    person=first_name_and_gender()
    names.append(person.get('first_name') + ' ' + fake.last_name())
    gender.append(person.get('gender'))
    address.append(fake.address())
#    birthdate.append(fake.date_of_birth())
    age.append(randint(18,100))
    COVID_results.append(fake.boolean(chance_of_getting_true=100)) #we can change this number to our required portion


# Create symptoms based on desired distribution
def symptomsGenerator(share,population):
    testSymptom=[]
    count=0
    shareCount=round(share*population)
    for i in range(0,population):
        if count < shareCount:
            testSymptom.append('yes')
        else:
            testSymptom.append('no')
        count+=1
    random.shuffle(testSymptom)
    return testSymptom,shareCount

# function for creating related data, it gets inputSymptom as a symptoms on which outputSymptoms created
# pop equals to the population of positive cases in inputSymptom
# share defines the transition probability
#positiveCases is the number of whole positive cases for each symptom
def relatedSymptomsGenerator(inputSymptom,outputSymptom, pop, share, positiveCases):
    cnt=0
    countshareCNT=0
    countshare = round(share * pop)
    i=0
    flag=0
    while i>-1:
        if ((positiveCases == countshareCNT) and (cnt == countshare)):
            break
        if (countshare>positiveCases):
            if (positiveCases==countshareCNT):
                break
        if cnt != countshare:
            if inputSymptom[i]=='yes':
                outputSymptom[i]='yes'
                cnt+=1
                countshareCNT+=1
        if countshareCNT != positiveCases:
            if inputSymptom[i]=='no':
                outputSymptom[i]='yes'
                countshareCNT+=1
        if countshareCNT>positiveCases:
            if (inputSymptom[i]=='no'):
                outputSymptom[i]='no'
                countshareCNT-=1
        i+=1
        if i==(n_people-1):
            if(countshareCNT>positiveCases):
                i=0
                flag+=1
        if flag == 2:
            break
    return outputSymptom, countshare

#based on population and their distribuation probability, it outputs the number of positive cases for each symptom
def positiveCasesGenerator(shareList,pop):
    positiveCases=[]
    lengthShare=len(shareList)
    for i in range(0,lengthShare):
        positiveCases.append(round(shareList[i]*pop))
    return positiveCases

# Creating empty list for each symptom
testCough,testFatigue, testBreath, testSoreThroat,testHeadache\
    ,testMylagia,testChills,testNausea,testNasal,testDiarrhea=(['no']*n_people for i in range(10))



# the probability of each symptom based on WHO report
#"0.fever":0.879,"1.cough": 0.677,"2.fatigue":0.381,"3.breath":0.186,"4.sore throat":0.139,
#                    "5.headache":0.136,"6.myalgia":0.148,"7.chills":0.114,"8.nausea":0.05,"9.nasal":0.048,"10.diarrhea":0.037}
positiveCasesShare=[0.879, 0.677, 0.381, 0.186, 0.139, 0.136, 0.148, 0.114, 0.05, 0.048, 0.037]
positiveCasesList=positiveCasesGenerator(positiveCasesShare,n_people)

#creating symptoms which we dont have their transition probability by symptomsGenerator function:

fatigue=symptomsGenerator(positiveCasesShare[2],n_people)
shortBreath=symptomsGenerator(positiveCasesShare[3],n_people)
chills=symptomsGenerator(positiveCasesShare[7],n_people)
nasal=symptomsGenerator(positiveCasesShare[9],n_people)

# creating symptoms which we have their transition probability:
fever=symptomsGenerator(positiveCasesShare[0],n_people)
cough=relatedSymptomsGenerator(fever[0],testCough,18,0.78,positiveCasesList[1])
soreThroat=relatedSymptomsGenerator(cough[0],testSoreThroat,cough[1],0.84,positiveCasesList[4])
headache=relatedSymptomsGenerator(cough[0],testHeadache,cough[1],0.84,positiveCasesList[5])
mylagia=relatedSymptomsGenerator(cough[0],testMylagia,cough[1],0.84,positiveCasesList[6])
nausea=relatedSymptomsGenerator(soreThroat[0],testNausea,soreThroat[1],0.65,positiveCasesList[8])
diarrhea=relatedSymptomsGenerator(nausea[0],testDiarrhea,nausea[1],1,positiveCasesList[10])



# Create a dataframe for better handling in ML models
variables=[names,gender,age,fever[0],cough[0],soreThroat[0],headache[0],mylagia[0],nausea[0],diarrhea[0],fatigue[0],shortBreath[0],chills[0],nasal[0],COVID_results]
df=pd.DataFrame(variables).transpose()
df.columns=["name","gender","Age","fever","cough","sore throat",'headache','mylagia',"nausea","diarrhea","fatigue","short of breath","chills", "nasal","COVID19 Test"]
#print(df.head())
df.to_csv('positiveCases.csv', index=False)


# we can implement the negative test cases like positive ones.
negativeCaseShare=[]
covid_result_negative=['no']*n_people
#lossTasteN=symptomsGenerator(0.647,n_people)
fatigueN=symptomsGenerator(0.298,n_people)
shortBreathN=symptomsGenerator(0.152,n_people)
feverN=symptomsGenerator(0.343,n_people)
coughN=symptomsGenerator(0.567,n_people)
diarrheaN=symptomsGenerator(0.259,n_people)
headacheN=symptomsGenerator(0.178,n_people) #Delirium
#skipped meals
#abdomina pain
#chest pain
