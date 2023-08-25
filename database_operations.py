import mysql.connector
from mysql.connector import errorcode
from rich.prompt import Prompt
import re
import sys
from tabulate import tabulate


config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "contacts",
}


def manage_db(config):
    global db
    try:
        db = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                db = mysql.connector.connect(
                    **{key: value for key, value in config.items() if key != "database"}
                )
                cursor = db.cursor()
                cursor.execute(f'CREATE DATABASE IF NOT EXISTS {config["database"]};')
                db.commit()
                cursor.close()
            except mysql.connector.Error as create_err:
                sys.exit(f"An error occurred while creating the 'contacts' database: {create_err}")
        else:
            sys.exit(f"Error {err}")
    finally:
        if "db" in locals() and db.is_connected():
            ...


def create_table(config):
    cursor = db.cursor()
    cursor.execute(f"USE {config['database']};")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_data(
            name TEXT,
            phone TEXT,
            category TEXT 
        );            
        """
    )
    db.commit()
    cursor.close()


def check_table_empty():
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM user_data")
    try:
        return cursor.fetchone()
    finally:
        cursor.close()


def check_name_exist(name: str):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM user_data WHERE name = '{name}'")
    try:
        return cursor.fetchall()
    finally:
        cursor.close()


# Needs to run
manage_db(config)
create_table(config)


def add_contacts():
    cursor = db.cursor()
    cursor.execute(f"USE {config['database']};")
    db.commit()
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
    phone_number = Prompt.ask("Phone Number", default="0000000000").strip()
    if re.search(r"^[0-9\s\-()]+$", phone_number):
        ...
    else:
        sys.exit("Invalid Phone Number,Try Again Later!")
    print("")
    category = Prompt.ask("Category", default="Friend").strip().title()
    if re.search(r"^[A-Za-z]+$", category):
        ...
    else:
        sys.exit("Invalid Category,Try Again Later!")
    print("")

    phone_number = f"{country_code} {phone_number}"

    cursor.execute(
        f"""
    INSERT INTO user_data (name, phone,category)
    VALUES ('{name}','{phone_number}','{category}'); 
   """
    )
    print("Contact Added")
    print("")
    db.commit()
    cursor.close()


def remove_contacts():
    cursor = db.cursor()
    print("")
    name = input("Name (to remove): ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+", name):
        if check_table_empty() is None:
            print("Table is Currently Empty")
            print("")

        elif check_name_exist(name) == []:
            print("Name You Wanted to Delete, Does Not Exist in the first place")
            print("")

        else:
            cursor.execute(f"DELETE FROM user_data WHERE name = '{name}'")
            db.commit()
            cursor.close()

            print("Entered Name Deleted Successfully!")
            print("")
    else:
        sys.exit("Invalid Name,Try Again Later!")


def search_contacts():
    cursor = db.cursor()
    print("")
    name = input("Name (to search for): ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+", name):
        cursor.execute(f'SELECT * FROM user_data WHERE name = "{name}"')
        result_name = cursor.fetchall()

        if check_table_empty() is None:
            print("Table is Currently Empty")
            cursor.close()

        elif result_name == []:
            print("Name You Wanted to Search, Does Not Exist in the first place")
            cursor.close()

        else:
            print("")
            print(
                tabulate(
                    {
                        "Name": [result_name[0][0]],
                        "Phone Number": [result_name[0][1]],
                        "Category": [result_name[0][-1]],
                    },
                    headers="keys",
                    tablefmt="grid",
                    colalign=("center",),
                )
            )
            print("")
            cursor.close()

    else:
        sys.exit("Invalid Name,Try Again Later!")


def update_number():
    cursor = db.cursor()
    print("")
    name = input("Name (to update for): ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+", name):
        if check_table_empty() is None:
            print("Table is Currently Empty")
            print("")
            cursor.close()

        elif check_name_exist(name) == []:
            print("Name You Wanted to Update, Does Not Exist in the first place")
            print("")
            cursor.close()

        else:
            print("")
            country_code = Prompt.ask("Country Code", default="+971").strip()
            if re.search(r"^\+?(\d+)", country_code):
                ...
            else:
                sys.exit("Invalid Country Code,Try Again Later!")
            print("")
            phone_number = Prompt.ask("Phone Number", default="0000000000").strip()
            if re.search(r"^[0-9\s\-()]+$", phone_number):
                ...
            else:
                sys.exit("Invalid Phone Number,Try Again Later!")

            phone_number = f"{country_code} {phone_number}"

            cursor.execute(
                f'UPDATE user_data SET phone = "{phone_number}" WHERE name = "{name}";'
            )
            print("Update Executed")
            print("")
            db.commit()
            cursor.close()


def show_all():
    cursor = db.cursor()
    name = []
    phone = []
    category = []

    if check_table_empty() is None:
        print("")
        print("Table is Currently Empty,Nothing to Display")
        print("")

    else:
        cursor.execute("SELECT * FROM user_data;")
        name, phone, category = zip(*cursor.fetchall())
        print("")
        print(
            tabulate(
                {"Name": name, "Phone Number": phone, "Category": category},
                headers="keys",
                tablefmt="grid",
                colalign=("center",),
            )
        )
        print("")
        cursor.close()


if __name__ == "__main__":
    add_contacts()
    remove_contacts()
    search_contacts()
    update_number()
    show_all()
