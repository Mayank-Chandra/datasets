def studentdata():
    studentID={}
    while True:
        studentName=input("Enter Student Name(Full Name Seperated by Comma(,)): ")
        studentRoll=int(input("Enter Student RollNo: "))
        studentClass=input("Enter Student Class: ")
        str=input("Do you want to Continue(Yes/No): ")
        if studentRoll in studentID:
            print("Student ID Already Exist, Please Try Again With Different RollNO:")
        else:
            studentID[studentRoll]=studentName
        if str=='no':
            return studentID
data=studentdata()
print(data)

        