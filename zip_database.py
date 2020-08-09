import os
import sqlite3
import datetime

DATABASE_FILE = "zip_code.db"


def create_db():
    """
    Creates the database if it doesn't already exist in the current directory.
    """
    if not os.path.isfile(DATABASE_FILE):
        conn = sqlite3.connect(DATABASE_FILE)

        zip_cursor = conn.cursor()
        zip_cursor.execute("""CREATE TABLE zip_codes (
            zip_code text,
            message text,
            created time
            )""")
        conn.commit()

        conn.close()
        print("Created the {} database file.".format(DATABASE_FILE))


def is_valid_zipcode(user_zip_code):
    """
    Returns True if the zip_code is valid.
    """
    return len(str(user_zip_code)) == 5 or type(
        user_zip_code) == int or int(user_zip_code) >= 0


def get_zip_code():
    """
    Returns the user inputted zip code.
    """
    prompt = "What is your ZIP code (no extension)? " + \
             "If you want to exit, enter 00000. "
    user_zip_code = input(prompt)
    if int(user_zip_code) == 0:
        exit()
    elif not is_valid_zipcode(user_zip_code):
        while not is_valid_zipcode(user_zip_code):
            user_zip_code = input(
                "That is an invalid ZIP code. Please try again. ")
    return user_zip_code


def chat_menu(user_zip_code):
    """
    Gathers the user's selection in the chat menu.
    """
    selection = input(
        "Welcome to the " +
        user_zip_code +
        " chat room! Please select an option:\n " +
        "Enter 1 to write a message.\n " +
        "Enter 2 to see the last 20 messages.\n " +
        "Enter 3 to exit to the ZIP code menu.\n ")
    selection = int(selection)
    if selection < 1 or selection > 3:
        while not(type(selection) != int or selection < 1 or selection > 3):
            selection = input("Your selection is invalid. Please try again. ")
    elif selection == 1:
        chat(user_zip_code)
    elif selection == 2:
        message_list(user_zip_code)
    elif selection == 3:
        main_menu()


def chat(user_zip_code):
    """
    Gathers the user's message and records it in the database.
    """
    user_message = input(
        "If you want to exit, enter '*~Y~*'. Otherwise, please enter your message here: ")
    if user_message == "*~Y~*":
        chat_menu(user_zip_code)
    now = datetime.datetime.now()
    conn = sqlite3.connect(DATABASE_FILE)
    with conn:
        zip_cursor = conn.cursor()
        zip_cursor.execute("INSERT INTO zip_codes VALUES (:zip_code, :message, :created)", {
                           "zip_code": user_zip_code, "message": user_message, "created": now})
    response_message = input(
        "Would you like to enter another message (enter yes or no)? ")
    if response_message.lower() == "yes":
        chat(user_zip_code)
    elif response_message.lower() == "no":
        chat_menu(user_zip_code)
    else:
        while response_message.lower() not in ["yes", "no"]:
            response_message = input("Please enter a valid answer: ")


def message_list(user_zip_code):
    """
    Prints a list of the last 20 messages the user sends.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    with conn:
        zip_cursor = conn.cursor()
        zip_cursor.execute(
            "SELECT message, created FROM zip_codes WHERE zip_code=:zip_code ORDER BY created DESC LIMIT 20", {
                "zip_code": user_zip_code})
        messages = list(reversed(zip_cursor.fetchall()))
        if len(messages) == 0:
            print("There aren't any messages for this zip code.")
        else:
            print(
                "Here are your messages from the " +
                user_zip_code)
            for message in messages:
                print(message)

    chat_menu(user_zip_code)


def main_menu():
    create_db()
    zip_code = get_zip_code()
    chat_menu(zip_code)


main_menu()