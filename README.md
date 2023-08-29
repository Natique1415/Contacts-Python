# Contacts (in Python)
* Creating a **Command Line Interface** to simulate a contact app.


## Libraries
* [MySQL](https://www.mysql.com/)
* [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
* [Rich](https://rich.readthedocs.io/en/stable/introduction.html)


## Limitations  
* It is based on the command line (so yeah)
* Provides basic features for contact manipulation.
* Little Scope for error checking or verifying the numbers or country code given to it.


## Future Improvements
* Provide the user with more flexibility with their contacts app. (Kindly suggest, If you have something in mind)
* Provide a powerful **GUI-like app** (maybe using Tkinter)
* Reduce LOC (lines of code).


## Update 1 (24/08/2023)
* The code now makes the required **database** and the **tables**.
* Error checking for creating the above-given parameters has also been added.


## Update 2 (24/08/2023)
* Added **check_table_empty()** and **check_name_exist(name: str)** to shorten the code.
* **show_all()** will first check if the table is **empty** before unpacking the variables (to avoid unpacking errors).


## Update 3 (29/08/2023)
* Added **close_server** function to close the SQL server when the user chooses to quit the application.
