import sqlite3

c = sqlite3.connect("card.s3db")


def connect():
    return c.cursor()


def create_table(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER IDENTITY PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
    c.commit()


def insert_table(conn, number, pin):
    conn.execute("INSERT INTO card (number, pin) VALUES (?, ?);", (number, pin))
    c.commit()


def return_balance(conn, card_number):
    conn.execute("SELECT balance FROM card WHERE (?) LIKE number", (card_number,))
    c.commit()
    r = conn.fetchone()[0]
    return r


def add_income(conn, income, card_number):
    conn.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (income, card_number))
    c.commit()


def transfer_income(conn, income, card_number):
    conn.execute("UPDATE card SET balance = balance - ? WHERE number = ?", (income, card_number))
    c.commit()


def existing_number(conn, card_number):
    conn.execute("SELECT COUNT(*) FROM card WHERE number LIKE (?)", (card_number, ))
    val = conn.fetchone()[0]
    if val == 1:
        return True
    return False


def existing_pin(conn, card_number, pin):
    conn.execute("SELECT COUNT(*) FROM card WHERE number LIKE (?) AND pin LIKE (?)", (card_number, pin))
    val = conn.fetchone()[0]
    if val == 1:
        return True
    return False


def delete_account(conn, card_number):
    conn.execute("DELETE FROM card WHERE number LIKE ?", (card_number,))
    c.commit()
