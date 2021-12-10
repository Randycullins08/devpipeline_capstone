import sqlite3
import csv
from datetime import date
import bcrypt
from getpass import getpass

connection = sqlite3.connect('competency.db')
cursor = connection.cursor()

# def new_database(cursor):
#     with open('competency.sql') as sql_file:
#         sql_as_string = sql_file.read()
#         cursor.executescript(sql_as_string)
#     connection.commit()
#     print("This worked")

# new_database(cursor)

class CompetencyTracking:
    def __init__(self, cursor, email, password):
        self.cursor = cursor
        self.email = email
        self.__password = None
        self.hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.matched = bcrypt.checkpw(password, self.hashed)

class User(CompetencyTracking):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def view_user_info(self):
        view_info = "SELECT first_name, last_name, phone, email, hire_date FROM Users"

        rows = cursor.execute(view_info,).fetchall()
        print()
        print(f"{'First Name':<12}{'Last Name':<12}{'Phone':<14}{'Email Address':<25}{'Hire Date'}\n")
        for row in rows:
            print(f"{row[0]:<12}{row[1]:<12}{row[2]:<14}{row[3]:<25}{row[4]}")
        print()

    def print_user(self):
        view_info = "SELECT first_name, last_name, phone, email, hire_date FROM Users WHERE email = ?"
        rows = cursor.execute(view_info, (self.email,)).fetchall()
        print()
        print(f"{'First Name':<12}{'Last Name':<12}{'Phone':<14}{'Email Address':<26}{'Hire Date'}")
        print('-'*73)
        for row in rows:
            print(f"{row[0]:<12}{row[1]:<12}{row[2]:<14}{row[3]:<25}{row[4]}")
        print()

    def user_competencies(self):
        competency_table = "SELECT * FROM Competencies"
        rows = cursor.execute(competency_table).fetchall()
        print()
        print(f"{'Competency ID':<16}{'Name':<20}{'Description':<35}{'Date Created':>12}")
        print("-" * 83)
        for row in rows:
            print(f"{row[0]:<16}{row[1]:<20}{row[2]:<35}{row[3]:>12}")
        print()
        comp_selection = input("Enter Competency ID: ")
        join_sql = """
        SELECT co.name, u.first_name, u.last_name, ca.score, ca.date_taken
        FROM Users u
        INNER JOIN Competency_Assessment_Results ca
            ON ca.user_id = u.user_id
        INNER JOIN Assessments a
            ON a.assessment_id = ca.user_id
        INNER JOIN Competencies co
            ON ca.competency_id = co.competency_id
        WHERE ca.active = 1 AND co.competency_id = ? AND u.email = ?"""
        values = (comp_selection, self.email)
        rows = cursor.execute(join_sql, values).fetchall()
        print()
        print(f"{'Competency':<20}{'First Name':<14}{'Last Name':<12}{'Score':<7}{'Date Taken'}")
        print('-'*63)
        for row in rows:
            print(f"{row[0]:<20}{row[1]:<14}{row[2]:<16}{row[3]:<3}{row[4]:<10}")
        print()


    def update_user_info(self):
        self.print_user()
        update_input = input("""
What would you like to update? 
(1) - First Name
(2) - Last name
(3) - Phone
(4) - Email Address
(5) - Password
(6) - Go Back
""")
        update_email = "UPDATE Users SET email = ? WHERE email = ?"
        update_password = "UPDATE Users SET password = ? WHERE email = ?"
        update_first_name = "UPDATE Users SET first_name = ? WHERE email = ?"
        update_last_name = "UPDATE Users SET last_name = ? WHERE email = ?"
        update_phone = "UPDATE Users SET Phone = ? WHERE email = ?"
        
        if update_input == '1':
            name = input("Enter New First Name: ").title()
            cursor.execute(update_first_name, (name, self.email))
            connection.commit()
            self.print_user()
        if update_input == '2':
            name = input("Enter New Last Name: ").title()
            cursor.execute(update_last_name, (name, self.email))
            connection.commit()
            self.print_user()
        if update_input == '3':
            phone = input("Enter New Phone Number(555-555-5555): ")
            cursor.execute(update_phone, (phone, self.email))
            connection.commit()
            self.print_user()
        if update_input == '4':
            new_email = input("Enter New Email Address: ")
            cursor.execute(update_email, (new_email, self.email))
            connection.commit()
            self.print_user(new_email)
        if update_input == '5':
            new_password = getpass("Enter New Password: ")
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(update_password, hashed)
            connection.commit()
            self.print_user()
        if update_input == '6':
            print("Good Bye!")
            return user_menu(self.email)

