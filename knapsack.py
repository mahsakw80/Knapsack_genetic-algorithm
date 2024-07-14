from random import randint,shuffle,uniform

N=7
maxWeight=15
populationSize=10
mutationRate=0.0002
crossoverRate=1
rate=200
things=[(10,2),(5,3),(15,5),(7,7),(6,1),(18,4),(3,1)]

class Item:
    def __init__(self,profit,weight):
        self.profit=profit
        self.weight=weight

#***********************************Creat items************************************
def setItems(n,object):
    x=[]
    for i in object:
        x.append(Item(i[0],i[1]))
    return x
#***********************************Creat chromosomes*******************************
def chromosome (n,p):
    chromosomes=[]
    for i in range(p):
        new=[0 for i in range(n)]+[1 for i in range(n)]
        shuffle(new)
        new=new[:n]+[None]
        chromosomes.append(new)
    return chromosomes 
#*************************************Crossover*************************************
def one_point(chromosomes,n,p):
    neww=[]
    for i in range(0,p,2):
        pointer=randint(0,n-1)
        first_child=chromosomes[i][:pointer]+chromosomes[i+1][pointer:n]+[None]
        second_child=chromosomes[i+1][:pointer]+chromosomes[i][pointer:n]+[None]
        neww.append(first_child)
        neww.append(second_child)
    return neww 
#---------------------------------------       
def n_point(chromosomes,n,p,numpointer):
    new=[]
    pointer=set()
    for i in range(numpointer):
        pointer.update([randint(0,n-1)])
    pointer.update([0,n])
    sorted(pointer) 
    pointer=list(pointer)
    for i in range(0,p,2):
        first_child=[]
        second_child=[]
        clock=0
        for j in range(len(pointer)-1):
            if clock==0:
                first_child+=chromosomes[i][pointer[j]:pointer[j+1]]
                second_child+=chromosomes[i+1][pointer[j]:pointer[j+1]]
                clock=1
                continue
            if clock==1:
                second_child+=chromosomes[i][pointer[j]:pointer[j+1]]
                first_child+=chromosomes[i+1][pointer[j]:pointer[j+1]]
                clock=0
                continue
        new.append(first_child+[None])
        new.append(second_child+[None])
    return new    
#----------------------------            
def uniformm(chromosomes,n,p):
    new=[]
    for i in range(0,p,2):
        first_child=[]
        second_child=[]
        for j in range(n):
            clock=randint(0,1)
            if clock==0:
                first_child+=[chromosomes[i][j]]
                second_child+=[chromosomes[i+1][j]]
            if clock==1:
                second_child+=[chromosomes[i][j]]
                first_child+=[chromosomes[i+1][j]]
        new.append(first_child+[None])
        new.append(second_child+[None])
    return new        
#*************************************Mutation**********************************
def mutation(chromosomes,n,p,rate):
    for i in range(p):
        for j in range(n):
            if uniform(0,1)<rate:
                chromosomes[i][j]=1 if chromosomes[i][j]==0 else 0
    # select=[i for i in range(p)]
    # shuffle(select)
    # select=select[:int(((p)-1)*rate)]
    # for i in select:
    #     x=randint(0,n-1)
    #     chromosomes[i][x]=1 if chromosomes[i][x]==0 else 0
    return chromosomes
#*************************************Fitness**********************************
def fitness(chromosomes,n,p,items_list,max_weight,part):
    if part==1:
        start=0
        end=p
    else:    
        start=p
        end=len(chromosomes)
    max_fitness=0
    for i in range(start,end):
        weight=0
        profit=0
        for j in range(n):
            weight+=items_list[j].weight*chromosomes[i][j]
            profit+=items_list[j].profit*chromosomes[i][j]
        chromosomes[i][n]=profit if weight<=max_weight else 0
         
    return chromosomes
#*********************************Parent selection******************************
def roulette_wheel(chromosomes,n,p,size):
    newchromosomes=[]
    max= sum([chromosomes[i][n] for i in range(p)])
    for j in range(size):
        pick= randint(0, max)
        current = 0
        for f in range(p):
            if current<=pick:
                current+=chromosomes[f][n]
                new=chromosomes[f]
        newchromosomes.append(new)  
    return newchromosomes  
