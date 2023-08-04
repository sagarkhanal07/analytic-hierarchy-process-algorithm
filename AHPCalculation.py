import numpy as np
import pandas as pd

print("=============================")
print("Analytic Hierarchy Process")
print("=============================")

# Objective
objective = input("What's the main objective?: ")

#Criterias
no_of_criterias = int(input("No of Criterias?: "))
criterias = []
for i in range(no_of_criterias):
    criterias_input = input("Enter Criteria "+str(i+1)+": ")
    criterias.append(criterias_input)

rank_collection_one = []
rank_collection_two = []

factor_one = []
factor_two = []


#SubCriterias
print("=============================")
No_Factors_One = 0
No_Factors_Two = 0
No_Factors = [No_Factors_One,No_Factors_Two]

for i in range(no_of_criterias):
    times = int(input("How many "+str(criterias[i]).lower()+' values are there?: '))
    No_Factors[i] = int(times)

# For First Criteria

def rankModel(no_of_factors,s):
    n = 0
    factors = {}
    com_board = [["  " for i in range(no_of_factors + 1)] for z in range(no_of_factors + 1)]
    norm_factors = [["  " for i in range(no_of_factors)] for z in range(no_of_factors)]
    while n < no_of_factors:
        factor =input("Enter factor No. {} name: ".format(n + 1))
        factors[n] = factor
        global factor_one
        global factor_two
        if(s==0):
            factor_one.append(factor)
        elif(s==1):
            factor_two.append(factor)
        com_board[0][n + 1] = factor
        com_board[n + 1][0] = factor
        com_board[n + 1][n + 1] = 1
        n += 1
    # print(com_board)

    # inserting the User Weights for each factors pair

    def weights():
        #Pair Comparison
        print("Pair Comarison Importance Scale: Pick One Value")
        print("============================================")
        print("============================================")
        print("1 - Equal Importance")
        print("2 - Equal to Moderately Importance")
        print("3 - Moderately Importance")
        print("4 - Moderately to Strongly Importance")
        print("5 - Strongly Importance")
        print("6 - Strong to very Strongly Importance")
        print("7 - Very Strongly Importance")
        print("8 - Very Strongly to Extremely Importance")
        print("9 - Extremely Importance")
        print("============================================")
        print("============================================")
        x = 0
        while x <= no_of_factors ** 2:
            z = x + 1
            while z < no_of_factors:
                com_board[x + 1][z + 1] = float(input("The Importance of Factor {} {} compared to Factor {} {} on a Scale of (1-9): ".format(x + 1,factors[x],z + 1,factors[z])))
                com_board[z + 1][x + 1] = 1 / (com_board[x + 1][z + 1])
                z += 1
            x += 1


    weights()


    # Normalization & weight determination
    x = 1
    tot_factors = [0 for i in range(no_of_factors)]
    print("Total values for Each Column")
    while x <= no_of_factors:
        j = 1
        while j <= no_of_factors:
            tot_factors[(x - 1)] = float(tot_factors[(x - 1)]) + com_board[j][x]
            j += 1
        print(tot_factors[(x - 1)], end=" ")
        print()
        x += 1
    
    print()
    print("=================================")
    print("Normalized values for Each Factor")
    print("=================================")
    x = 1
    while x <= no_of_factors:
        j = 1
        while j <= no_of_factors:
            norm_factors[j - 1][x - 1] = float(com_board[j][x]) / tot_factors[x - 1]
            j += 1
        x += 1
    x = 1
    while x <= no_of_factors:
        j = 1
        while j <= no_of_factors:
            print(norm_factors[(x - 1)][j - 1], end=" ")
            j += 1
        print()
        x += 1

    # Normalization & weight determination
    print()
    print("=================================")
    print("Priority vector or weight Values")
    print("=================================")
    x = 0
    priority_vector = [0 for i in range(no_of_factors)]
    while x < no_of_factors:
        priority_vector[x] = sum(norm_factors[x]) / no_of_factors
        print(factors[x], ": ", priority_vector[(x)])
        global rank_collection_one
        global rank_collection_two
        if(s==0):
            rank_collection_one.append(priority_vector[(x)])
        elif(s==1):
            rank_collection_two.append(priority_vector[(x)])
        x += 1




for i in range(no_of_criterias):
    print("==================================")
    print("Ranking for Sub-Criterian :"+str(criterias[i]))
    print("==================================")
    rankModel(No_Factors[i],i)
    if(i==0):
        dataframeOne = pd.DataFrame(data =rank_collection_one,columns=['Weight'] )
        for j in range(len(factor_one)):
            dataframeOne.rename(index={j:factor_one[j]},inplace=True)
        dataframeOne['Rank'] = dataframeOne['Weight'].rank(ascending=0)
        
    elif(i==1):
        dataframeTwo = pd.DataFrame(data =rank_collection_two,columns=['Weight'] )
        for j in range(len(factor_two)):
            dataframeTwo.rename(index={j:factor_two[j]},inplace=True)
        dataframeTwo['Rank'] = dataframeTwo['Weight'].rank(ascending=0)


# Scoring

score_one = []
total_one = len(rank_collection_one)
for i in range(total_one):
    score_one.append(total_one - dataframeOne['Rank'][i] + 1)
dataframeOne['AHP Score']= score_one
dataframeOne.to_csv(r'DegreePriority.csv')

score_two = []
total_two = len(rank_collection_two)
for i in range(total_two):
    score_two.append(total_two - dataframeTwo['Rank'][i] + 1)
dataframeTwo['AHP Score']= score_two
dataframeTwo.to_csv(r'ExperiencePriority.csv')


print("==============================")
print()
print(dataframeOne)
print("==============================")
print()
print(dataframeTwo)
print("==============================")
