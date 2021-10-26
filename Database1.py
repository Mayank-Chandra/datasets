def database():
    Employees={}
    while True:
        EmpName=input("Enter Your Full Name: ")
        EmpID=input("Enter Your ID: ")
        EmpDOB=input("Enter your Date Of Birth: ")
        EmpAddress=input("Enter your Permanent Address: ")
        EmpSalary=float(input('Enter your Salary: '))
        if EmpID in Employees:
            print("EmpID Already Exists Please Enter Different Employee ID...")
        else:
            Employees[EmpID]=EmpName

            avgsalary=0
            for x in Employees:
                avgsalary=EmpSalary/12
            print("Average Salary of The Employee is: ",avgsalary)
        str=input("Do you Wish to Continue: ")
        if str=='no':
         return Employees

           
data=database()
print(data)