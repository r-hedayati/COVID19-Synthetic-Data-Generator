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
n_people=10

# Create gender based on name
def first_name_and_gender():
   g = 'M' if random.randint(0,1) == 0 else 'F'
   n = fake.first_name_male() if g=='M' else fake.first_name_female()
   return {'gender':g,'first_name':n}

# Create required columns data
for n in range(n_people):
    person=first_name_and_gender()
    names.append(person.get('first_name') + ' ' + fake.last_name())
    gender.append(person.get('gender'))
    address.append(fake.address())
#    birthdate.append(fake.date_of_birth())
    age.append(randint(18,100))
    COVID_results.append(fake.boolean(chance_of_getting_true=50)) #we can change this number to our required portion

# Create Data frame for better handling in ML models
variables=[names,gender,age,COVID_results,address]
df=pd.DataFrame(variables).transpose()
df.columns=["Name","gender","Age","COVID19 Test","Address"]
print(df.head())



                                # some useful functions that may need
# choose among a list based on sepecif probability
claim_reason=["Medical","Travel","Phone","Other"]
claim_reasons=np.random.choice(claim_reason,n_people, p=[.55,.15,.15,.15])
#print(claim_reasons)

# Create symptoms based on desired distribution
def symptomsGenerator(share, population):
    testSymptom=[]
    count=0
    for i in range(0,population):
        if count < share:
            testSymptom.append('yes')
        else:
            testSymptom.append('no')
        count+=1
    random.shuffle(testSymptom)
    return testSymptom

x=symptomsGenerator(7,n_people)
print("fever: ",x)

