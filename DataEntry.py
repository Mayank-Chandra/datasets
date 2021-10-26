def dataentry():
    dict={}
    print(">>>>Scurvey Of Employees<<<<")
    while True:
        EmpName=input("Enter the Employee Name: ")
        EmpEmail=input("Enter the Employee Email: ")
        EmpID=input("Enter the Employee ID: ")
        if EmpID in dict:
            print("The ID already exist.\n",'Please Enter Different ID\n')
        else:
            dict[EmpID]=EmpName
        str=input("Do you want to continue(Yes/No): ")
        if str=='no':
            return dict
data=dataentry()
print(data)
        

        