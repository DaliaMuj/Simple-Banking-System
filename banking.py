import random
import sys
import luhn as luhn
import database

card_number = ""
connection = database.connect()
database.create_table(connection)


def display_first_menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def display_second_menu():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")


def implement_options(a):
    if a == 1:
        display_balance()
    elif a == 2:
        add_income()
    elif a == 3:
        transfer()
    elif a == 4:
        close_account()
    elif a == 5:
        logout()
    elif a == 0:
        exit_program()


def display_balance():
    print("Balance: " + database.return_balance(connection, card_number))


def add_income():
    print("Enter income:")
    database.add_income(connection, int(input()), card_number)
    print("Income was added!")


def transfer():
    print("Transfer")
    print("Enter card number:")
    card_number2 = input()
    if card_number == card_number2:
        print("You can't transfer money to the same account")
    elif not luhn.verify(card_number2):
        print("Probably you made a mistake in the card number. Please try again!")
    elif not database.existing_number(connection, card_number2):
        print("Such a card does not exist.")
    else:
        print("Enter how much money you want to transfer:")
        money = input()
        if int(money) <= database.return_balance(connection, card_number):
            print("Success!")
            database.transfer_income(connection, money, card_number)
            database.add_income(connection, money, card_number2)
        else:
            print("Not enough money!")


def close_account():
    database.delete_account(connection, card_number)
    print("The account has been closed!")


def logout():
    print("You have successfully logged out!")


def exit_program():
    print("Bye!")
    sys.exit()


def account_options():
    while True:
        display_second_menu()
        implement_options(int(input()))


def second_option():
    global card_number
    print("Enter your card number:")
    if database.existing_number(connection, card_number := input()):
        print("Enter your PIN:")
        if database.existing_pin(connection, card_number, input()):
            print("You have successfully logged in!")
            account_options()
        else:
            print("Wrong card number or PIN!")
    else:
        print("Wrong card number or PIN!")


def first_option():
    global card_number
    print("Your card has been created")
    print("Your card number:")
    card_number = luhn.append("400000" + str(random.randint(10 ** 8, 10 ** 9)))
    print(card_number)
    print("Your card PIN:")
    pin = str(random.randint(1000, 9999))
    print(pin)
    database.insert_table(connection, card_number, pin)


def choice(a):
    if a == 1:
        first_option()
    elif a == 2:
        second_option()
    elif a == 0:
        exit_program()


while True:
    display_first_menu()
    choice(int(input()))
