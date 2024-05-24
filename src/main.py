from database_operations import close_server,add_contacts,remove_contacts,search_contacts,update_number,show_all
from tabulate import tabulate
import sys
import os


#For Styling Purpose
import pyfiglet
from colorama import Fore, Style, init
init()

def print_magenta_gradient(text):
    ascii_art = pyfiglet.figlet_format(text, font="doom")
    neon_shades = [
        '\033[95m',  
        '\033[96m', 
        '\033[94m', 
        '\033[95m',  
        '\033[96m',  
    ]
    lines = ascii_art.split('\n')

    for i, line in enumerate(lines):
        color = neon_shades[i % len(neon_shades)]  
        print(color + line + Style.RESET_ALL)


def display_options():
    print_magenta_gradient("PyContacts")
    options = ["[A/a]","[R/r]","[S/s]","[U/u]","[SA/sa]","[CLS/cls]","[Q/q]"]
    actions = ["Add Contacts","Remove Contacts","Search Contacts","Update Contacts","Show All Contacts","Clear Terminal","Exit"]
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
    print_magenta_gradient()

if __name__ == '__main__':
    main()

