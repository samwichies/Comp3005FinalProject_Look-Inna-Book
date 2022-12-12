import makeReport
import editBook

#View a users "safe data" (not password or card/billing information)
def userProfile(connection, username):
    print("Profile:")
    cursor = connection.cursor()
    cursor.execute("SELECT username, shippingInformation FROM BOOKSTORE_USER WHERE username = ?", (username,))
    user = cursor.fetchall()
    userProfile = user[0]
    print("Username: " + userProfile[0] + ", Shipping information: " + userProfile[1] + "\n")

#View a owners "safe data" (not password or card/billing information) and lets them choice to view reports/add/remove books
def ownerProfile(connection, username):
    print("Profile:")
    cursor = connection.cursor()
    cursor.execute("SELECT username, shippingInformation FROM BOOKSTORE_USER WHERE username = ?", (username,))
    user = cursor.fetchall()
    userProfile = user[0]
    print("Username: " + userProfile[0] + ", Shipping information: " + userProfile[1] + "\n")
    exploringProfile = ""
    while (exploringProfile != "y" and exploringProfile != "n"):
        exploringProfile = input("Would you like to view reports or edit books? (y/n): ")
        print()
        if(exploringProfile == "y"):
            ownerMenu(connection)

#Menu for owners to view reports/add/remove books
def ownerMenu(connection):
    browsing = True
    while browsing:
        print("Menu:")
        print("1) Sales vs. expenditures")
        print("2) Sales per genre")
        print("3) Sales per author")
        print("4) Sales per publisher")
        print("5) Add Book")
        print("6) Remove Book")
        print("0) Exit")
        choice = input("Enter your selection: ")
        print()
        if(choice == "0"):
            browsing = False
        elif(choice == "1"):
            makeReport.salesAndExp(connection)
        elif(choice == "2"):
            makeReport.salesPerGenre(connection)
        elif(choice == "3"):
            makeReport.salesPerAuthor(connection)
        elif(choice == "4"):
            makeReport.salesPerPublisher(connection)
        elif(choice == "5"):
            while True:
                isbn = input("ISBN (13 characters): ")
                if(len(isbn) != 13):
                    print("Please enter a 13 character ISBN")
                else:
                    break
            title = input("Title: ")
            while True:
                try:
                    price = float(input("Price (Ex. X.XX): $"))
                except ValueError:
                    print("Please enter a price with the format X.XX")
                    continue
                else:
                    break
            author = input("Author: ")
            while True:
                publisher = input("Publisher: ")
                cursor = connection.cursor()
                cursor.execute("SELECT publisherName FROM PUBLISHER WHERE publisherName = ?", (publisher,))
                foundPublisher = cursor.fetchall()
                if (foundPublisher):
                    break
                else:
                    print("Please enter a valid publisher")
                    continue
            genre = input("Genre: ")
            while True:
                try:
                    numberOfPages = int(input("Number of pages: "))
                except ValueError:
                    print("Please enter a valid integer for the number of pages")
                    continue
                else:
                    break
            while True:
                try:
                    publisherPercent = float(input("Publisher percent (Ex. XXX.XX): "))
                except ValueError:
                    print("Please enter a price with the format XXX.XX")
                    continue
                else:
                    break
            while True:
                try:
                     stockQuantity = int(input("Stock Quantity: "))
                except ValueError:
                    print("Please enter a valid integer for the stock quantity")
                    continue
                else:
                    break
            while True:
                try:
                     salesLastMonth = int(input("Sales last month: "))
                except ValueError:
                    print("Please enter a valid integer for the sales last month")
                    continue
                else:
                    break
            while True:
                try:
                     currentSales = int(input("Current sales: "))
                except ValueError:
                    print("Please enter a valid integer for the current sales")
                    continue
                else:
                    break
            while True:
                try:
                     warehousePrice = float(input("Warehouse price: "))
                except ValueError:
                    print("Please enter a warehouse price with the format X.XX")
                    continue
                else:
                    break
            isAdded = editBook.addBook(connection, isbn, title, price, author, publisher, genre, numberOfPages, publisherPercent, stockQuantity, salesLastMonth, currentSales, warehousePrice)
            if(isAdded == False):
                print("Book with ISBN " + isbn + "already exists\n")
            else:
                print(title + " added!\n")
                editBook.orderBooksForStore(connection)
        elif(choice == "6"):
            isbn = input("ISBN of book to be deleted: ")
            isDeleted = editBook.deleteBook(connection, isbn)
            if(isDeleted == False):
                print("Book with ISBN " + isbn + " does not exist\n")
            else:
                print("book removed!\n")
        else:
            print("Please try again :(")
