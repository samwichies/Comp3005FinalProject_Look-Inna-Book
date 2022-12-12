import os
import sqlite3
from sqlite3 import Error
import makeReport
import editBook
import viewProfile
import shopStore
import useCart
import viewOrder
import accountActions

if os.path.exists("bookstore"):
  os.remove("bookstore")

connection = sqlite3.connect('bookstore', isolation_level = None) 
cursor = connection.cursor()

bookstoreDDL = open("SQL/bookstoreDDL.sql")
bookstoreDDLString = bookstoreDDL.read()
cursor.executescript(bookstoreDDLString)

bookstoreDML = open("SQL/bookstoreDML.sql")
bookstoreDMLString = bookstoreDML.read()
cursor.executescript(bookstoreDMLString)

shopping = True
loggedIn = False
privileges = False 
hasCart = False
username = ""
cartNumber = 0

print("Welcome to Look Inna Book! :)")

hasCart, cartNumber = useCart.getCart(connection, hasCart, cartNumber, loggedIn, username)
editBook.orderBooksForStore(connection)

makeReport.createGenreView(connection)
makeReport.createAuthorView(connection)
makeReport.createPublisherView(connection)
makeReport.createSalesView(connection)

#Run main menu
while shopping:
    print("Menu:")
    print("1) Log in")
    print("2) Register")
    print("3) Browse")
    print("4) View cart")
    print("5) View orders")
    print("6) View profile")
    print("7) Log out")
    print("0) Exit")
    choice = input("Enter your selection: ")
    print()
    if(choice == "0"):
        print("Good-bye!")
        shopping = False
    elif(choice == "1"):
        if(loggedIn):
            print("You are already logged in\n")
        else:   
            print("Please log in:")
            loggedIn, privileges, username = accountActions.login(connection, loggedIn, privileges, username, cartNumber)
    elif(choice == "2"):
        if(loggedIn):
            print("You are already logged in\n")
        else:   
            loggedIn, username = accountActions.register(connection, loggedIn, username)
    elif(choice == "3"):
        shopStore.browse(connection, cartNumber)
    elif(choice == "4"):
        doesCartContain = useCart.viewCart(connection, cartNumber)
        if(doesCartContain == True):
            editingCart = ""
            while (editingCart != "y" and editingCart != "n"):
                editingCart = input("Would you like to edit your cart? (y/n): ")
                print()
            if(editingCart == "y"):
                useCart.editCart(connection, cartNumber)
                continue
            isCheckingOut = ""
            while (isCheckingOut != "y" and isCheckingOut != "n"):
                isCheckingOut = input("Would you like to check out? (y/n): ")
                print()
            if(isCheckingOut == "y"):
                if(loggedIn == False):
                    print("Please log in to continue:")
                    loggedIn, privileges, username = accountActions.login(connection, loggedIn, privileges, username, cartNumber)
                if(loggedIn == True):
                    isBuying = shopStore.purchase(connection, cartNumber, username)
                    if(isBuying == False):
                        continue
                    cardRowId = useCart.createCart(connection, 0, loggedIn, username) 
                    cursor.execute("SELECT cartNumber FROM BOOKSTORE_CART WHERE rowid = ?", (cardRowId,))
                    cart = cursor.fetchall()
                    cartNumber = cart[0][0]
    elif(choice == "5"):
        viewOrder.viewOrderList(connection, username)
    elif(choice == "6"):
        if(loggedIn):
            if(privileges):
                viewProfile.ownerProfile(connection, username)
            else:
                viewProfile.userProfile(connection, username)
        else:
            print("You are not logged in\n")    
    elif(choice == "7"):
        if(loggedIn):
            username, hasCart, cartNumber, loggedIn, privileges = accountActions.logout(connection, username, hasCart, cartNumber, loggedIn, privileges)
        else:
            print("You are not logged in\n")       
    else:
        print("Please try again :(")


