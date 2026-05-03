import mysql.connector

# Step 1: Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Trinabh1543",
    database="banking"
)
cursor = conn.cursor()

#Banking app starts
#MySQL conditions were made with the help of google, because I've never used MySQL before.
#All the python code is mine


def new_account():
    account_name = input("Enter Account Name: ")
    ini_depo = float(input("Enter Initial Deposit for account: "))

    cursor.execute(
        "INSERT INTO accounts (name, balance) VALUES (%s, %s)",
        (account_name, ini_depo)
    )
    conn.commit()
    print(f"new account for {account_name}")


def money_withdraw():
    name = input("Please Enter Your Name: ")
    amount = float(input("Enter Withdrawal Amount: "))

    if amount <= 0:
        print("Enter a positive amount, please.")
        return

    cursor.execute("SELECT balance FROM accounts WHERE name = %s", (name,))
    result = cursor.fetchone()

    if result is None:
        print("The account was not found.")
        return

    balance = float(result[0])

    if amount > balance:
        print(f"Not enough funds. Balance: ${balance:.2f}, Requested: ${amount:.2f}")
        return

    cursor.execute(
        "UPDATE accounts SET balance = balance - %s WHERE name = %s",
        (amount, name)
    )

    cursor.execute(
        "INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'withdrawal', %s)",
        (name, amount)
)


    conn.commit()

    cursor.execute("SELECT balance FROM accounts WHERE name = %s", (name,))
    new_balance = cursor.fetchone()[0]

    print(f"Withdrew ${amount:.2f}. New balance: ${new_balance:.2f}")


def money_deposit():
    name = input("Please Enter Your Name: ")
    money = float(input("Enter Deposit amount: "))

    update = "UPDATE accounts SET balance = balance + %s WHERE name = %s"
    cursor.execute(update, (money, name))

    conn.commit()
    print(f"Money Deposited: ${money} to {name}")


def account_balance():
    name = input("Please Enter Your Name: ")

    cursor.execute("SELECT balance FROM accounts WHERE name = %s", (name,))
    result = cursor.fetchone()

    if result is None:
        print("The account was not found.")
        return

    current_balance = float(result[0])
    print(f"{name}, your current balance is: ${current_balance:.2f}")



def main():
    while True:
        print("1.Create A New Account")
        print("2.Withdraw Balance")
        print("3.Deposit Balance")
        print("4.Check Balance")
        print("5.Exit App")

        user = int(input("Please Enter A Number According To The List: "))

        if user == 1:
            new_account()
        
        elif user == 2:
            money_withdraw()
        
        elif user == 3:
            money_deposit()
        
        elif user == 4:
            account_balance()
        
        elif user == 5:
            print("Thank you!")
            break
        
        else:
            print("")
            print("Invalid Option, Try Again.")
            print("")


main()

cursor.close()
conn.close()
