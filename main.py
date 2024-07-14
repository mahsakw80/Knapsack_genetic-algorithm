import csv
from knapsack import main

    






k=0
np=0
print("----------Knapsack Problem---------- \n\n")
csvf=input("Enter csv file  name : ")
print("\n")
population=int(input("Population Size = "))
print("\nParent Selection:\n1-Roulette Wheel\n2-Stochastic Universal Sampling\n3-Tournament")
parent_selection=int(input("Enter number : "))
if parent_selection==3:
    k=int(input("Numbeer of k = "))
print("\nCroos Over :\n\t1-One Point\n\t2-N Point\n\t3-Uniform")
crossover=int(input("Enter number : "))
if crossover==2:
    np=int(input("Number of pointers = ")) 
print("\n")   
crossoverrate=float(input("Cross Over Rate = "))
print("\n")
mutationrate=float(input("Mutation Rate = "))
print("\n")
rate=int(input("The number of iterations of the algorithm = "))
print("\n")
maxWeigt=int(input("Maximum backpack weight = "))
print("\nElitism (If you don't want to set the number to 0)")
elitism=int(input("Number of Elitism = "))


itemslist=list()
things=list()
with open(csvf,"r") as csvfile:
    data=csv.reader(csvfile)
    for line in data:
        itemslist.append(line)
    
    num=len(itemslist[0])
    for i in range(num):
        item=(int(itemslist[2][i]),int(itemslist[1][i]))
        things.append(item)
result=main(num,maxWeigt,population,mutationrate,crossoverrate,things,crossover,parent_selection,elitism,rate,k,np) 
print("\n--------Result--------\n")
weight=0
print("Items : " ,end="   ")
for i in range(num):
    if result[i]==1:
        print(itemslist[0][i],end="\t")
        weight+=things[i][1]
print("\nWeight = ",weight,"  Profit = ",result[-1])        
    
