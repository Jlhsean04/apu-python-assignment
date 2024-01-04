import datetime
import time

# JASON LEE HWAN SEAN
# TP071888
# LIM CHAO JIE
# TP072960

min_balance_savings = 100
min_balance_current = 500

userFilePath = "user.txt"
adminFilePath = "admin.txt"
transactionFilePath = "transaction.txt"
currentUser = []

def MainP():
    print("\n" + "=" * 70)
    print("\t" * 2, "Welcome to Rich Bank!")
    print('Which Action Would You Like to Perform?')
    print('1. Welcome!!')
    main = input('Enter the Action:  ')
    if main == '1':
        MainMenu()
    else:
        print('Please Select Available Action')
        return MainP()
    print("=" * 70)


def MainMenu():
    print("\n" + ("=" * 30) + " Rich Bank Main Menu " + ("=" * 29))
    print("\n" + ("=" * 30) + " login As " + ("=" * 29))
    print('1. User')
    print('2. Admin')
    print('3. Super User')
    print('4. Exit')
    choice = input('Enter the selection:   ')
    if choice == '1':
        CusLog()
    elif choice == '2':
        AdminLog()
    elif choice == '3':
        SuperLog()
    elif choice == '4':
        MainP()
    else:
        print('Please Select an Available Action')


def CusLog():
    name = input('Enter User Name:  ')
    acc = input('Enter Account Number:  ')
    password = input('Enter Account Password: ')

    with open('user.txt', 'r') as file:
        lines = file.readlines()

    global currentUser
    currentUser = []

    for line in lines:
        user_info = line.strip().split(',')
        if password in line and name in line and acc in line:
            print('Login Successful')
            currentUser = user_info
            CusMenu()
            break
    else:
        print('Login Failed')

def CusMenu():
    print("\n" + ("=" * 28) + " Customer Menu " + ("=" * 28))
    print('Welcome to Rich Bank Customer Account!!')
    print('Which Action Would You Like to Perform?')
    print('1. Deposit')
    print('2. Withdraw')
    print('3. Change Account Password')
    print('4. Log Out')
    choice = input('Enter the selection:   ')
    if choice == '1':
        Deposit()
    elif choice == '2':
        Withdraw()
    elif choice == '3':
        print('Change Password')
        ChangeCusPassword()
    elif choice == '4':
        MainP()
    else:
        print('Please Select an Available Action')

