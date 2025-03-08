from database_operations import (
    close_server,
    add_contacts,
    remove_contacts,
    search_contacts,
    update_number,
    show_all,
)
from tabulate import tabulate
import sys
import os

# For Styling Purpose
import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True)  # Auto reset colors after each print


def print_magenta_gradient(text):
    """Display stylized text header using pyfiglet and gradient colors"""
    try:
        ascii_art = pyfiglet.figlet_format(text, font="doom")
        neon_shades = [
            "\033[95m",  # Light magenta
            "\033[96m",  # Light cyan
            "\033[94m",  # Light blue
            "\033[95m",  # Light magenta
            "\033[96m",  # Light cyan
        ]
        lines = ascii_art.split("\n")

        for i, line in enumerate(lines):
            color = neon_shades[i % len(neon_shades)]
            print(color + line + Style.RESET_ALL)
    except Exception as e:
        # Fallback if pyfiglet fails
        print(Fore.MAGENTA + f"===== {text} =====" + Style.RESET_ALL)


def display_options():
    print_magenta_gradient("PyContacts")
    options = ["[A/a]", "[R/r]", "[S/s]", "[U/u]", "[SA/sa]", "[CLS/cls]", "[Q/q]"]
    actions = [
        "Add Contacts",
        "Remove Contacts",
        "Search Contacts",
        "Update Contacts",
        "Show All Contacts",
        "Clear Terminal",
        "Exit",
    ]

    print("")
    print(
        tabulate(
            {"Options": options, "Actions": actions},
            headers="keys",
            tablefmt="grid",
            colalign=("center",),
        )
    )
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
            # Cross-platform clear screen
            os.system("cls" if os.name == "nt" else "clear")
            display_options()
        else:
            print("")
            print(Fore.RED + "Invalid Action, Try Again!" + Style.RESET_ALL)
            print("")


def main():
    """Main application entry point"""
    try:
        display_options()
        verify_options()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Closing database connection...")
        close_server()
        sys.exit("\nProgram terminated.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        close_server()
        sys.exit("Program terminated due to an error.")


if __name__ == "__main__":
    main()
