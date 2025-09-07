
# COVID-19 Synthetic Data Generator
# Author: r-hedayati
# License: MIT
#
# This script generates synthetic COVID-19 patient data for research and educational purposes.

import pandas as pd
import numpy as np
import random
from faker import Faker
from random import randint


# DataFrame display configuration (optional)
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 12)


# Initialize Faker
fake = Faker()
Faker.seed(3210)  # Remove or change seed for different data each run


# Number of synthetic patients to generate
n_people = 20

# Lists to store generated data
names = []
ages = []
genders = []
addresses = []
COVID_results = []


# Generate a random first name and gender
def first_name_and_gender():
    gender = 'Male' if random.randint(0, 1) == 0 else 'Female'
    first_name = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
    return {'gender': gender, 'first_name': first_name}


# Generate demographic and COVID test data
for _ in range(n_people):
    person = first_name_and_gender()
    names.append(f"{person['first_name']} {fake.last_name()}")
    genders.append(person['gender'])
    addresses.append(fake.address())
    ages.append(randint(18, 100))
    COVID_results.append(fake.boolean(chance_of_getting_true=100))  # Adjust chance as needed



# Generate symptoms based on probability share
def symptoms_generator(probability, population):
    symptom_list = ['yes'] * round(probability * population) + ['no'] * (population - round(probability * population))
    random.shuffle(symptom_list)
    return symptom_list, symptom_list.count('yes')


# Generate related symptoms based on transition probability
def related_symptoms_generator(input_symptom, output_symptom, pop, share, positive_cases):
    cnt = 0
    count_share_cnt = 0
    count_share = round(share * pop)
    i = 0
    flag = 0
    while i > -1:
        if ((positive_cases == count_share_cnt) and (cnt == count_share)):
            break
        if (count_share > positive_cases):
            if (positive_cases == count_share_cnt):
                break
        if cnt != count_share:
            if input_symptom[i] == 'yes':
                output_symptom[i] = 'yes'
                cnt += 1
                count_share_cnt += 1
        if count_share_cnt != positive_cases:
            if input_symptom[i] == 'no':
                output_symptom[i] = 'yes'
                count_share_cnt += 1
        if count_share_cnt > positive_cases:
            if (input_symptom[i] == 'no'):
                output_symptom[i] = 'no'
                count_share_cnt -= 1
        i += 1
        if i == (n_people - 1):
            if (count_share_cnt > positive_cases):
                i = 0
                flag += 1
        if flag == 2:
            break
    return output_symptom, count_share


# Calculate number of positive cases for each symptom
def positive_cases_generator(share_list, pop):
    return [round(share * pop) for share in share_list]


# Empty lists for symptoms
test_cough, test_fatigue, test_breath, test_sore_throat, test_headache, test_mylagia, test_chills, test_nausea, test_nasal, test_diarrhea = (['no'] * n_people for _ in range(10))




# Symptom probabilities (WHO report)
symptom_probabilities = [0.879, 0.677, 0.381, 0.186, 0.139, 0.136, 0.148, 0.114, 0.05, 0.048, 0.037]
positive_cases_list = positive_cases_generator(symptom_probabilities, n_people)


# Symptoms without transition probability
fatigue = symptoms_generator(symptom_probabilities[2], n_people)
short_breath = symptoms_generator(symptom_probabilities[3], n_people)
chills = symptoms_generator(symptom_probabilities[7], n_people)
nasal = symptoms_generator(symptom_probabilities[9], n_people)


# Symptoms with transition probability
fever = symptoms_generator(symptom_probabilities[0], n_people)
cough = related_symptoms_generator(fever[0], test_cough, fever[1], 0.78, positive_cases_list[1])
sore_throat = related_symptoms_generator(cough[0], test_sore_throat, cough[1], 0.84, positive_cases_list[4])
headache = related_symptoms_generator(cough[0], test_headache, cough[1], 0.84, positive_cases_list[5])
mylagia = related_symptoms_generator(cough[0], test_mylagia, cough[1], 0.84, positive_cases_list[6])
nausea = related_symptoms_generator(sore_throat[0], test_nausea, sore_throat[1], 0.65, positive_cases_list[8])
diarrhea = related_symptoms_generator(nausea[0], test_diarrhea, nausea[1], 1, positive_cases_list[10])




# Create DataFrame for ML models or analysis
columns = [
    "name", "gender", "age", "fever", "cough", "sore_throat", "headache", "mylagia",
    "nausea", "diarrhea", "fatigue", "short_of_breath", "chills", "nasal", "COVID19_test"
]
data = list(zip(
    names, genders, ages, fever[0], cough[0], sore_throat[0], headache[0], mylagia[0],
    nausea[0], diarrhea[0], fatigue[0], short_breath[0], chills[0], nasal[0], COVID_results
))
df = pd.DataFrame(data, columns=columns)
df.to_csv('positiveCases.csv', index=False)



# To generate negative test cases, repeat the above process with adjusted probabilities and COVID_results set to 'no'.
# Example:
# covid_result_negative = ['no'] * n_people
# fatigueN = symptoms_generator(0.298, n_people)
# ...
# Extend as needed for your use case.