def Deposit():
    print("\n" + ("=" * 31) + " Deposit Menu " + ("=" * 30))

    amount = float(input('Enter the Amount to Deposit: '))

    with open('user.txt', 'r') as file:
        all_data = file.read().splitlines()

    user_found = False

    for i in range(len(all_data)):
        current_user = all_data[i].split(',')
        if len(current_user) >= 7 and currentUser and len(currentUser) > 0 and i < len(all_data):
            if currentUser[2] == current_user[2]:
                # Update balance and write back to file
                current_user[6] = str(float(current_user[6]) + amount)
                all_data[i] = ','.join(current_user)

                # Record the deposit transaction in transaction.txt
                transaction_data = [currentUser[0], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Deposit', str(amount)]
                writeToFile(transactionFilePath, [transaction_data], append=True)

                with open('user.txt', 'w') as file:
                    file.write('\n'.join(all_data))

                print('Deposit Successful')
                user_found = True
                break

    if not user_found:
        print('User not found')


def Withdraw():
    print("\n" + ("=" * 32) + " Withdraw Menu " + ("=" * 31))

    user_id = getUserIdByUsername(currentUser[1])

    with open('user.txt', 'r') as file:
        all_data = file.read().splitlines()

    user_found = False

    for i in range(len(all_data)):
        current_user = all_data[i].split(',')

        # Check if the current_user list has at least 7 elements before accessing them
        if len(current_user) >= 7 and user_id == current_user[0]:
            amount = float(input('Enter the Amount to Withdraw: '))

            if float(current_user[6]) >= amount:
                current_user[6] = str(float(current_user[6]) - amount)
                all_data[i] = ','.join(current_user)

                # Record the withdrawal transaction in transaction.txt
                transaction_data = [user_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Withdraw',
                                    str(amount)]
                writeToFile(transactionFilePath, [transaction_data], append=True)

                with open('user.txt', 'w') as file:
                    file.write('\n'.join(all_data))

                print('Withdrawal Successful')
                user_found = True
                break
            else:
                print('Insufficient balance')
                user_found = True
                break

    if not user_found:
        print('User not found')


def ChangeCusPassword():
    global currentUser
    name = currentUser[1]
    acc = currentUser[2]
    password = input('Enter Current Password: ')
    new_password = input('Enter New Password: ')
    print(currentUser)
    with open('user.txt', 'r') as file:
        lines = file.readlines()

    found_user = False

    with open('user.txt', 'w') as file:
        for line in lines:
            user_info = line.strip().split(',')
            print(f"Checking: {user_info}")
            if len(user_info) >= 5 and name == user_info[1] and acc == user_info[2] and password == user_info[0]:
                print('Password Change Successful')
                user_info[0] = new_password
                currentUser[0] = new_password
                found_user = True
            file.write(','.join(user_info) + '\n')

    if not found_user:
        print('Invalid current password. Password not changed.')

    CusMenu()


def AdminLog():
    name = input('Enter User Name: ')
    acc = input('Enter Account Number: ')
    password = input('Enter Account Password: ')

    with open('admin.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        if acc in line and password in line and name in line:
            print('Login Successful')
            account_type = line [-2].strip()

            if account_type == 'A':
                AdminMenu()
            else:
                print('Invalid Account Type for Admin Login')


def AdminMenu():
    print("\n" + ("=" * 29) + " Admin Menu " + ("=" * 29))
    print('Welcome to Rich Bank Admin Account!!')
    print('1. Create New Customer Account')
    print('2. Generate Customer Statement ')
    print('3. Edit Customer Details')
    print('4. Log Out')
    choice = input('Enter the selection:   ')
    if choice == '1':
        CreateNewCus()
    elif choice == '2':
        print('Print Customer Statement')
        CusStatement()
    elif choice == '3':
        print('Edit Customer Details')
        EditCusDetail()
    elif choice == '4':
        MainP()
    else:
        print('Please Select Available Action')


def CreateNewCus():
    print("\n" + ("=" * 29) + " New Customer Menu " + ("=" * 26))

    createFile(userFilePath)

    while True:
        current_time = str(datetime.datetime.now())
        acc_num = current_time.replace('-', '').replace(':', '').replace('.', '').replace(' ', '')
        current_datetime = datetime.datetime.now()
        formatted_date = current_datetime.strftime('%A %d %B %Y %H:%M:%S')
        stripped_date = formatted_date.replace(' ', '').replace(':', '')
        acc_pass = ''.join(sorted(stripped_date))

        with open('user.txt', 'r') as file:
            all_data = file.read()

        name = input('Enter Your Name:  ')
        gender = input('Enter Your Gender (male / female):  ')
        phone_number = input('Enter Your Phone Number:  ')
        account_type = input('Enter Your Account Type (savings / current):  ')

        if account_type == 'savings':
            saving_amount = float(input('Enter Your Initial Saving Amount (minimum RM100):  '))
            if saving_amount < 100:
                print('Minimum saving amount for savings account is RM100.')
                return CreateNewCus()
        elif account_type == 'current':
            saving_amount = float(input('Enter Your Initial Saving Amount (minimum RM500):  '))
            if saving_amount < 500:
                print('Minimum saving amount for current account is RM500.')
                return CreateNewCus()
        else:
            print('Invalid Account Type')
            return CreateNewCus()

        if name in all_data:
            print('Name Already Exists')
            return CreateNewCus()
        elif any(char.isdigit() for char in name):
            print('User Name Cannot Contain Numbers')
            return CreateNewCus()
        elif gender != 'male' and gender != 'female':
            print('Invalid Gender')
            return CreateNewCus()
        elif not phone_number.isdigit():
            print('Phone Number Cannot Contain Alphabets')
            return CreateNewCus()
        elif len(phone_number) != 10:
            print('Invalid Phone Number')
            return CreateNewCus()
        elif phone_number in all_data:
            print('Phone Number Already Exists')
            return CreateNewCus()
        else:
            acc_data = [acc_pass, name, acc_num, gender, phone_number, account_type, str(saving_amount)]

            # Save the customer details into user.txt
            with open('user.txt', 'a') as file:
                file.write(','.join(acc_data) + '\n')

            print(f'Your Account Numbers are {acc_num} and Account Password is {acc_pass}')
            return acc_data

def CusStatement(user_id=None):
    while True:
        if user_id is None:
            acc = input("Enter Account Number: ")
            password = input("Enter Account Password: ")
        else:
            acc = user_id
            password = "dummy_password"  # Provide a dummy password as it's not needed in this case

        data = readfile(userFilePath)
        transactionData = readfile(transactionFilePath)

        user_found = False
        for i in data:
            if len(i) >= 3 and acc == i[2] and password == i[0]:
                user_found = True
                header = ["Password", "Username", "User ID", "Gender", "Phone Number", "Account Type", "Balance"]
                createTable(i[1] + " detail", [i], header, 7)

                start_date = input("Enter Start Date (dd-mm-yyyy): ")
                end_date = input("Enter End Date (dd-mm-yyyy): ")

                try:
                    datetime.datetime.strptime(start_date, '%d-%m-%Y')
                    datetime.datetime.strptime(end_date, '%d-%m-%Y')
                except ValueError:
                    print("Invalid date format. Please use dd-mm-yyyy.")
                    break

                print("Transaction History:")
                header = ["Date", "Type", "Amount"]


                user_transaction_data = [
                    [j[1], j[2], j[3]] for j in transactionData if
                    j[0] == i[0] and start_date <= j[1].split()[0] <= end_date
                ]

                createTable(i[1] + " transaction history", user_transaction_data, header, 3)

                total_deposit = sum(
                    float(j[2]) for j in user_transaction_data if j[1] == "Deposit"
                )
                total_withdraw = sum(
                    float(j[2]) for j in user_transaction_data if j[1] == "Withdraw"
                )

                current_balance = float(i[6])

                print("\nSummary:")
                print("Total Deposit : RM", total_deposit)
                print("Total Withdraw: RM", total_withdraw)
                print("Current Balance: RM", current_balance)

                break

        if not user_found:
            print("Invalid credentials or user not found!")
            time.sleep(1)

        break


def EditCusDetail():
    acc_num = input("Enter the account number of the user to edit: ")

    data = readfile(userFilePath)
    user_found = False

    for i in range(len(data)):
        if acc_num == data[i][2]:
            user_found = True
            print("Current User Details:")
            header = ["User ID", "Username", "Gender", "Phone Number", "Account Type", "Balance"]
            createTable(data[i][1] + " detail", [data[i]], header, 6)

            new_name = input("Enter new name (Leave empty to keep the current name): ")
            if ValidateNoInput(new_name):
                data[i][1] = new_name

            new_gender = input("Enter new gender (Leave empty to keep the current gender): ")
            if ValidateNoInput(new_gender):
                data[i][3] = new_gender

            new_phone_number = input("Enter new phone number (Leave empty to keep the current phone number): ")
            if ValidateNoInput(new_phone_number) and new_phone_number.isdigit():
                data[i][4] = new_phone_number

            new_account_type = input("Enter new account type (Leave empty to keep the current account type): ")
            if ValidateNoInput(new_account_type):
                data[i][5] = new_account_type

            updateFile(userFilePath, acc_num, data[i])
            print("User details updated successfully!")
            time.sleep(1)
            break

    if not user_found:
        print("User not found!")
        time.sleep(1)


def SuperLog():
    super_user_name = "super"
    super_user_password = "123456"

    print("Super User Login")
    name_input = input("Enter User Name: ")
    password_input = input("Enter Password: ")

    if name_input == super_user_name and password_input == super_user_password:
        print("Login Successful")
        SuperMenu()
    else:
        print("Invalid Super User Credentials")


def SuperMenu():
    print("\n" + ("=" * 29) + " Super User Account Menu" + ("=" * 29))
    print('Welcome to Rich Bank Super User Account!!')
    print('Which Action Would You Like to Perform?')
    print('1. Create New Admin Account')
    print('2. View All Admin')
    print('3. Log Out')
    choice = input('Enter the Action:   ')
    if choice == '1':
        CreateNewAdmin()
    if choice == '2':
        ViewAllAdmin()
    if choice == '3':
        MainP()

def CreateNewAdmin():
    print("\n" + "=" * 29 + " New Admin Register Menu" + "=" * 26)

    createFile(adminFilePath)

    while True:
        new_admin_name = input("Enter new admin username: ")
        new_admin_password = input("Enter new admin password: ")
        confirm_password = input("Confirm new admin password: ")

        if ValidateNoInput(new_admin_name) and ValidateNoInput(new_admin_password) and validatePassword(
                new_admin_password, confirm_password):
            admin_id = generateUserId("admin")
            new_admin_data = [admin_id, new_admin_name, new_admin_password, "A"]
            writeToFile(adminFilePath, [new_admin_data])
            print("New admin account created successfully!")
            time.sleep(1)
            break
        else:
            print("Invalid input or password mismatch. Please try again.")
            time.sleep(1)


def ViewAllAdmin():
    admin_data = readfile(adminFilePath)

    if not admin_data:
        print("No admin data available.")
        return

    header = ["Admin ID", "Username", "Password", "Account Type"]
    createTable("All Admin Data", admin_data, header, 4)


def _exit():
    print("\n" + "=" * 69)
    print("\n", "\t", "Well Done! :)")
    print("\n", "\t", "Thank you for using this system. Have a nice day! :)")
    print("=" * 69)


def createFile(filePath):
    try:
        with open(filePath, "x"):
            pass
    except FileExistsError:
        pass


def writeToFile(filePath, data, append=False):
    createFile(filePath)

    with open(filePath, "a" if append else "w") as file:
        for i in data:
            line = ",".join(map(str, i))
            file.write(line + "\n")


def readfile(file_path):
    with open(file_path, 'r') as file:
        data = [line.strip().split(',') for line in file]
    return data


def updateFile(filePath, id, data):
    with open(filePath, "r") as file:
        lines = file.readlines()

    with open(filePath, "w") as file:
        for line in lines:
            if line.split("\t")[0] == id:
                line = "\t".join(map(str, data)) + "\n"
            file.write(line)


def ValidateIc(text):
    if text.isdigit() == False:
        print("=" * 13 + " Invalid input. Input must not include text. " + "=" * 12)
        return
    if len(text) != 12:
        print("=" * 9 + " Invalid input. Input must be 12 digit without '-'. " + "=" * 9)
        return
    return True


def ValidateChoice(input, max):
    if input.isdigit() and int(input) <= max:
        return True
    else:
        return False


def ValidateNoInput(input):
    if input == "":
        print("Input cannot be empty!!")
        time.sleep(1)
        return False
    return True


def ValidateUserName(username, userType):
    if userType == "admin":
        data = readfile(adminFilePath)
    else:
        data = readfile(userFilePath)

    for row in data:
        if username == row[1]:
            print("Username already exists! Please try again.")
            time.sleep(1)
            return False
    return True


def validatePassword(password, confirmPassword):
    if password == confirmPassword:
        return True
    else:
        print("Password does not match!")
        time.sleep(1)
        return False


def createTable(title, data, header, columnNum):
    clear_line = '\n' + '=' * (columnNum * 25)

    colWidth = 25

    print(clear_line)
    print("|", end="")
    print(title.center(columnNum * colWidth - 4), end="")
    print("|")
    print("=" * columnNum * colWidth)
    print("|", end="")
    for i in header:
        print(i.center(colWidth - 2), end="|")
    print()
    print("-" * columnNum * colWidth)
    for i in data:
        print("|", end="")
        for j in i:
            print(j.center(colWidth - 2), end="|")
        print()
    print("=" * columnNum * colWidth)


def generateUserId(userType):
    print(userType)
    if userType == "admin":
        data = readfile(adminFilePath)
    else:
        data = readfile(userFilePath)

    print(len(data),1)

    if len(data) == 0:
        return "Ad001"
    else:
        lastUserId = data[-1][0].split('\t')
        lastUserId = lastUserId[0]
        if lastUserId[2:].isdigit():
            number = int(lastUserId[2:]) + 1
        else:
            number = 1
        newUserId = f"Ad{number:03d}"
        return newUserId


def getUserIdByUsername(username):
    data = readfile(userFilePath)

    for i in data:
        # Check if the list has at least 2 elements before accessing index 1
        if len(i) >= 2 and username == i[1]:
            return i[0]

    # If the loop completes without returning, the username was not found
    return None


def manageUser():
    while True:
        createTable("Manage User", readfile(userFilePath),
                    ["Account Number", "Username", "IC Number", "Email", "Password", "Account Type", "Balance"], 7)
        print("\n1. Edit User Detail")
        print("2. Generate User Report")
        print("0. Exit\n")
        choice = input("Enter your choice: ")
        if ValidateChoice(choice, 2):
            if choice == "1":
                EditCusDetail()
            elif choice == "2":
                GenerateReport()
            else:
                break
        else:
            print("Invalid input!")
            input("Press Enter to continue...")

def GenerateReport():
    while True:
        createTable("View User Financial Report", readfile(userFilePath),
                    ["User ID", "Username", "Password", "Account Type", "Balance"], 5)

        userId = input("Enter user ID (0 to exit): ")
        if userId == "0":
            break

        # Call the CusStatement function for the specified user ID
        CusStatement(userId)

        input("Press Enter to continue...")
        break

def viewTransactionHistory(userId):
    data = readfile(userFilePath)
    if len(data) == 0:
        print("No user found!")
        input("Press Enter to continue...")
    else:
        for i in data:
            if userId == i[0]:
                header = ["User ID", "Username", "Password", "Account Type", "Balance"]
                createTable(i[1] + " detail", [i], header, 5)

                print("Please specify a time period")
                start = input("Start Date(dd-mm-yyyy):")
                end = input("End Date(dd-mm-yyyy):")

                try:
                    intstart = int(start.replace("-", ""))
                    intend = int(end.replace("-", ""))
                    datetime.datetime.strptime(start, '%d-%m-%Y')
                    datetime.datetime.strptime(end, '%d-%m-%Y')
                except:
                    print("Invalid date format!")
                    input("Press Enter to continue...")
                    break

                transactionData = readfile(transactionFilePath)
                filteredTransactionData = []
                for j in transactionData:
                    if userId == j[0]:
                        date = j[1].split(" ")[0]
                        intdate = int(date.replace("/", ""))
                        if intdate >= intstart and intdate <= intend:
                            filteredTransactionData.append(j)
                if len(filteredTransactionData) == 0:
                    print("No transaction found!")
                    input("Press Enter to continue...")
                    break
                else:
                    header = ["User ID", "Date", "Type", "Amount"]
                    createTable(i[1] + " transaction history", filteredTransactionData, header, 4)
                    totalDeposit = 0
                    totalWithdraw = 0
                    for j in filteredTransactionData:
                        if j[2] == "Deposit":
                            totalDeposit += float(j[3])
                        else:
                            totalWithdraw += float(j[3])
                    print("Total deposit : RM" + str(totalDeposit))
                    print("Total withdraw: RM" + str(totalWithdraw))
                    print("Balance       : RM" + str(float(i[6])))
                    input("Press Enter to continue...")
                break
        else:
            print("User not found!")
            input("Press Enter to continue...")


MainP()