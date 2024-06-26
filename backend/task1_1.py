
import cx_Oracle

def create_employee_hire_sp():
    
    # Task 1_1: Create a Procedure called Employee_hire_sp 
    connection = None
    username = 'COMP214_W24_ers_77'
    password = 'passwords'
    dsn = '199.212.26.208:1521/SQLD'
    encoding = 'UTF-8'
    
    try:
        connection = cx_Oracle.connect(username, password, dsn, encoding=encoding)
        
        cursor = connection.cursor()
        
        sql_procedure = """
        
        CREATE OR REPLACE PROCEDURE Employee_hire_sp (
            p_first_name    IN HR_EMPLOYEES.FIRST_NAME%TYPE,
            p_last_name     IN HR_EMPLOYEES.LAST_NAME%TYPE,
            p_email         IN HR_EMPLOYEES.EMAIL%TYPE,
            p_salary        IN HR_EMPLOYEES.SALARY%TYPE,
            p_hire_date     IN HR_EMPLOYEES.HIRE_DATE%TYPE,
            p_phone         IN HR_EMPLOYEES.PHONE_NUMBER%TYPE,
            p_job_id        IN HR_EMPLOYEES.JOB_ID%TYPE,
            p_manager_id    IN HR_EMPLOYEES.MANAGER_ID%TYPE,
            p_department_id IN HR_EMPLOYEES.DEPARTMENT_ID%TYPE
        ) AS
        BEGIN
            INSERT INTO HR_EMPLOYEES (
                EMPLOYEE_ID,
                FIRST_NAME,
                LAST_NAME,
                EMAIL,
                PHONE_NUMBER,
                HIRE_DATE,
                JOB_ID,
                SALARY,
                MANAGER_ID,
                DEPARTMENT_ID
            ) VALUES (
                HR_EMPLOYEES_SEQ.NEXTVAL,
                p_first_name,
                p_last_name,
                p_email,
                p_phone,
                p_hire_date,
                p_job_id,
                p_salary,
                p_manager_id,
                p_department_id
            );
            
            COMMIT;
        END Employee_hire_sp;
        
        """
        cursor.execute(sql_procedure)

        print("Procedure Employee_hire_sp created successfully!")

    except cx_Oracle.Error as error:
        print(f"Error creating procedure: {error}")
    finally:
        if connection:
            connection.close()
  
    ''' 
    try:
        connection = cx_Oracle.connect(username, password, dsn, encoding=encoding)
        
        cursor = connection.cursor()
        
        sql_statement = """
        
        BEGIN
            Employee_hire_sp(
                p_first_name    => 'Julian',
                p_last_name     => 'Aristizabal',
                p_email         => 'juliandres1227@gmail.com',
                p_salary        => 6000,
                p_hire_date     => TO_DATE('2024-04-01', 'YYYY-MM-DD'),
                p_phone         => '4379918059',
                p_job_id        => 'IT_PROG',
                p_manager_id    => 103,
                p_department_id => 60
            );
        END;
        
        """
        cursor.execute(sql_statement)

        print("Employee record created successfully!")

    except cx_Oracle.Error as error:
        print(f"Error creating procedure: {error}")
    finally:
        if connection:
            connection.close()
    '''

    # Task 2_3: Create a Procedure called new_job 
    try:
        connection = cx_Oracle.connect(username, password, dsn, encoding=encoding)
        
        cursor = connection.cursor()
        
        sql_statement = """

        CREATE OR REPLACE PROCEDURE new_job(
            p_jobid IN HR_JOBS.job_id%TYPE,
            p_title IN HR_JOBS.job_title%TYPE, 
            p_minsal IN HR_JOBS.min_salary%TYPE
        ) IS
            v_maxsal HR_JOBS.max_salary%TYPE := 2 * p_minsal;  
        BEGIN
            INSERT INTO HR_JOBS (job_id, job_title, min_salary, max_salary)
            VALUES (p_jobid, p_title, p_minsal, v_maxsal);

            DBMS_OUTPUT.PUT_LINE('New row added to JOBS table:');
            DBMS_OUTPUT.PUT_LINE(p_jobid || ' | ' || p_title || ' | ' || p_minsal || ' | ' || v_maxsal);
        END new_job;

        """

        cursor.execute(sql_procedure)

        print("Procedure new_job created successfully!")

    except cx_Oracle.Error as error:
        print(f"Error creating procedure: {error}")
    finally:
        if connection:
            connection.close()
            
    # Task 3: Create a Procedure called check_salary
    try:
        connection = cx_Oracle.connect(username, password, dsn, encoding=encoding)
        
        cursor = connection.cursor()
        
        sql_statement = """
        
        CREATE OR REPLACE PROCEDURE Check_salary(p_job_id IN VARCHAR2, p_salary IN NUMBER) AS
        v_min_sal NUMBER;
        v_max_sal NUMBER;
        
        BEGIN
        -- Get the minimum and maximum salary for the specified job
            SELECT min_salary, max_salary INTO v_min_sal, v_max_sal
            FROM hr_jobs 
            WHERE job_id = p_job_id;
        
        -- Check if the salary is within the acceptable range
            IF salary < v_min_sal OR p_salary > v_max_sal THEN
            RAISE_APPLICATION_ERROR(-20001, 'Invalid salary ' || p_salary ||
                                '. Salaries for job ' || p_job_id ||
                                ' must be between ' || v_min_sal || ' and ' || v_max_sal);
            END IF;
        END;
        
        """

        cursor.execute(sql_procedure)
        print("Procedure created successfully!")

    except cx_Oracle.Error as error:
        print(f"Error creating procedure: {error}")
    finally:
        if connection:
            connection.close()
    
    # Task 3: Creating a Trigger called check_salary
    try:
        connection = cx_Oracle.connect(username, password, dsn, encoding=encoding)
        
        cursor = connection.cursor()
        
        sql_statement = """
        
        CREATE OR REPLACE TRIGGER CHECK_SALARY_TRG
        BEFORE INSERT OR UPDATE ON employees
        FOR EACH ROW
        DECLARE
            job_min_sal NUMBER;
            job_max_sal NUMBER;
        BEGIN
        -- Get the minimum and maximum salary for the employee's job
            SELECT min_salary, max_salary INTO job_min_sal, job_max_sal
            FROM jobs
            WHERE job_id = :new.job_id;

        -- Call the check_salary procedure
        check_salary(:new.job_id, :new.salary);
        END;
           
        """

        cursor.execute(sql_procedure)
        print("Trigger created successfully!")

    except cx_Oracle.Error as error:
        print(f"Error creating procedure: {error}")
    finally:
        if connection:
            connection.close()
            

if __name__ == "__main__":
    create_employee_hire_sp()
    