class Manager(CompetencyTracking):
    def __init__(self,name):
        self.name = name

    def view_users_list(self):
        view_info = "SELECT user_id, first_name, last_name, phone, email, hire_date FROM Users"
        users_list = []
        rows = cursor.execute(view_info,).fetchall()
        for row in rows:
            users_list.append(row)
        print(users_list)

    def view_user_info(self):
        view_info = "SELECT user_id, first_name, last_name, phone, email, hire_date FROM Users"
        rows = cursor.execute(view_info,).fetchall()
        print()
        print(f"{'User ID':<9}{'First Name':<12}{'Last Name':<12}{'Phone':<14}{'Email Address':<25}{'Hire Date'}")
        print("-" * 82)
        for row in rows:
            print(f"{row[0]:<9}{row[1]:<12}{row[2]:<12}{row[3]:<14}{row[4]:<25}{row[5]}")
        print()
        

    def search_user(self):
        last_name_view = "SELECT first_name, last_name, phone, email, hire_date FROM Users WHERE last_name = ?"
        last_name_input = input("Enter Last Name: ").title()
        rows = cursor.execute(last_name_view, (last_name_input,)).fetchall()
        print()
        print(f"{'First Name':<12}{'Last Name':<12}{'Phone':<14}{'Email Address':<25}{'Hire Date'}")
        print("-" * 73)
        for row in rows:
            print(f"{row[0]:<12}{row[1]:<12}{row[2]:<14}{row[3]:<25}{row[4]}")
        print()

    def add_user(self):
        first_name = input("Enter First Name: ").title()
        last_name = input("Enter Last Name: ").title()
        phone = input("Enter Phone Number: ")
        email = input("Enter Email Address: ")
        password = "password"
        hire_date = input("Enter Hire Date: ")
        date_created = date.today()
        print(f"{first_name} {last_name} was added")

        values = (first_name, last_name, phone, email, password, hire_date, date_created)

        enter_user_into_database = """
        INSERT INTO Users(first_name, last_name, phone, email, password, hire_date, date_created)
        Values (?,?,?,?,?,?,?)
        """
        cursor.execute(enter_user_into_database, values)
        connection.commit()

    def view_competencies(self):
        competency_table = "SELECT * FROM Competencies"
        rows = cursor.execute(competency_table).fetchall()
        print()
        print(f"{'Competency ID':<16}{'Name':<20}{'Description':<35}{'Date Created':>12}")
        print("-" * 83)
        for row in rows:
            print(f"{row[0]:<16}{row[1]:<20}{row[2]:<35}{row[3]:>12}")
        print()

    def view_assessments(self):
        assessment_table = "SELECT * FROM Assessments"
        rows = cursor.execute(assessment_table).fetchall()
        print()
        print(f"{'Assessment ID':<15}{'Name':<25}{'Description'}")
        print('-'*77)
        for row in rows:
            print(f"{row[0]:<15}{row[2]:<25}{row[3]}")
        print()
    
    def add_competencies(self):
        self.view_competencies()
        name = input("Enter Name of New Competency: ").title()
        description = input("Enter Description of Competency: ")
        date_created = date.today()
        add_competency = """
        INSERT INTO Competencies(name, description, date_created)
        VALUES (?,?,?)"""
        values = (name, description, date_created)
        cursor.execute(add_competency, values)
        connection.commit()
        self.view_competencies()

    def add_assessment(self):
        self.view_assessments()
        name = input("Enter Name of New Assessment: ").title()
        description = input("Enter Description of Assessment: ")
        competency_id = input("Enter Competency ID That Matches Your New Assessment: ")
        add_assessment = """
        INSERT INTO Assessments(competency_id, name, description)
        Values(?,?,?)"""
        values = (competency_id, name, description)
        cursor.execute(add_assessment, values)
        connection.commit()
        self.view_assessments()

    def add_assessment_results(self):
        add_results = """
        INSERT INTO Competency_Assessment_Results(user_id, competency_id, assessment_id, score, date_taken)
        VALUES (?,?,?,?,?)"""
        user_id = input("Enter User ID: ")
        competency_id = input("Enter Competency ID: ")
        assessment_id = input("Enter Assessment ID: ")
        score = input("Enter Score: ")
        date_taken = input("Enter Date Assessment Was Taken (yyyy-mm-dd): ")
        values = (user_id, competency_id,assessment_id, score, date_taken)
        cursor.execute(add_results, values)
        connection.commit()
        print("Results have been added!")

    def edit_user(self):
        self.view_user_info()
        update_input = input("""
What would you like to update? 
(1) - First Name
(2) - Last name
(3) - Phone
(4) - Email Address
(5) - Change Password
(6) - Make User Manager
(7) - Back To Menu
""")
        update_email = "UPDATE Users SET email = ? WHERE user_id = ?"
        update_first_name = "UPDATE Users SET first_name = ? WHERE user_id = ?"
        update_last_name = "UPDATE Users SET last_name = ? WHERE user_id = ?"
        update_phone = "UPDATE Users SET Phone = ? WHERE user_id = ?"
        update_user_type = "UPDATE Users SET user_type = ? WHERE user_id = ?"
        update_password = "UPDATE Users SET password = ? WHERE user_id = ?"
        if update_input == '1':
            user_id_input = input("Enter User Id: ")
            name = input("Enter New First Name: ").title()
            cursor.execute(update_first_name, (name, user_id_input))
            connection.commit()
            self.view_user_info()
            print("User has been updated")
        if update_input == '2':
            user_id_input = input("Enter User Id: ")
            name = input("Enter New Last Name: ").title()
            cursor.execute(update_last_name, (name, user_id_input))
            connection.commit()
            self.view_user_info()
            print("User has been updated")
        if update_input == '3':
            user_id_input = input("Enter User Id: ")
            phone = input("Enter New Phone Number(555-555-5555): ")
            cursor.execute(update_phone, (phone, user_id_input))
            connection.commit()
            self.view_user_info()
            print("User has been updated")
        if update_input == '4':
            user_id_input = input("Enter User Id: ")
            new_email = input("Enter New Email Address: ")
            cursor.execute(update_email, (new_email, user_id_input))
            connection.commit()
            self.view_user_info()
            print("User has been updated")
        if update_input == '5':
            user_id_input = input("Enter User Id: ")
            email = input("Enter Users Email Address: ")
            check_password = getpass("Enter Old Password: ")
            check_sql = cursor.execute("SELECT password FROM Users WHERE email = ?", (email,)).fetchone()
            if check_password == 'password':
                new_password = getpass("Enter New Password: ")
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(update_password, (hashed, user_id_input))
                connection.commit()
                print()
                print("Password Was Changed")
            elif check_sql[0] == bcrypt.hashpw(check_password.encode('utf-8'), check_sql[0]):
                new_password = getpass(input("Enter New Password: "))
                cursor.execute(update_password, (new_password, user_id_input))
                connection.commit()
                print()
                print("Password Was Changed")
        if update_input == '6':
            user_id_input = input("Enter User Id: ")
            user_type = input("Enter (1) To Change User To Manager: ")
            cursor.execute(update_user_type, (user_type, user_id_input))
            connection.commit()
            self.view_user_info()
        if update_input == '7':
            print("Going Back")
            return manager_menu()

    def edit_competency(self):
        self.view_competencies()
        update_name = "UPDATE Competencies SET name = ? WHERE competency_id = ?"
        update_description = "UPDATE Competencies SET description = ? WHERE competency_id = ?"
        update_date_created = "UPDATE Competencies SET date_created = ? WHERE competency_id = ?"
        update_input = input("""
What would you like to update? 
(1) - Name
(2) - Description
(3) - Date Created
(4) - Go Back
""")    
        if update_input == '1':
            competency_id_input = input("Enter Competency ID To Update: ")
            name = input("Enter New Name: ").title()
            cursor.execute(update_name, (name, competency_id_input))
            connection.commit()
            self.view_competencies()
        if update_input == '2':
            competency_id_input = input("Enter Competency ID To Update: ")
            description = input("Enter New Description: ").title()
            cursor.execute(update_description, (description, competency_id_input))
            connection.commit()
            self.view_competencies()
        if update_input == '3':
            competency_id_input = input("Enter Competency ID To Update: ")
            date_created = input("Enter New Date Created: ")
            cursor.execute(update_date_created, (date_created, competency_id_input))
            connection.commit()
            self.view_competencies()
        if update_input == '4':
            print("Going Back")
            return manager_menu()

    def edit_assessment(self):
        self.view_assessments()
        update_name = "UPDATE Assessments SET name = ? WHERE assessment_id = ?"
        update_description = "UPDATE Assessments SET description = ? WHERE assessment_id = ?"
        update_input = input("""
What would you like to update? 
(1) - Name
(2) - Description
(3) - Go Back
""")
        if update_input == '1':
            assessment_id_input = input("Enter Assessment ID To Update: ")
            name = input("Enter New Name: ").title()
            cursor.execute(update_name, (name, assessment_id_input))
            connection.commit()
            self.view_assessments()
        if update_input == '2':
            assessment_id_input = input("Enter Assessment ID To Update: ")
            description = input("Enter New Description: ").title()
            cursor.execute(update_description, (description, assessment_id_input))
            connection.commit()
            self.view_assessments()
        if update_input == '3':
            print("Going Back")
            return manager_menu()
    
    def user_assessments(self):
        print("\nWhich User Would You Like To View?")
        print()
        self.view_user_info()
        print()
        join_sql = """
        SELECT u.first_name, u.last_name,  a.name, ca.score, ca.date_taken
        FROM Users u
        INNER JOIN Competency_Assessment_Results ca
            ON ca.user_id = u.user_id
        INNER JOIN Assessments a
            ON a.assessment_id = ca.user_id
        WHERE u.user_id = ?"""
        user_id_input = input("Enter User ID: ")
        rows = cursor.execute(join_sql, (user_id_input,)).fetchall()
        user_assessments_taken = []
        for row in rows:
            for i in row:
                user_assessments_taken.append(i)
        print(user_assessments_taken)

    def view_assessment_results(self):
        join_sql = """
        SELECT result_id, u.last_name, co.name, a.name, ca.score, ca.date_taken
        FROM Users u
        INNER JOIN Competency_Assessment_Results ca
            ON ca.user_id = u.user_id
        INNER JOIN Assessments a
            ON ca.assessment_id = a.assessment_id
        INNER JOIN Competencies co
            ON ca.competency_id = co.competency_id
        WHERE ca.active = 1"""
        rows = cursor.execute(join_sql).fetchall()
        print()
        print(f"{'Result ID':<11}{'Users Last Name':<19}{'Competency':<20}{'Assessment':<25}{'Score':<7}{'Date Taken'}")
        print('-'*92)
        for row in rows:
            print(f"{row[0]:<11}{row[1]:<19}{row[2]:<20}{row[3]:<29}{row[4]:<3}{row[5]}")
        print()

    def edit_assessment_results(self):
        menu_input = input("""
Are You Sure You Want To Update Assessment Results?
(1) - Yes
(2) - Go back       
""")
        if menu_input == '1':
            self.view_assessment_results()
            update_score = "UPDATE Competency_Assessment_Results SET score = ?, date_taken = ? WHERE result_id = ?"
            result_id_input = input("Enter Result ID To Update Assessment Results: ")
            new_score_input = input("Enter New Score: ")
            date_taken_input = input("Enter New Date Taken(yyyy-mm-dd): ")
            values = (new_score_input, date_taken_input, result_id_input)
            cursor.execute(update_score, values)
            connection.commit()
            self.view_assessment_results()
        if menu_input == '2':
            print("Going Back")
            return manager_menu()

    def delete_assessment_results(self):
        menu_input = input("""
Are You Sure You Want To Delete Assessment Results?
(1) - Yes
(2) - Go back       
""")
        if menu_input == '1':
            self.view_assessment_results()
            deactivate_assessment = "UPDATE Competency_Assessment_Results SET active = 0 WHERE result_id = ?"
            result_id_input = input("Enter Result ID To Delete: ")
            cursor.execute(deactivate_assessment, result_id_input)
            connection.commit()
            self.view_assessment_results()
        if menu_input == '2':
            print("Going Back")
            return manager_menu()

    def user_competency_report(self):
        self.view_competencies()
        comp_selection = input("Enter Competency ID: ")
        self.view_user_info()
        user_selction = input("Enter User ID: ")
        join_sql = """
        SELECT co.name, u.first_name, u.last_name, ca.score, ca.date_taken
        FROM Users u
        INNER JOIN Competency_Assessment_Results ca
            ON ca.user_id = u.user_id
        INNER JOIN Assessments a
            ON a.assessment_id = ca.user_id
        INNER JOIN Competencies co
            ON ca.competency_id = co.competency_id
        WHERE ca.active = 1 AND co.competency_id = ? AND u.user_id = ?"""
        values = (comp_selection, user_selction)
        rows = cursor.execute(join_sql, values).fetchall()
        print()
        print(f"{'Competency':<20}{'First Name':<14}{'Last Name':<12}{'Score':<7}{'Date Taken'}")
        print('-'*63)
        for row in rows:
            print(f"{row[0]:<20}{row[1]:<14}{row[2]:<16}{row[3]:<3}{row[4]:<10}")
        print()

    def competency_report(self):
        self.view_competencies()
        comp_selection = input("Enter Competency ID: ")
        join_sql = """
        SELECT co.name, u.first_name, u.last_name, ca.score, ca.date_taken
        FROM Users u
        INNER JOIN Competency_Assessment_Results ca
            ON ca.user_id = u.user_id
        INNER JOIN Assessments a
            ON a.assessment_id = ca.user_id
        INNER JOIN Competencies co
            ON ca.competency_id = co.competency_id
        WHERE ca.active = 1 AND co.competency_id = ?"""
        values = (comp_selection)
        rows = cursor.execute(join_sql, (values,)).fetchall()
        print()
        print(f"{'Competency':<20}{'First Name':<14}{'Last Name':<12}{'Score':<7}{'Date Taken'}")
        print('-'*63)
        for row in rows:
            print(f"{row[0]:<20}{row[1]:<14}{row[2]:<16}{row[3]:<3}{row[4]:<10}")
        print()

    def competency_report_m_users(self):
        # fields = ["Competency", "First Name", "Last Name", "Score", "Date Taken"]
        self.view_competencies()
        comp_selection = input("Enter Competency ID: ")
        join_sql = """
        SELECT co.name, u.first_name, u.last_name, ca.score, ca.date_taken
        FROM Users u
        INNER JOIN Competency_Assessment_Results ca
            ON ca.user_id = u.user_id
        INNER JOIN Assessments a
            ON a.assessment_id = ca.user_id
        INNER JOIN Competencies co
            ON ca.competency_id = co.competency_id
        WHERE ca.active = 1 AND co.competency_id = ?"""
        values = (comp_selection)
        csv_rows = cursor.execute(join_sql, (values,)).fetchall()
        rows = []
        for row in csv_rows:
            rows.append(row)
        with open('competency_multiple_users_report.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            # writer.writerow(fields)
            writer.writerows(rows)
        print("Report was added to 'competency_multiple_users_report.csv' file.")

    def competency_report_s_users(self):
        # fields = ["Competency", "First Name", "Last Name", "Score", "Date Taken"]
        self.view_competencies()
        comp_selection = input("Enter Competency ID: ")
        self.view_user_info()
        user_selction = input("Enter User ID: ")
        join_sql = """
        SELECT co.name, u.first_name, u.last_name, ca.score, ca.date_taken
        FROM Users u
        INNER JOIN Competency_Assessment_Results ca
            ON ca.user_id = u.user_id
        INNER JOIN Assessments a
            ON a.assessment_id = ca.user_id
        INNER JOIN Competencies co
            ON ca.competency_id = co.competency_id
        WHERE ca.active = 1 AND co.competency_id = ? AND u.user_id = ?"""
        values = (comp_selection, user_selction)
        csv_rows = cursor.execute(join_sql, values).fetchall()
        rows = []
        for row in csv_rows:
            rows.append(row)
        with open('competency_single_user_report.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            # writer.writerow(fields)
            writer.writerows(rows)
        print("Report was added to 'competency_single_user_report.csv' file.")

    def assessment_results_report(self):
        fields = ["user_id", "assessment_id", "score", "date_taken"]
        join_sql = """
        SELECT u.user_id, ca.assessment_id, ca.score, ca.date_taken
        FROM Users u
        INNER JOIN Competency_Assessment_Results ca
            ON ca.user_id = u.user_id
        INNER JOIN Assessments a
            ON ca.assessment_id = a.assessment_id
        WHERE ca.active = 1"""
        csv_rows = cursor.execute(join_sql).fetchall()
        rows = []
        for row in csv_rows:
            rows.append(row)
        with open('competency_assessment_reasults_report.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            writer.writerows(rows)
        print("Report was added to 'competency_assessment_reasults_report.csv' file.")

    def import_assessment_results_report(self):
        data_list = []
        fields = []
        with open('competency_assessment_reasults_report.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                data_list.append(row)
            print()
            print(f"{fields[0]:<9}{fields[1]:<15}{fields[2]:<7}{fields[3]}")
            print('-'*41)
            for i in data_list:
                print(f"{i[0]:<9}{i[1]:<15}{i[2]:<7}{i[3]}")
            print()

def manager_menu():
    while True:
        manager1 = Manager(cursor)
        menu = input("""
What would you like to do? 
(1) - View Users List
(2) - View Users Information
(3) - Search Single Users Information
(4) - View All Competencies
(5) - View User Results For Given Competency
(6) - View Single User Competency Level
(7) - View Assessments For User
(8) - Add Information
(9) - Edit Information
(10) - CSV Reporting
(11) - Back To Main Menu
""")
        if menu == '1':
            manager1.view_users_list()
        if menu == '2':
            manager1.view_user_info()
        if menu == '3':
            manager1.search_user()
        if menu == '4':
            manager1.view_competencies()
        if menu == '5':
            manager1.competency_report()
        if menu == '6':
            manager1.user_competency_report()
        if menu == '7':
            manager1.view_assessment_results()
        if menu == '8':
            add_input = input("""
What Would You Like To Add?
(1) - Add New User
(2) - Add New Competency        
(3) - Add New Assessment To Competency
(4) - Add Assessment Results For User For Assessment
(5) - Delete Assessment Result 
(6) - Back To Menu
""")
            while True:
                if add_input == '1':
                    manager1.add_user()
                if add_input == '2':
                    manager1.add_competencies()
                if add_input == '3':
                    manager1.add_assessment()
                if add_input == '4':
                    manager1.add_assessment_results()
                if add_input == '5':
                    manager1.delete_assessment_results()
                if add_input == '6':
                    print("Going Back To Main Menu")
                    break
        if menu == '9':
            edit_input = input("""
What Would You Like To Edit?
(1) - Edit Users Information
(2) - Edit Competency        
(3) - Edit Assessment
(4) - Edit Assessment Results
(5) - Back To Menu
""")
            while True:
                if edit_input == '1':
                    manager1.edit_user()
                if edit_input == '2':
                    manager1.edit_competency()
                if edit_input == '3':
                    manager1.edit_assessment()
                if edit_input == '4':
                    manager1.edit_assessment_results()
                if edit_input == '5':
                    print("Going Back To Main Menu")
                    break
        if menu == '10':
            csv_input = input("""
What Would You Like To Do?
(1) - Export Report
(2) - Import Report
(3) - Go Back
""")
            if csv_input == '1':
                while True:
                    export_input = input("""
Which Report Would You Like To Export?
(1) - Competency Report By Competency and Users
(2) - Competency Report For Single User
(3) - Go Back
""")
                    if export_input == '1':
                        manager1.competency_report_m_users()
                    if export_input == '2':
                        manager1.competency_report_s_users()
                    if export_input == '3':
                        print("Going Back")
                        break
            if csv_input == '2':
                while True:
                    import_input = input("""
Are You Sure You Want To Import Assessment Results?
(1) - Yes
(2) - Go Back
""")
                    if import_input == '1':
                        manager1.import_assessment_results_report()
                    if import_input == '2':
                        print("Going Back")
                        break
        if menu == '11':
            print("Exiting Program")
            quit()

def user_menu(email):
    user1 = User(cursor, email)
    while True:
        menu = input("""
What Would You Like To Do?
(1) - View User Information
(2) - Edit User Information
(3) - View Competencies 
(4) - Exit Program
""")
        if menu == '1':
            user1.print_user()
        if menu == '2':
            user1.update_user_info()
        if menu == '3':
            user1.user_competencies()
        if menu == '4':
            print("Exiting The Program")
            quit()

def main_menu(email):
    check_sql = "SELECT user_type FROM Users WHERE email = ?"
    row = cursor.execute(check_sql, (email,)).fetchone()
    if row[0] == 1:
        manager_menu()
    else:
        user_menu(email)

def register_user():
        first_name = input("Enter First Name: ").title()
        last_name = input("Enter Last Name: ").title()
        phone = input("Enter Phone Number(555-555-5555): ")
        email = input("Enter Email Address: ")
        password = getpass("Enter Password: ")
        hire_date = date.today()
        date_created = date.today()

        if not email:
            return "Missing Email!"
        if not password:
            return "Missing Password!"

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        sql = """
        INSERT INTO Users (first_name, last_name, phone, email, password, hire_date, date_created)
        VALUES (?,?,?,?,?,?,?)
        """
        values = (first_name, last_name, phone, email, hashed, hire_date, date_created)
        cursor.execute(sql, values)
        connection.commit()
        print()
        print(f"Welcome {first_name}!!!!!")
        return user_menu(email)

def login():
    email = input("Enter Email Address: ")
    password = getpass("Enter Password: ")
    check_sql = cursor.execute("SELECT password FROM Users WHERE email = ?", (email,)).fetchone()
    if check_sql[0] == 'password':
        print("Please Change Your Password!!")
    elif check_sql[0] == bcrypt.hashpw(password.encode('utf-8'), check_sql[0]):
        print("Welcome!")
    main_menu(email)

def run_program():
    print("Welcom To Dev Pipeline!")
    account = input("""
Login or Sign Up
(1) - Login
(2) - Sign Up
""")
    if account == '1':
        login()
    if account == '2':
        register_user()

run_program()