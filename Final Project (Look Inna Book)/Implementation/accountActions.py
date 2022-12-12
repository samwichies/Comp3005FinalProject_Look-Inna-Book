import shopStore
import useCart

#Handle users logging in
def login(connection, loggedIn, privileges, username, cartNumber):
    loggingIn = True
    while (loggingIn):
        username = input("Username: ")
        password = input("Password: ")
        cursor = connection.cursor()
        cursor.execute("SELECT username, userPrivileges FROM BOOKSTORE_USER WHERE username = ? and userPassword = ?", (username, password,))
        currentUser = cursor.fetchall()
        if(currentUser):
            if(currentUser[0][1] == True):
                privileges = True
            loggedIn = True
            print("Welcome back " + currentUser[0][0] + "!\n")
            cursor = connection.cursor()
            cursor.execute("UPDATE BOOKSTORE_CART SET username = ? WHERE cartNumber = ?", (username, cartNumber))
            loggingIn = False
        else:
            isLoggingIn = ""
            while (isLoggingIn != "y" and isLoggingIn != "n"):
                isLoggingIn = input("Invaild credentials, would you like to try again? (y/n): ")
                print()
            if(isLoggingIn == "n"):
                loggingIn = False
                username = ""
    return loggedIn, privileges, username

#Handle new user registering
def register(connection, loggedIn, username):
    creatingAccount = True
    print("Make new account:")
    while creatingAccount:
        username = input("Username: ")
        password = input("Password: ")
        if(username == "" or username == " " or password == "" or password == " "):
            print("Invalid username or password\n")
            continue
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BOOKSTORE_USER WHERE username = ? and userPassword = ?", (username, password,))
        currentUser = cursor.fetchall()
        if(currentUser):
            tryingUsernames = ""
            while (tryingUsernames != "y" and tryingUsernames != "n"):
                tryingUsernames = input("Username is taken, would you like to try again? (y/n): ")
                if(tryingUsernames == "n"):
                    creatingAccount = False
                    username = ""
        else:
            billing = input("Billing information: ")
            shipping = input("Shipping information: ")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO BOOKSTORE_USER(username, userPassword, billingInformation, shippingInformation, userPrivileges) VALUES(?, ?, ?, ?, ?)", (username, password, billing, shipping, False))
            print("Welcome " + username + "!\n")
            loggedIn = True
            creatingAccount = False
    return loggedIn, username

#Handle a user logging out 
def logout(connection, username, hasCart, cartNumber, loggedIn, privileges):
    username = ""
    loggedIn = False
    shopStore.deleteCart(connection, cartNumber)
    shopStore.deleteCartContains(connection, cartNumber)
    hasCart = False
    cartNumber = 0
    privileges = False
    hasCart, cartNumber = useCart.getCart(connection, hasCart, cartNumber, loggedIn, username)
    print("You are now logged out\n")
    return username, hasCart, cartNumber, loggedIn, privileges