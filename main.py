from database_operations import close_server,add_contacts,remove_contacts,search_contacts,update_number,show_all,country_code
import pyfiglet
from tabulate import tabulate
import sys
import os


def display_options():
    print(pyfiglet.figlet_format("PyContacts",font = "big"))
    options = ["[A/a]","[R/r]","[S/s]","[U/u]","[SA/sa]","[CC/cc]","[CLS/cls]","[Q/q]"]
    actions = ["Add Contacts","Remove Contacts","Search Contacts","Update Contacts","Show All Contacts","Country Code Count","Clear Terminal","Exit"]
    print("")
    print(tabulate({"Options":options,"Actions": actions}, headers="keys",tablefmt="grid",colalign=("center",)))
    print("")


def verify_options():
    while True:
        action = input("Desired Action: ").strip().upper()
        if action == "A":
            add_contacts()
        elif action == "R":
            remove_contacts()
        elif action == "S":
            search_contacts()
        elif action == "U":
            update_number()
        elif action == "SA":
            show_all()
        elif action == "CC":
            country_code()
        elif action == "Q":
            print("")
            print("See you Again Later :)")
            close_server()
            sys.exit("")
        elif action == "CLS":
            os.system("cls")
            display_options()

        else:
            print("")
            print("Invalid Action,Try Again!")
            print("")
            
        
def main():
    display_options()
    verify_options()


if __name__ == '__main__':
    main()

