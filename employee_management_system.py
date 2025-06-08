import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv(r"C:\Users\aswin\Desktop\completed projects\EMPLOYEE MANAGEMENT\management.env")
conn=psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port="5432"
)
con=conn.cursor()
#-------- add employee --------
def add_employee(first_name1, last_name1, department1, job_title1, salary1, hire_date1):
    query ="""
    INSERT INTO employees (first_name, last_name, department, job_title, salary, hire_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING emp_id;
    """
    con.execute(query, (first_name1, last_name1, department1, job_title1, salary1, hire_date1))
    new_emp_id=con.fetchone()[0]
    conn.commit()
    return new_emp_id
#-------- view employee --------
def view_employee(emp_id):
    view_table=["Employee_ID","First_name","Last_name","Department","Job_title","Salary","Hire_date","is_active"]
    query = "SELECT * FROM employees WHERE emp_id = %s AND is_active=TRUE"
    con.execute(query, (emp_id,))
    employee = con.fetchone()
    if employee:
        print("\n--- EMPLOYEE DETAILS ---")
        for i in range(len(employee)):
            print(f"{view_table[i]}:{employee[i]}")
    else:
        print("EMPLOYEE NOT FOUND or is inactive")
#-------- update employee --------   
def update_employee(emp_id,department=None,salary=None):
    if department and department !='none':
        query='''UPDATE employees SET department=%s WHERE emp_id=%s AND is_active=TRUE'''
        con.execute(query,(department,emp_id))
    if salary and salary != 'none':
        query='UPDATE employees SET salary =%s WHERE emp_id=%s AND is_active=TRUE'
        con.execute(query,(salary,emp_id))
    conn.commit()
#-------- delete employee --------
def delete_employee(emp_id):
    try:
        query = "UPDATE employees SET is_active = FALSE WHERE emp_id = %s"
        con.execute(query, (emp_id,))
        conn.commit()
        print(f"Employee {emp_id} marked as inactive (soft deleted).")  
    except Exception as e:
        conn.rollback()
        print("An error occurred:", e)
#-------- mark attendance --------
def mark_attendance(emp_id,date,status):
    query="INSERT INTO attendance(emp_id,date,status) VALUES(%s,%s,%s)"
    con.execute(query,(emp_id,date,status))
    conn.commit()
#-------- view attendance report --------
def view_attendance_report(emp_id):
    query='SELECT*FROM attendance WHERE emp_id=%s'
    con.execute(query,(emp_id,))
    records=con.fetchall()
    for record in records:
        print(record)
#-------- calculate salary --------
def calculate_salary(emp_id,base_salary,bonus=0,deductions=0):
    total_salary=max(0,base_salary+bonus-deductions)
    query="""
    INSERT INTO salary (emp_id,base_salary,bonus,deductions,total_salary)
    VALUES(%s,%s,%s,%s,%s)"""
    con.execute(query,(emp_id,base_salary,bonus,deductions,total_salary))
    conn.commit()
    return total_salary
#-------- generate employee report--------
def generate_employee_report(emp_id):
    view_table = ["Employee_ID", "First_name", "Last_name", "Department", "Job_title", "Salary", "Hire_date1","is_active"]
    attendance_table = ["record_id", "emp_id", "date", "status"]
    salary_table = ["salary_id", "emp_id", "base_salary", "bonus", "deductions", "total_salary"]
    try:
        con.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
        employee = con.fetchone()

        con.execute("SELECT * FROM attendance WHERE emp_id = %s", (emp_id,))
        attendance = con.fetchall()

        con.execute("SELECT * FROM salary WHERE emp_id = %s", (emp_id,))
        salary = con.fetchall()

        if employee:
            print("\n--- EMPLOYEE DETAILS ---")
            for i in range(len(employee)):
                print(f"{view_table[i]}: {employee[i]}")
        else:
            print("EMPLOYEE NOT FOUND or is inactive")
            return

        if attendance:
            print("\n--- ATTENDANCE RECORDS ---")
            for record in attendance:
                for i in range(len(record)):
                    print(f"{attendance_table[i]}: {record[i]}")
                print("-" * 20)
        else:
            print("\nNo attendance records found.")

        if salary:
            print("\n--- SALARY DETAILS ---")
            for record in salary:
                for i in range(len(record)):
                    print(f"{salary_table[i]}: {record[i]}")
                print("-" * 20)
        else:
            print("\nNo salary records found.")

    except Exception as e:
        print(f"An error occurred: {e}")
#-------- getting inputs from user --------
status=True
while(status is True):
    print("1-add employee,2-view employee,3-update employee,4-delete employee,5-mark attendance,6-view attendance report,7-calculate salary,8-generate employee report")
    operation=input("enter a number to use certain operations:")
    try:
        if operation=='1':
            fn=input("ENTER FIRST NAME:")
            ln=input("ENTER LAST NAME:")
            dep=input("ENTER DEPARTMENT:")
            jt=input("ENTER JOB TITLE:")
            s=float(input("ENTER SALARY:"))
            hire=input("ENTER HIRING DATE(YYYY-MM-DD):")
            hire_date=datetime.strptime(hire,'%Y-%m-%d').date()
            a=add_employee(fn,ln,dep,jt,s,hire_date)
            print(f"New employee's ID:{a}")
            print("\n--- NEW EMPLOYEE ADDED ---")
        elif operation=='2':
            employee_id=int(input("ENTER YOUR EMPLOYEE ID:"))
            view_employee(employee_id)
        elif operation=='3':
            employee_id=int(input("ENTER YOUR EMPLOYEE ID:"))
            a=input("IF YOU CHANGE DEPARTMENT THEN ENTER NEW DEPARTMENT OTHERWISE ENTER NONE:")
            b_input = input("IF SALARY IS CHANGED ENTER NEW SALARY OTHERWISE ENTER NONE:")
            b = float(b_input) if b_input.lower() != 'none' else 'none'
            update_employee(employee_id,a,b)
            print("\n--- EMPLOYEE'S DETAILS UPDATED ---")
        elif operation=='4':
            employee_id=input("ENTER THE EMPLOYEE ID TO DELETE:")
            delete_employee(employee_id)
            print("\n--- EMPLOYEE REMOVED ---")
        elif operation=='5':
            employee_id=int(input("ENTER THE EMPLOYEE ID:"))
            date1=input("ENTER DATE(YYYY-MM-DD):")
            date2=datetime.strptime(date1,'%Y-%m-%d').date()
            s=input("ENTER TODAY STATUS:")
            mark_attendance(employee_id,date2,s)
            print("\n--- ATTENDANCE MARKED ---")
        elif operation=='6':
            employee_id=int(input('ENTER YOUR EMPLOYEE ID:'))
            view_attendance_report(employee_id) 
        elif operation=='7':
            employee_id=int(input('ENTER YOUR EMPLOYEE ID:'))
            bs=float(input('ENTER YOUR BASE SALARY:'))
            bo=float(input("ENTER YOUR BONUS IF NONE ENTER 0:"))
            de=float(input('ENTER DEDUCTION IF NOT ENTER 0:'))
            a=calculate_salary(employee_id,bs,bo,de)
            print(a)
        elif operation=='8':
            employee_id=int(input("ENTER EMPLOYEE ID TO GENERATE REPORT:"))
            generate_employee_report(employee_id)
        else:
            print("YOU ENTER INVALID OPERATION!")
    except Exception as e:
        print(f"An error occcured:{e}")
    activity=input('Do you want to continue IF YES ENTER 0 OTHERWISE 1:')
    if activity == '0':
        status=True
    else:
        status=False
con.close()
conn.close()
