
import pandas as pd
import numpy as np

#Degree Priority
degreeFrame = pd.read_csv("DegreePriority.csv")
# print(degreeFrame.head(10))
print()

degreeScore = np.array(degreeFrame['AHP Score']).astype(int)
print(degreeScore)

#Experience Priority
experienceFrame = pd.read_csv("ExperiencePriority.csv")
# print(experienceFrame.head(10))
print()

experienceScore = np.array(degreeFrame['AHP Score']).astype(int)

#Fetching Doctor Information

import json
import urllib.request

doctorInfo = urllib.request.urlopen("http://manojphuyal-001-site1.atempurl.com/api/GetDoctor")
doctorEducationInfo = urllib.request.urlopen("http://manojphuyal-001-site1.atempurl.com/api/GetDoctorDegree")



doctorInfoData = json.loads(doctorInfo.read().decode())
doctorEducationInfoData = json.loads(doctorEducationInfo.read().decode())



doctor_id = []
doctor_name = []
doctor_experience = []
for i in range(len(doctorInfoData)):
        doctor_id.append(doctorInfoData[i]['Doctor_ID'])
        doctor_name.append(doctorInfoData[i]['Doctor_Name'])
        doctor_experience.append(doctorInfoData[i]['Doctor_Experience'])





# Building a Table DataFrame

doctor_degree = []

for i in range(len(doctor_id)):
        doctorEducationInfoArray = urllib.request.urlopen("http://manojphuyal-001-site1.atempurl.com/api/GetDoctorDegree?id="+str(doctor_id[i]))
        doctorEducationInfoDataArray = json.loads(doctorEducationInfoArray.read().decode())
        tempArray=[]
        for j in range(len(doctorEducationInfoDataArray)):
                tempArray.append(doctorEducationInfoDataArray[j]['Doctor_Degree_Name'])
        doctor_degree.append(tempArray)
        # for k in range(len(doctor_degree)):
        #         doctor_degree.append(doctor_degree[k])

# doctorFrame['Degree']=[doctor_degree]
totalData = [doctor_id,doctor_name,doctor_degree,doctor_experience]
totalDataArray = np.array(totalData).transpose()
doctorFrame = pd.DataFrame(data=totalDataArray,columns=['ID','Doctor Name','Degree','Experience'])
doctorFrame.to_csv(r'NewScoreLabelData.csv')