#------------------------       
def sus(chromosomes,n,p,size):
    max= sum([chromosomes[i][n] for i in range(p)])
    dist=max/size
    point=uniform(0,max)
    pointers=[]
    for i in range(size):
        poin=point+i*dist
        if poin>max:
            poin%=max
        pointers.append(poin)
    current = 0
    newchromosomes=[]
    current=0
    for k in pointers:
        for j in range(p):
            if current<=k:
                current+=chromosomes[j][n]
                new=chromosomes[j]
        newchromosomes.append(new)
    return newchromosomes
#---------------------------------    
def tournament(chromosomes,n,p,k):
    newchromosomes=[]
    for i in range(p):
        shuffle(chromosomes)
        tourn=chromosomes[:k]
        sorted(tourn, key=lambda chromosomes:(chromosomes[n])) 
        newchromosomes.append(tourn[0])
    return newchromosomes    
#************************************Elitism********************************
def elitism(chromosomes,n,numE):
    newch=chromosomes.copy()
    newch=sorted(newch,key=lambda x:(-x[n]))
    return newch[:numE]
#**************************************Main*********************************
def main(num,maxW,popSize,mutationRate,crossoverRate,thing,crosover,selection,elsize,rate=200,ktourn=2,npoint=3):
    crosspop=[]
    nocrosspop=[]
    elitismList=[]
    newpop=[]
    best=0
    best_soulotions=[]
    #set items
    items=setItems(num,thing)
    #Primary population
    currentPopulation=chromosome(num,popSize)
    
    for m in range(rate):
        currentPopulation=fitness(currentPopulation,num,popSize,items,maxW,1)

        if elsize>0:
            elitismList=elitism(currentPopulation,num,elsize)
            pSize=popSize-elsize
        else:pSize=popSize   
        if selection==1:
                others=(roulette_wheel(currentPopulation,num,popSize,pSize))
        elif selection==2:
                others=(sus(currentPopulation,num,popSize,pSize))
        elif selection==3:
                others=(tournament(currentPopulation,num,pSize,ktourn))
        #newpop+=elitismList
        #newpop+=others  

        select=[i for i in range(pSize)]
        shuffle(select)
        h=int((pSize)*crossoverRate)
        h+=0 if h%2==0 else 1
        noselect=select[h:]
        select=select[:h]
        crosspop+=(others[i] for i in select )
        nocrosspop+=(others[i] for i in noselect )
        if crosover==1:
                newp=one_point (crosspop,num,len(crosspop))  
        if crosover==2:
                newp=n_point(crosspop,num,len(crosspop),npoint)   
        if crosover==3:
                newp=uniformm(crosspop,num,len(crosspop))
        newp+=nocrosspop  
        newp=mutation(newp,num,len(newp),mutationRate)
        currentPopulation+=newp 
        currentPopulation+=elitismList 
        currentPopulation=fitness(currentPopulation,num,popSize,items,maxW,2)
        currentPopulation=sorted(currentPopulation,key=lambda x:(-x[num])) 
        currentPopulation=currentPopulation[:popSize]  
        if currentPopulation[0][num]>best:
            best=currentPopulation[0][num]
            best_soulotions.append( currentPopulation[0])




    result=max(best_soulotions[i][num] for i in range(len(best_soulotions)))
    for i in range(len(best_soulotions)):
        if best_soulotions[i][num]==result:
            soulotion=best_soulotions[i]
    #print(soulotion)




    result=max(best_soulotions[i][num] for i in range(len(best_soulotions)))
    for i in range(len(best_soulotions)):
        if best_soulotions[i][num]==result:
            soulotion=best_soulotions[i]
    return soulotion
        

        # currentPopulation= uniformm(currentPopulation,N,populationSize)
        # currentPopulation=fitness(currentPopulation,N,populationSize,items,maxWeight,2)
        # print(currentPopulation)
        # currentPopulation=elitism(currentPopulation,N,3)
        # print(currentPopulation)

#print( main(N,maxWeight,populationSize,mutationRate,crossoverRate,things,1,2,2,5,ktourn=2,npoint=3))
