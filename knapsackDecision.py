from itertools import product,permutations,combinations,combinations_with_replacement
import time
import os
import matplotlib.pyplot as plt
import subprocess

def readFiles(filename):
    weightCost = []
    M = []
    B = []
    with open(filename,'r') as data:
        stock = data.readline()
        while stock !="":
            stock = stock.replace('\n','').split(' ')
            n = int(stock[1])
            M.append(int(stock[2]))
            B.append(int(stock[3]))
            weightCost.append([(int(stock[4+2*y]),int(stock[4+2*y+1])) for y in range(n)])
            stock = data.readline()
    return [n,M,B,weightCost]

count = 0

def knapsackDecisionBrutForce(n,M,B,WC):
    global count
    valCost=B
    valWeight = 0
    stockWeight = 0
    stockCost = 0
    solution= []
    for element in list(product('01',repeat=n)):
        count+=1
        for i in range(n):
            stockWeight+=int(element[i])*WC[i][0]
            stockCost+=int(element[i])*WC[i][1]
        if stockWeight <= M:
            if stockCost > B:
                solution = [int(val) for val in element]
                return stockWeight,stockCost,solution
            else:
                stockCost=0
                stockWeight=0
        else:
            stockCost=0
            stockWeight=0
    if solution == tuple(0 for i in range(n)):
        solution=[0 for i in range(n)]
    return valWeight,valCost,solution

def knapsackBranchAndBound(n,M,B,WC,index,currentknapsack,currentWeight,currentCost):
    global count
    if currentWeight>M:
        return False
    if currentCost>B:
        return [currentWeight,currentCost,currentknapsack]
    for y in range(index,n):
        for i in range(y,n):
            count+=1
            if currentknapsack[i]!=1:
                currentknapsack[i]=1
                currentWeight+=int(WC[i][0])
                currentCost+=int(WC[i][1])
                stock = knapsackBranchAndBound(n,M,B,WC,i+1,currentknapsack,currentWeight,currentCost)
                if stock != False:
                    return stock
                currentknapsack[i]=0 
                currentWeight-=int(WC[i][0])
                currentCost-=int(WC[i][1])
        break
    return False

def showPlot(filename,n):
    line = subprocess.check_output(['tail', '-1', filename])
    line = str(line[1:len(line)-1])[1:]
    line.replace("'",'')
    stock = line[1:len(line)-1].split(';')
    frequencies = []
    for element in stock:
        var = element[1:len(element)-1].split(',')
        frequencies.append([int(var[0]),int(var[1])])
    weights = [0]+[2**i for i in range(1,n+1)]
    plotFrequencies = [0 for i in range(n+1)]
    index=1
    for count in range(len(frequencies)):
        if frequencies[count][0] < 2**index :
            plotFrequencies[index]+=frequencies[count][1]
        else:
            index+=1
            plotFrequencies[index]+=frequencies[count][1]
    mean = 0
    for i in range(len(plotFrequencies)):
        mean+= plotFrequencies[i]*weights[i]
    mean/=500
    print('mean = '+str(mean))
    print(plotFrequencies)
    print(weights)
    input()
    # plt.hist(weights,weights=plotFrequencies,ec='black')
    # plt.xscale('log',basex=2)
    y_pos = [x+3 for x in range(len(plotFrequencies))]
    plt.bar(y_pos,plotFrequencies)
    plt.xticks(y_pos,weights)
    plt.show()


def Menu():
    global count
    frequencies = []
    print("Which algorithm do you want to use ?")
    print("1. Brut Force(decision)\n2. Branch And Bound (decision)\n3. Show Plot\n")
    ans = input("Selection : ")
    while(ans!='1' and ans!='2' and ans!='3'):
        print("Wrong selection, please try again \n")
        ans = input("Selection : ")
    if ans!='3':
        files = os.listdir("NR-Inst")
    else:
        files = os.listdir("solutions/Decision")
    files.sort()
    print("Which file do you want to use ?")
    for i in range(len(files)):
        print(str(i+1)+". "+files[i]+'\n')
    ans2 = input("Selection : ")
    while(int(ans2)<1 or int(ans2)>len(files)):
        print("Wrong selection, please try again \n")
        ans2 = input("Selection : ")
    if ans=='1':
        [n,M,B,WC] = readFiles("NR/"+files[int(ans2)-1])
        f = open("solutions/Decision/testLeeroyBrutDecision-"+files[int(ans2)-1],'w+')
        start = time.time()
        for i in range(500):
            stock = knapsackDecisionBrutForce(n,M[i],B[i],WC[i])
            if 1 not in stock[2]:
                f.write(str(i+1)+"\tFalse\n")
            else:
                f.write(str(i+1)+'\t'+str(stock[0])+'\t'+str(stock[1])+'\t'+str(stock[2])+'\n')
            if count not in list(freq[0] for freq in frequencies):
                frequencies.append([count,1])
            else:
                for i in range(len(frequencies)): 
                    if frequencies[i][0]==count:
                        frequencies[i][1]+=1
            count=0
        frequencies.sort()
        f.write(str(frequencies).replace(', [',';['))
        f.close()
        print(str(time.time()-start))
    if ans=='2':
        falseCount=0
        [n,M,B,WC] = readFiles("NR/"+files[int(ans2)-1])
        f = open("solutions/Decision/testLeeroyBBDecision-"+files[int(ans2)-1],'w+')
        start = time.time()
        for i in range(500):
            stock = knapsackBranchAndBound(n,M[i],B[i],WC[i],0,[0 for i in range(n)],0,0)
            if str(stock)=='False':
                f.write(str(i+1)+'\t'+str(stock)+'\n')
                falseCount +=1
            else:
                f.write(str(i+1)+'\t'+str(stock[0])+'\t'+str(stock[1])+'\t'+str(stock[2])+'\n')
            if count not in list(freq[0] for freq in frequencies):
                frequencies.append([count,1])
            else:
                for i in range(len(frequencies)): 
                    if frequencies[i][0]==count:
                        frequencies[i][1]+=1
            count=0
        frequencies.sort()
        f.write(str(frequencies).replace(', [',';['))
        f.close()
        print(str(time.time()-start))
    if ans=='3':
        x = int(input('Enter the value of n please :'))
        showPlot("solutions/Decision/"+files[int(ans2)-1],x)

    

Menu()
# f1 = open("solutions/Decision/testLeeroyBBDecision-NR4_inst.dat",'r')
# f2 = open("solutions/Decision/testLeeroyBrutDecision-NR4_inst.dat",'r')

# stock1,stock2 = f1.readline(),f2.readline()
# count=0
# count1=0
# count2=0
# while stock1[0]!="[":
#     content1,content2=stock1.split("\t"),stock2.split("\t")
#     if content1[1]=='False\n':
#         count1+=1
#     if content2[1]=='False\n':
#         count2+=1
#     if content1[1]==content2[1] and content1[1]=='False\n':
#         count+=1
#     stock1,stock2 = f1.readline(),f2.readline()
# print(count)
# print(count1)
# print(count2)