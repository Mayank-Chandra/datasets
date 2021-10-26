def Sorting(L):
    for i in range(0,len(L)):
        for j in range(i+1,len(L)):
            if L[i]>L[j]:
                temp=L[i]
                L[i]=L[j]
                L[j]=temp
    print(L)

Sorting([5,4,3,2,1,0])

def TrueOrFalse(a,b):
    Ans=a or b and b or a
    if Ans==True:
        print("True")
    else:
        print("False")
    
TrueOrFalse(False,True)
