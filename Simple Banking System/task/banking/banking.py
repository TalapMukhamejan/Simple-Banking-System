from random import randint
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
# cur.execute('''CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)''')


card = {}
counter = 0

def action():
    print("""1. Create an account
2. Log into account
0. Exit""")
    number = int(input())
    if number == 1:
        create_account()
    elif number == 2:
        log_in()
    elif number == 0:
        print("Bye!")
        exit()


def create_account():
    str_card_number = list(str(400000) + str(randint(100000000, 1000000000)))
    card_number = [int(i) for i in str_card_number]
    for x in range(0, 15, 2):
        card_number[x] = card_number[x] * 2
    for x in range(15):
        if card_number[x] > 9:
            card_number[x] = card_number[x] - 9
    num = sum(card_number)
    for x in range(10):
        if (num + x) % 10 == 0:
            str_card_number.append(x)
            card_number = [str(i) for i in str_card_number]
            card_number = int(''.join(card_number))

    pin = randint(1000, 10000)
    if card_number in card:
        create_account()
    card[card_number] = pin
    global counter
    cur.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (counter, card_number, pin, 0))
    counter += 1
    cur.execute(f"SELECT number FROM card WHERE number = {card_number}")
    data = str(cur.fetchone())
    data = data.translate(str.maketrans('', '', '\'(,)'))
    print(f"Your card number: \n{int(data)}")
    cur.execute(f"SELECT pin FROM card WHERE pin = {pin}")
    data = str(cur.fetchone())
    data = data.translate(str.maketrans('', '', '\'(,)'))
    print(f"Your card PIN: \n{int(data)}")
    conn.commit()
    action()


def log_in():
    card_n = int(input("Enter your card number:"))
    pin_ = int(input("Enter your PIN:"))
    if card_n in card:
        if card[card_n] == pin_:
            print("You have successfully logged in!")
            profile(card_n)
    print("Wrong card number or PIN!")
    action()


def add_income(card_n):
    bal = int(input("Enter income:"))
    cur.execute(f"SELECT balance FROM card WHERE number = {card_n}")
    balance = str(cur.fetchone())
    balance = balance.translate(str.maketrans('', '', '\'(,)'))
    cur.execute(f"UPDATE card SET balance = {int(balance) + bal} WHERE number = {card_n}")
    conn.commit()
    profile(card_n)

def check(card_n, trans_card):
    if str(trans_card).startswith("400000"):
        str_card_number = list(str(trans_card)[:-1])
        card_num = [int(i) for i in str_card_number]
        for x in range(0, 15, 2):
            card_num[x] = card_num[x] * 2
        for x in range(15):
            if card_num[x] > 9:
                card_num[x] = card_num[x] - 9
        num = sum(card_num)
        for x in range(10):
            if (num + x) % 10 == 0:
                str_card_number.append(x)
                card_num = [str(i) for i in str_card_number]
                card_num = int(''.join(card_num))
        return card_num
    return None
def do_transer(card_n):
    trans_card_number = int(input("Enter card number:"))
    cur.execute(f"SELECT balance FROM card WHERE number = {card_n}")
    balance = str(cur.fetchone())
    balance = int(balance.translate(str.maketrans('', '', '\'(,)')))
    cur.execute(f"SELECT number FROM card WHERE number = {trans_card_number}")
    db_check = str(cur.fetchone())
    db_check = db_check.translate(str.maketrans('', '', '\'(,)'))
    check_ = check(card_n, trans_card_number)
    if trans_card_number == check_:
        income = int(input("Enter income:"))
        if balance < income:
            print("Not enough money!")
            profile(card_n)
        else:
            print("Success!")
            cur.execute(f"SELECT balance FROM card WHERE number = {trans_card_number}")
            trans_balance = str(cur.fetchone())
            trans_balance = int(trans_balance.translate(str.maketrans('', '', '\'(,)')))
            cur.execute(f"UPDATE card SET balance = {trans_balance + income} WHERE number = {trans_card_number}")
            cur.execute(f"UPDATE card SET balance = {balance - income} WHERE number = {card_n}")
            conn.commit()
            profile(card_n)
    else:
        if db_check == None or check_ == None:
            print("Such a card does not exist.")
        elif card_n == trans_card_number:
            print("You can't transfer money to the same account!")
        else:
            print("Probably you made a mistake in the card number. Please try again!")
        do_transer(card_n)

def profile(card_n):
    print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
    number = int(input())
    if number == 1:
        cur.execute(f"SELECT balance FROM card WHERE number = {card_n}")
        data = str(cur.fetchone())
        data = data.translate(str.maketrans('', '', '(\',)'))
        print(f"Balance: {data}")
        profile(card_n)
    elif number == 2:
        add_income(card_n)
    elif number == 3:
        do_transer(card_n)
    elif number == 4:
        print("The account has been closed!")
        cur.execute(f"DELETE FROM card WHERE number = {card_n}")
        conn.commit()
        return
    elif number == 5:
        print("You have successfully logged out!")
        action()
    elif number == 0:
        print("Bye!")
        exit()


action()
cur.close()
conn.close()
# Write your code here
