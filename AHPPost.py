# Calculating Score and Points for Doctors
import pandas as pd
import numpy as np
import ast

#Importing Degree lables without double quotes
rm_quote = lambda x: x.replace('"','')
scoreFrame = pd.read_csv("NewScoreLabelData.csv",converters={'Degree':rm_quote})
degreeFrame = pd.read_csv("DegreePriority.csv")
experienceFrame = pd.read_csv("ExperiencePriority.csv")


print(scoreFrame)

#Experience Years Priority
experienceYears = experienceFrame['Experience'].values

#Score for each Experience
experienceScore = experienceFrame['AHP Score'].values

#Score Value Generation i.e Score for Each Degree
score = degreeFrame['AHP Score']
scoreValue = []
for i in range(len(score)):
    scoreValue.append(int(score[i]))

#Degree Value Generation from DegreePriorityCSV
degreeValue = degreeFrame['Degree']


#Generating Dictionary for each 
dictionaryForDegree = dict(zip(degreeValue,scoreValue))
dictionaryForExperience = dict(zip(experienceYears,experienceScore))

# print(dictionaryForDegree)
# print(dictionaryForExperience)


#Degree in Score Format Calculation
degreeData = scoreFrame['Degree'].values
degreeData = [ast.literal_eval(i) for i in degreeData]
print(degreeData)
pointsForDegree = []
for i in range(len(degreeData)):
    for j in range(len(degreeData[i])):
        temp = [dictionaryForDegree[j] for j in degreeData[i]]
    pointsForDegree.append(temp)

# Summing Degree Score Inside Array

pointsForDegreeNormalized = []
for i in range(len(pointsForDegree)):
        temp=sum(pointsForDegree[i])
        pointsForDegreeNormalized.append(temp)



#Experience in Score Format Calculation
experienceData = scoreFrame['Experience'].values
pointsForExperience = []
pointsForExperience = [dictionaryForExperience[i] for i in experienceData]


#Totalling Degree Score and Experience Score

finalAHPScore = [sum(i) for i in zip(pointsForDegreeNormalized,pointsForExperience)]
finalAHPPoint = finalAHPScore

#Posting Datas To Database
doctor_id = scoreFrame['ID'].values
print(len(doctor_id))

#Generating Score Table To New DataFrame
doctorData = scoreFrame['Doctor Name'].values
totalData = [doctor_id,doctorData,finalAHPScore,finalAHPPoint]
totalDataArray = np.array(totalData).transpose()
scoreTable = pd.DataFrame(data =totalDataArray,columns=['Doctor ID','Doctor Name','AHP Score','AHP Point'] )
scoreTable.to_csv(r'FinalScoreTable.csv')


#Posting AHP Score and Points To Database
import json
import urllib.request

import requests

ahpList = urllib.request.urlopen("http://manojphuyal-001-site1.atempurl.com/api/GetDoctorAHP")
ahpListData = json.loads(ahpList.read().decode())

ahpPostURL = "http://manojphuyal-001-site1.atempurl.com/api/PostDoctorAHP"

def send_data():
    for j in range(len(doctor_id)):
        data = {
            'AHP_Score':finalAHPScore[j],
            'AHP_Point':finalAHPPoint[j],
            'Doctor_ID':doctor_id[j]
            }
        requests.post(ahpPostURL,data=data)
        print(str(j+1)+" requests sent")
        # if(i>0):
        #     requests.put(ahpPostURL,data=data)
        #     print(str(j)+" requests sent")
        # else:
            

send_data()