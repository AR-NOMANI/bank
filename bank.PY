from datetime import datetime

#          PREDEFINED USERS 
accounts = [
    {
        "acc_no": "1001",
        "name": "Ali",
        "type": "S",
        "balance": 5000,
        "pin": "1234",
        "cnic": "52201-6552840-1",
        "email": "ali1223@gmail.com",
        "date of birth": "12-3-1999",
        "cheque_book": False,
        "atm_card": False,
        "locked": False,
        "attempts": 0
    },
    {
        "acc_no": "1002",
        "name": "Ahmed",
        "type": "C",
        "balance": 10000,
        "pin": "5678",
        "cnic": "52201-6552840-2",
        "email": "ahmed1223@gmail.com",
        "date of birth": "12-12-1987",
        "cheque_book": False,
        "atm_card": False,
        "locked": False,
        "attempts": 0
    }
]

transactions = []

def find_account(acc_no):
    for acc in accounts:
        if acc["acc_no"] == acc_no:
            return acc
    return None

def log(acc_no, t_type, amount, balance):
    time = datetime.now().strftime("%d/%m/%Y %H:%M")
    transactions.append({
        "acc_no": acc_no,
        "time": time,
        "type": t_type,
        "amount": amount,
        "balance": balance
    })

# ---------------- Login ----------------

def login():
    acc_no = input("Account Number: ")
    acc = find_account(acc_no)

    if not acc:
        print("Account not found.")
        return

    if acc["locked"]:
        print("Account is locked due to 3 wrong attempts.")
        return

    pin = input("PIN: ")

    if acc["pin"] == pin:
        acc["attempts"] = 0
        print(f"\nWelcome {acc['name']}!")
        user_menu(acc)
    else:
        acc["attempts"] += 1
        print("Wrong PIN!")
        if acc["attempts"] >= 3:
            acc["locked"] = True
            print("Account Locked due to 3 wrong attempts.")

# ---------------- User Menu ----------------

def user_menu(acc):
    while True:
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. ATM Withdraw")
        print("4. Transfer")
        print("5. Balance")
        print("6. History")
        print("7. Profile")
        print("8. Change PIN")
        print("9. Cheque Book")
        print("10. ATM Card")
        print("11. Logout")

        choice = input("Enter your choice: ")

        # ---------------- Deposit ----------------
        if choice == "1":
            try:
                amount = int(input("Deposit Amount: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                acc["balance"] += amount
                log(acc["acc_no"], "Deposit", amount, acc["balance"])
                print("Deposit Successful")
            except ValueError:
                print("Invalid input! Please enter a number.")

        # ---------------- Withdraw ----------------
        elif choice == "2":
            try:
                amount = int(input("Withdraw Amount: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                minimum = 500 if acc["type"] == "S" else 1000
                if acc["balance"] - amount < minimum:
                    print("Minimum balance rule violated")
                else:
                    acc["balance"] -= amount
                    log(acc["acc_no"], "Withdraw", amount, acc["balance"])
                    print("Withdraw Successful")
            except ValueError:
                print("Invalid input! Please enter a number.")

        # ---------------- ATM Withdraw ----------------
        elif choice == "3":
            if not acc["atm_card"]:
                print("You must request an ATM card first.")
                continue
            atm_pin = input("Enter PIN for ATM Transaction: ")
            if atm_pin != acc["pin"]:
                print("Incorrect PIN! ATM Transaction Cancelled.")
                continue
            try:
                amount = int(input("ATM Withdraw Amount (Max 10000): "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                if amount > 10000:
                    print("ATM Limit Exceeded (Max 10000)")
                    continue
                minimum = 500 if acc["type"] == "S" else 1000
                if acc["balance"] - amount < minimum:
                    print("Insufficient Balance")
                else:
                    acc["balance"] -= amount
                    log(acc["acc_no"], "ATM Withdraw", amount, acc["balance"])
                    print("ATM Withdraw Successful")
            except ValueError:
                print("Invalid input! Please enter a number.")

        # ---------------- Transfer ----------------
        elif choice == "4":
            receiver_no = input("Receiver Account: ")
            if receiver_no == acc["acc_no"]:
                print("Cannot transfer to same account")
                continue
            receiver = find_account(receiver_no)
            if not receiver:
                print("Receiver not found")
                continue
            try:
                amount = int(input("Amount: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                minimum = 500 if acc["type"] == "S" else 1000
                if acc["balance"] - amount < minimum:
                    print("Transfer failed due to minimum balance rule")
                else:
                    acc["balance"] -= amount
                    receiver["balance"] += amount
                    log(acc["acc_no"], f"Transfer to {receiver_no}", amount, acc["balance"])
                    log(receiver_no, f"Received from {acc['acc_no']}", amount, receiver["balance"])
                    print("Transfer Successful")
            except ValueError:
                print("Invalid input! Please enter a number.")

        # ---------------- Balance ----------------
        elif choice == "5":
            print("Balance:", acc["balance"])

        # ---------------- History ----------------
        elif choice == "6":
            print("\nTransaction History:")
            found = False
            for t in transactions:
                if t["acc_no"] == acc["acc_no"]:
                    print(f"{t['time']} | {t['type']} | {t['amount']} | Balance: {t['balance']}")
                    found = True
            if not found:
                print("No transactions yet.")

        # ---------------- Profile ----------------
        elif choice == "7":
            print("\n--- Profile ---")
            print("Name:", acc["name"])
            print("Account No:", acc["acc_no"])
            print("CNIC:", acc["cnic"])
            print("Email:", acc["email"])
            print("Account Type:", acc["type"])

        # ---------------- Change PIN ----------------
        elif choice == "8":
            old_pin = input("Enter Old PIN: ")
            if old_pin == acc["pin"]:
                new_pin = input("Enter New 4-digit PIN: ")
                if len(new_pin) == 4 and new_pin.isdigit():
                    acc["pin"] = new_pin
                    print("PIN Changed Successfully")
                else:
                    print("PIN must be 4 digits")
            else:
                print("Wrong Old PIN")

        # ---------------- Cheque Book ----------------
        elif choice == "9":
            if acc["type"] == "C":
                acc["cheque_book"] = True
                print("Cheque Book Request Approved!")
            else:
                print("Only Current Account can request Cheque Book.")

        # ---------------- ATM Card ----------------
        elif choice == "10":
            acc["atm_card"] = True
            print("ATM Card Request Approved!")

        elif choice == "11":
            print("Logged out.")
            break

        else:
            print("Invalid Choice")


while True:
    print("\n1. Login  2. Exit")
    ch = input("Choice: ")
    if ch == "1":
        login()
    elif ch == "2":
        print("Thank you for using the banking system.")
        break
    else:
        print("Invalid Choice")