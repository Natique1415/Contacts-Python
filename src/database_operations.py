import mysql.connector
from rich.prompt import Prompt
import re
import sys
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Change parameters according to your database
config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "contacts",
}


def initialize_database():
    """Initialize the database connection and create necessary tables if they don't exist."""
    try:

        temp_config = {key: value for key, value in config.items() if key != "database"}
        db = mysql.connector.connect(**temp_config)
        cursor = db.cursor()

        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {config["database"]};')
        cursor.execute(f"USE {config['database']};")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_data(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name TEXT,
                phone VARCHAR(15),
                category TEXT 
            );            
            """
        )
        db.commit()
        cursor.close()

        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(Fore.RED + f"Database initialization error: {err}" + Style.RESET_ALL)
        sys.exit(1)


# Create the database connection
db = initialize_database()


# Validation functions
def validate_name(name):
    if not name:
        print(Fore.RED + "Name cannot be empty." + Style.RESET_ALL)
        return False

    if not re.search(r"\b([A-ZÀ-ÿ][\w\s',.-]*[A-Za-zÀ-ÿ])\b", name):
        print(
            Fore.RED
            + "Invalid name format. Name should start with a capital letter."
            + Style.RESET_ALL
        )
        return False
    return True


def validate_country_code(country_code):
    if not re.search(r"^\+(\d{1,3})$", country_code):
        print(
            Fore.RED
            + "Invalid country code. Format should be like +971."
            + Style.RESET_ALL
        )
        return False
    return True


def validate_phone_number(phone_number):
    if not re.search(r"^\d{10}$", phone_number):
        print(
            Fore.RED
            + "Invalid phone number. Must be exactly 10 digits."
            + Style.RESET_ALL
        )
        return False
    return True


def validate_category(category):
    if not re.search(r"^[A-Za-z]+$", category):
        print(
            Fore.RED
            + "Invalid category. Use only alphabetic characters."
            + Style.RESET_ALL
        )
        return False
    return True


def validate_full_phone(full_phone_number):
    if len(full_phone_number) > 15:
        print(
            Fore.RED
            + "Combined phone number too long. Max 15 characters."
            + Style.RESET_ALL
        )
        return False
    return True


def get_validated_input(
    prompt_text, validation_func, default_value=None, transform_func=None
):
    """
    Get user input with validation.

    Args:
        prompt_text (str): Text to display when prompting the user.
        validation_func (callable): Function to validate the input.
        default_value (str, optional): Default value to suggest. Defaults to None.
        transform_func (callable, optional): Function to transform input after validation. Defaults to None.

    Returns:
        str: Validated and possibly transformed input.
    """
    while True:
        if default_value:
            value = Prompt.ask(prompt_text, default=default_value).strip()
        else:
            value = input(f"{prompt_text}: ").strip()

        if transform_func:
            value = transform_func(value)

        if validation_func(value):
            return value

        print("")


def add_contacts():
    try:
        cursor = db.cursor()
        cursor.execute(f"USE {config['database']};")

        print("")

        name = get_validated_input(
            "Name", validate_name, transform_func=lambda x: x.title()
        )
        print("")

        country_code = get_validated_input(
            "Country Code", validate_country_code, default_value="+971"
        )
        print("")

        phone_number = get_validated_input(
            "Phone Number", validate_phone_number, default_value="0000000000"
        )
        print("")

        category = get_validated_input(
            "Category",
            validate_category,
            default_value="Friend",
            transform_func=lambda x: x.title(),
        )
        print("")

        full_phone_number = f"{country_code} {phone_number}".strip()
        if not validate_full_phone(full_phone_number):
            return

        try:
            cursor.execute(
                """
                INSERT INTO user_data (name, phone, category)
                VALUES (%s, %s, %s)
                """,
                (name, full_phone_number, category),
            )
            print(Fore.GREEN + "Contact Added Successfully" + Style.RESET_ALL)
            print("")
            db.commit()
        except mysql.connector.Error as err:
            print(Fore.RED + f"Failed to insert data: {err}" + Style.RESET_ALL)
        finally:
            cursor.close()

    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)


def remove_contacts():
    try:
        print("")
        name = get_validated_input(
            "Name (to remove)", validate_name, transform_func=lambda x: x.title()
        )

        cursor = db.cursor()
        cursor.execute("SELECT * FROM user_data WHERE name = %s", (name,))
        result = cursor.fetchall()

        if not result:
            print(
                Fore.YELLOW
                + "Name you wanted to delete does not exist in the database."
                + Style.RESET_ALL
            )
            print("")
            cursor.close()
            return

        cursor.execute("DELETE FROM user_data WHERE name = %s", (name,))
        db.commit()
        cursor.close()

        print(Fore.GREEN + "Entered name deleted successfully!" + Style.RESET_ALL)
        print("")

    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)


def search_contacts():
    try:
        print("")
        name = get_validated_input(
            "Name (to search for)", validate_name, transform_func=lambda x: x.title()
        )

        cursor = db.cursor()
        cursor.execute("SELECT * FROM user_data WHERE name = %s", (name,))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            print(
                Fore.YELLOW
                + "Name you wanted to search does not exist in the database."
                + Style.RESET_ALL
            )
            print("")
            return

        print("")
        print(
            tabulate(
                {
                    "Name": [result[0][1]],
                    "Phone Number": [result[0][2]],
                    "Category": [result[0][3]],
                },
                headers="keys",
                tablefmt="grid",
                colalign=("center",),
            )
        )
        print("")

    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)


def update_number():
    try:
        print("")
        name = get_validated_input(
            "Name (to update for)", validate_name, transform_func=lambda x: x.title()
        )

        cursor = db.cursor()
        cursor.execute("SELECT * FROM user_data WHERE name = %s", (name,))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            print(
                Fore.YELLOW
                + "Name you wanted to update does not exist in the database."
                + Style.RESET_ALL
            )
            print("")
            return

        print("")
        country_code = get_validated_input(
            "Country Code", validate_country_code, default_value="+971"
        )
        print("")

        phone_number = get_validated_input(
            "Phone Number", validate_phone_number, default_value="0000000000"
        )
        print("")

        full_phone_number = f"{country_code} {phone_number}".strip()
        if not validate_full_phone(full_phone_number):
            return

        cursor = db.cursor()
        cursor.execute(
            "UPDATE user_data SET phone = %s WHERE name = %s", (full_phone_number, name)
        )
        db.commit()
        cursor.close()

        print(Fore.GREEN + "Phone number updated successfully" + Style.RESET_ALL)
        print("")

    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)


def show_all():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT name, phone, category FROM user_data")
        result = cursor.fetchall()
        cursor.close()

        if not result:
            print(
                Fore.YELLOW
                + "Table is currently empty, nothing to display."
                + Style.RESET_ALL
            )
            return

        # Unpack results
        name, phone, category = zip(*result)

        print(
            tabulate(
                {"Name": name, "Phone Number": phone, "Category": category},
                headers="keys",
                tablefmt="grid",
                colalign=("center",),
            )
        )

    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)


def close_server():
    try:
        if db.is_connected():
            db.close()
            print(Fore.BLUE + "Database connection closed." + Style.RESET_ALL)
    except Exception:
        pass


if __name__ == "__main__":
    add_contacts()
    remove_contacts()
    search_contacts()
    update_number()
    show_all()
    close_server()
