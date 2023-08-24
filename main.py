from database_operations import add_contacts,remove_contacts,search_contacts,update_number,show_all
from tabulate import tabulate
import sys


def display_options():
    options = ["[A/a]","[R/r]","[S/s]","[U/u]","[SA/sa]","[Q/q]"]
    actions = ["Add Contacts","Remove Contacts","Search Contacts","Update Contacts","Show All Contacts","Exit"]
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
        elif action == "Q":
            print("")
            print("Cya Again Later :)")
            sys.exit("")
        else:
            print("")
            print("Invalid Action,Try Again!")
            print("")
            
        
def main():
    display_options()
    verify_options()


if __name__ == '__main__':
    main()

