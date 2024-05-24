import mysql.connector
from rich.prompt import Prompt
import re
import sys
from tabulate import tabulate


# Change parameters according to your database
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
    CREATE TABLE IF NOT EXISTS user_data(
        name TEXT,
        phone VARCHAR(15),
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
    if not re.search(r"\b([A-ZÀ-ÿ][\w\s',.-]*[A-Za-zÀ-ÿ])\b", name):
        sys.exit("Invalid Name,Try Again Later!")
    print("")


    country_code = Prompt.ask("Country Code", default="+971").strip()
    if not re.search(r"^\+(\d{1,3})$", country_code):
        sys.exit("Invalid Country Code,Try Again Later!")        
    print("")

    phone_number = Prompt.ask("Phone Number", default="0000000000").strip()
    if not re.search(r"^\d{10}$", phone_number):
        sys.exit("Invalid Phone Number,Try Again Later!")
    print("")

    category = Prompt.ask("Category", default="Friend").strip().title()
    if not re.search(r"^[A-Za-z]+$", category):
        sys.exit("Invalid Category,Try Again Later!")
    print("")

    full_phone_number = f"{country_code} {phone_number}".strip()
    if len(full_phone_number) > 15:  
        sys.exit("Combined phone number too long. Please adhere to the format.")

    try:
        cursor.execute(
            f"""
        INSERT INTO user_data (name, phone,category)
        VALUES ('{name}','{full_phone_number}','{category}'); 
        """
        )
        print("Contact Added")
        print("")
        db.commit()
        cursor.close()
    
    except mysql.connector.Error as err:
        print("Failed to insert data.")


def remove_contacts():
    print("")
    name = input("Name (to remove): ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][\w\s',.-]*[A-Za-zÀ-ÿ])\b", name):
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
    if re.search(r"\b([A-ZÀ-ÿ][\w\s',.-]*[A-Za-zÀ-ÿ])\b", name):
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
                        "Phone Number": [result[0][1]],
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
    if re.search(r"\b([A-ZÀ-ÿ][\w\s',.-]*[A-Za-zÀ-ÿ])\b", name):
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
            if re.search(r"^\+(\d{1,4})$", country_code):
                ...
            else:
                sys.exit("Invalid Country Code,Try Again Later!")
            print("")

            phone_number = Prompt.ask("Phone Number", default="0000000000").strip()
            if re.search(r"^\d{10}$", phone_number):
                ...
            else:
                sys.exit("Invalid Phone Number,Try Again Later!")


            # Phone number
            phone_number = f"{country_code} {phone_number}"
            
            cursor = db.cursor()
            cursor.execute(
                f'UPDATE user_data SET phone = "{phone_number}" WHERE name = "{name}";'
            )
            db.commit()
            cursor.close()
            print("Update Executed")
            print("")
    else:
        print("")
        sys.exit("Invalid Name,Try Again Later!")


def show_all():
    cursor = db.cursor()
    cursor.execute("SELECT name, phone, category FROM user_data")  # Explicitly specify columns
    result = cursor.fetchall()
    cursor.close()

    if result == []:
        print("Table is Currently Empty, Nothing to Display")
    else:
        name, phone, category = zip(*result)
        print(
            tabulate(
                {"Name": name, "Phone Number": phone, "Category": category},
                headers="keys",
                tablefmt="grid",
                colalign=("center",),
            )
        )


def close_server():
    db.close()

if __name__ == "__main__":
    add_contacts()
    remove_contacts()
    search_contacts()
    update_number()
    show_all()
