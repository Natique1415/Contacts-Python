import mysql.connector
from rich.prompt import Prompt
import re
import sys
from tabulate import tabulate

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "contacts"
)
def add_contacts():
    cursor = db.cursor()
    print("")
    name = input("Name : ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+",name):
        ...
    else:
        sys.exit("Invalid Name,Try Again Later!")
    print("")   
    country_code = Prompt.ask("Country Code",default="+971").strip()
    if re.search(r"^\+?(\d+)",country_code):
        ...
    else: 
        sys.exit("Invalid Country Code,Try Again Later!")  
    print("")
    phone_number = Prompt.ask("Phone Number",default="0000000000").strip()
    if re.search(r"^[0-9\s\-()]+$",phone_number):
        ...
    else:
        sys.exit("Invalid Phone Number,Try Again Later!")   
    print("")
    category = Prompt.ask("Category",default="Friend").strip().title()
    if re.search(r"^[A-Za-z]+$",category):
        ...
    else:
        sys.exit("Invalid Category,Try Again Later!")     
    print("")

    phone_number = f'{country_code} {phone_number}'

    #Adding the data to the table
    cursor.execute(f"""
    INSERT INTO user_data (name, phone,category)
    VALUES ('{name}','{phone_number}','{category}'); 
   """)
    print("Contact Added")
    print("")
    db.commit()
    cursor.close()
    

def remove_contacts():
    cursor = db.cursor()
    print("")
    name = input("Name (to remove): ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+",name):
        cursor.execute(f"SELECT * FROM user_data")
        result_table = cursor.fetchone()


        cursor.nextset()
        cursor.execute(f"SELECT * FROM user_data WHERE name = '{name}'")
        result_name = cursor.fetchall()

        if result_table is None:
            print("Table is Currently Empty")
            print("")
            cursor.close()
            
        
        elif result_name == []:
            print("Name You Wanted to Delete, Does Not Exist in the first place")
            print("")
            cursor.close()
            

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
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+",name):
        cursor.execute(f"SELECT * FROM user_data")
        result_table = cursor.fetchone()

        cursor.nextset()

        cursor.execute(f'SELECT * FROM user_data WHERE name = "{name}"')
        result_name = cursor.fetchall()

        if result_table is None:
            print("Table is Currently Empty")
            cursor.close()
            
        
        elif result_name == []:
            print("Name You Wanted to Search, Does Not Exist in the first place")
            cursor.close()
            
        else:
            print("")
            print(tabulate({"Name":[result_name[0][0]],"Phone Number": [result_name[0][1]],"Category":[result_name[0][-1]]}, headers="keys",tablefmt="grid",colalign=("center",)))
            print("")
            cursor.close()
            
            
    else:
        sys.exit("Invalid Name,Try Again Later!")
        

def update_number():
    cursor = db.cursor()
    print("")
    name = input("Name (to update for): ").strip().title()
    if re.search(r"\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+",name):
        cursor.execute(f"SELECT * FROM user_data")
        result_table = cursor.fetchone()

        cursor.nextset()

        cursor.execute(f'SELECT * FROM user_data WHERE name = "{name}"')
        result_name = cursor.fetchall()

        if result_table is None:
            print("Table is Currently Empty")
            print("")
            cursor.close()
            
        
        elif result_name == []:
            print("Name You Wanted to Update, Does Not Exist in the first place")
            print("")
            cursor.close()
            
        else:
            print("")
            country_code = Prompt.ask("Country Code",default="+971").strip()
            if re.search(r"^\+?(\d+)",country_code):
                ...
            else: 
                sys.exit("Invalid Country Code,Try Again Later!")  
            print("")
            phone_number = Prompt.ask("Phone Number",default="0000000000").strip()
            if re.search(r"^[0-9\s\-()]+$",phone_number):
                ...
            else:
                sys.exit("Invalid Phone Number,Try Again Later!")   
            
            phone_number = f'{country_code} {phone_number}'
            
            cursor.execute(f'UPDATE user_data SET phone = "{phone_number}" WHERE name = "{name}";')
            print("Update Executed")
            print("")
            db.commit()
            cursor.close()


def show_all():
  cursor = db.cursor()
  name = []
  phone = []
  category = []

  cursor.execute("SELECT * FROM user_data;")
  name,phone,category = zip(*cursor.fetchall())
  print("")
  print(tabulate({"Name":name,"Phone Number": phone,"Category":category}, headers="keys",tablefmt="grid",colalign=("center",)))
  print("")
  cursor.close()
  

if __name__ == '__main__':
    add_contacts()
    remove_contacts()
    search_contacts()
    update_number()
    show_all()
