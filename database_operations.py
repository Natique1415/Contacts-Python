import mysql.connector
from rich.prompt import Prompt
import re
import sys
from tabulate import tabulate
import matplotlib.pyplot as plt




config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database":"contacts"
}


# Initialize Database and table
db = mysql.connector.connect(**{key: value for key, value in config.items() if key != "database"})
cursor = db.cursor()
cursor.execute(f'CREATE DATABASE IF NOT EXISTS {config["database"]};')
cursor.execute(f"USE {config['database']};")
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS code_count(
        code VARCHAR(255) PRIMARY KEY,
        count INT
    );            
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS user_data(
        name TEXT,
        code TEXT,
        phone INT,
        category TEXT 
    );            
    """
)
db.commit()
cursor.close()


def add_contacts():
    cursor = db.cursor()
    cursor.execute(f"USE contacts;")

    print("")

    name = input("Name : ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+", name):
        ...
    else:
        sys.exit("Invalid Name,Try Again Later!")
    print("")

    country_code = Prompt.ask("Country Code", default="+971").strip()
    if re.search(r"^\+?(\d+)", country_code):
        ...
    else:
        sys.exit("Invalid Country Code,Try Again Later!")
    print("")

    phone_number = input("Phone Number: ").strip()
    if re.search(r"^[0-9\s\-()]+$", phone_number) and len(phone_number) < 11:
        phone_number = int(phone_number)
    else:
        print("")
        print("Phone Length More than 11 Numbers")
        print("")
        print("OR")
        print("Invalid Phone Number")
        print("")
        sys.exit("Try Again Later!")
    print("")

    category = Prompt.ask("Category", default="Friend").strip().title()
    if re.search(r"^[A-Za-z]+$", category):
        ...
    else:
        sys.exit("Invalid Category,Try Again Later!")
    print("")

    cursor.execute(f"INSERT INTO user_data (name,code,phone,category) VALUES ('{name}','{country_code}',{phone_number},'{category}');")
    print("Contact Added")
    print("")
    db.commit()
    cursor.close()


def remove_contacts():
    print("")
    name = input("Name (to remove): ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+", name):
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM user_data WHERE name = '{name}'")
        result = cursor.fetchall()
        cursor.close()


        if result == []:
            print("Name You Wanted to Delete, Does Not Exist in the first place")
            print("")

        else:
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM user_data WHERE name = '{name}';")
            db.commit()
            cursor.close()

            print("Entered Name Deleted Successfully!")
            print("")
    else:
        print("")
        sys.exit("Invalid Name,Try Again Later!")


def search_contacts():
    print("")
    name = input("Name (to search for): ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+", name):
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM user_data WHERE name = '{name}'")
        result = cursor.fetchall()
        cursor.close()

        if result == []:
            print("Name You Wanted to Search, Does Not Exist in the first place")
            print("")

        else:
            print("")
            print(
                tabulate(
                    {
                        "Name": [result[0][0]],
                        "Country Code":[result[0][1]],
                        "Phone Number": [result[0][2]],
                        "Category": [result[0][-1]],
                    },
                    headers="keys",
                    tablefmt="grid",
                    colalign=("center",),
                )
            )
            print("")

    else:
        print("")
        sys.exit("Invalid Name,Try Again Later!")


def update_number():
    print("")
    name = input("Name (to update for): ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+", name):
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM user_data WHERE name = '{name}'")
        result = cursor.fetchall()
        cursor.close()

        if result == []:
            print("Name You Wanted to Update, Does Not Exist in the first place")
            print("")

        else:
            print("")
            country_code = Prompt.ask("Country Code", default="+971").strip()
            if re.search(r"^\+?(\d+)", country_code):
                ...
            else:
                sys.exit("Invalid Country Code,Try Again Later!")
            print("")

            phone_number = input("Phone Number: ").strip()
            if re.search(r"^[0-9\s\-()]+$", phone_number):
                phone_number = int(phone_number)
            else:
                sys.exit("Invalid Phone Number,Try Again Later!")
            print("")

            
            cursor = db.cursor()
            cursor.execute(
                f"UPDATE user_data SET code = '{country_code}' WHERE name = '{name}';"
            )
            cursor.execute(
                f"UPDATE user_data SET phone = {phone_number} WHERE name = '{name}';"
            )
            db.commit()
            cursor.close()
            print("Update Executed")
            print("")
    else:
        print("")
        sys.exit("Invalid Name,Try Again Later!")


def show_all():
    #Checking if table is empty
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM user_data")
    result = cursor.fetchall()
    cursor.close()

    if result == []:
        print("")
        print("Table is Currently Empty,Nothing to Display")
        print("")


    # Display data (if table not empty)
    else:
        name = []
        code = []
        phone = []
        category = []
        name, code,phone, category = zip(*result)
        print("")
        print(
            tabulate(
                {"Name": name, "Country Code":code,"Phone Number": phone, "Category": category},
                headers="keys",
                tablefmt="grid",
                colalign=("center",),
            )
        )
        print("")


def country_code():
    cursor = db.cursor()
    cursor.execute('''
            SELECT code, count(*) as count        
            FROM user_data
            GROUP BY code;
    ''')
    result = cursor.fetchall()
    cursor.close()
    
    code = []
    count = []
    code,count = zip(*result)
    print("")
    print(
            tabulate(
                {"Country Code": code, "Count":count},
                headers="keys",
                tablefmt="grid",
                colalign=("center",),
            )
        )
    print("")
    plt.bar(code,count)
    plt.xlabel("Country Code")
    plt.ylabel("Frequency")
    plt.title("Bar Chart Of Country Code Usage")
    plt.yticks(range(0, max(count) + 1, 1))
    plt.show()
    print("")


def country_code_table():
    cursor = db.cursor()
    cursor.execute(
    '''
            SELECT code, count(*) as count        
            FROM user_data
            GROUP BY code;
    ''')
    result = cursor.fetchall()

    for code,count in result:
        cursor.execute('''
        INSERT INTO code_count (code, count)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE count = count + %s;
    ''', (code, count, count))
    db.commit()
    cursor.close()



def close_server():
    db.close()

if __name__ == "__main__":
    add_contacts()
    remove_contacts()
    search_contacts()
    update_number()
    show_all()
    country_code()
    country_code_table()
