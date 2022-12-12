import datetime
import editBook

#Browsing menu
def browse(connection, cartNumber):
    searching = True
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM BOOK")
    books = cursor.fetchall()
    while searching:
        print("Menu:")
        print("1) Search by title")
        print("2) Search by author")
        print("3) Search by publisher")
        print("4) Search by ISBN")
        print("5) Search by genre")
        print("6) Add item(s) to cart")
        print("0) Go back")
        choice = input("Enter your selection: ")
        print()
        if(choice == "0"):
            searching = False
        elif(choice == "1"):
            title = input("Enter title: ")
            found = False
            for book in books:
                if str.lower(title) in str.lower(book[1]):
                    found = True
                    print("Title: " + book[1] + ", ISBN: " + book[0]) 
            print()
            if(found == True):
                viewBookInfo(connection)
            else:
                print("No matches found :(\n")
        elif(choice == "2"):
            author = input("Enter author: ")
            found = False
            for book in books:
                if str.lower(author) in str.lower(book[3]):
                    found = True
                    print("Title: " + book[1] + ", ISBN: " + book[0])
            print()
            if(found == True):
                viewBookInfo(connection)
            else:
                print("No matches found :(\n")
        elif(choice == "3"):
            publisher = input("Enter publisher: ")
            found = False
            for book in books:
                if str.lower(publisher) in str.lower(book[4]):
                    found = True
                    print("Title: " + book[1] + ", ISBN: " + book[0]) 
            print()
            if(found == True):
                viewBookInfo(connection)
            else:
                print("No matches found :(\n")
        elif(choice == "4"):
            isbn = input("Enter ISBN: ")
            found = False
            for book in books:
                if str.lower(isbn) in str.lower(book[0]):
                    found = True
                    print("Title: " + book[1] + ", ISBN: " + book[0]) 
            print()
            if(found == True):
                viewBookInfo(connection)
            else:
                print("No matches found :(\n")             
        elif(choice == "5"):
            genre = input("Enter genre: ")
            found = False
            for book in books:
                if str.lower(genre) in str.lower(book[5]):
                    found = True
                    print("Title: " + book[1] + ", ISBN: " + book[0]) 
            print()
            if(found == True):
                viewBookInfo(connection)
            else:
                print("No matches found :(\n")
        elif(choice == "6"):
            print("Enter the ISBN(s) of the book(s) you would like to purchase (Enter 0 to exit)")
            addingToCart = True
            while addingToCart:
                isbn = str(input("ISBN: "))
                if(isbn == "0"):
                    addingToCart = False
                    print()
                    break                
                quantity = input("Quantity: ")
                if(quantity == "0"):
                    addingToCart = False
                    print()
                    break
                found = False
                for book in books:
                    if isbn == str(book[0]):
                        found = True
                        cursor = connection.cursor()
                        cursor.execute("SELECT * FROM CART_CONTAINS WHERE ISBN = ? ", (isbn,))
                        currentlyInCart = cursor.fetchall()
                        if(currentlyInCart):
                            canAdd = updateBookInCart(connection, isbn, quantity, cartNumber)
                            if(canAdd != False):
                                print(book[1] + " added to cart!\n")                        
                        else:
                            canAdd = addBookToCart(connection, isbn, quantity, cartNumber)
                            if(canAdd != False):
                                print(book[1] + " added to cart!\n")

                if(found == False):
                    print("No matches found :(\n")
        else:
            print("Please try again :(")

#View more info on a book with a specfic ISBN
def viewBookInfo(connection):
    while True:
        isbn = str(input("Enter an ISBN to view more info (Enter 0 to exit): "))
        if(isbn == "0"):
            print()
            break
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BOOK WHERE ISBN = ? ", (isbn,))
        books = cursor.fetchall()
        if(books):
            book = books[0]
            print("Title: " + book[1] + ", Price: $" + str("{:.2f}".format(book[2])) + ", In Stock: " + str(book[8]))
            print("\tISBN: " + book[0] + ", Author: " + book[3] + ", Publisher: " + book[4] + ", Genre: " + book[5] + "\n")  
        else:
            print("ISBN " + isbn + " not found :(\n")

#Try to add a book to the users cart
def addBookToCart(connection, isbn, quantity, cartNumber):
    cursor = connection.cursor()
    cursor.execute("SELECT stockQuantity FROM BOOK WHERE ISBN = ?", (isbn,))
    book = cursor.fetchall()
    if(book):
        numberofCopies = book[0][0]
        if(numberofCopies >= int(quantity)):
            cursor = connection.cursor()
            cursor.execute("INSERT INTO CART_CONTAINS(ISBN, cartNumber, quantity) VALUES(?, ?, ?)", (isbn, cartNumber, quantity))
            return cursor.lastrowid
        else:
            print("Quantity unavailable, please try again\n")
            return False
    else:
        print("ISBN " + isbn + " not found :(\n")
        return False

#Try to update a book if a user wants to add more of it to their cart
def updateBookInCart(connection, isbn, quantity, cartNumber):
    cursor = connection.cursor()
    cursor.execute("SELECT stockQuantity FROM BOOK WHERE ISBN = ?", (isbn,))
    book = cursor.fetchall()
    stockQuantity = book[0][0]
    
    cursor = connection.cursor()
    cursor.execute("SELECT quantity FROM CART_CONTAINS WHERE cartNumber = ?", (cartNumber,))
    cart = cursor.fetchall()
    copiesWanted = cart[0][0]

    if(stockQuantity >= int(quantity) + copiesWanted):
        cursor = connection.cursor()
        cursor.execute("UPDATE CART_CONTAINS SET quantity = quantity + ? WHERE ISBN = ? and cartNumber = ?", (quantity, isbn, cartNumber,))
        return cursor.lastrowid
    else:
        print("Quantity unavailable, please try again\n")
        return False

#Try to purchase the items in the user cart
def purchase(connection, cartNumber, username):
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(price*quantity) FROM CART_CONTAINS LEFT JOIN BOOK ON CART_CONTAINS.ISBN = BOOK.ISBN WHERE cartNumber = ?", (cartNumber,))
    currentCart = cursor.fetchall()
    total = currentCart[0][0]
    print("Your total is: $" + str("{:.2f}".format(total)))   
    toPlace = ""
    while (toPlace != "y" and toPlace != "n"):
        toPlace = input("Would you like to proceed? (y/n): ")
    if(toPlace == "y"):
        billing = input("Please enter your billing information: ")
        shipping = input("Please enter your shipping information: ")
    elif(toPlace == "n"):
        print()
        return False
    placed = ""
    while (placed != "y" and placed != "n"):
        placed = input("Place order? (y/n): ")
        print("Order placed :)\n")
    if(placed == "y"):
        orderNumber = createOrder(connection, total, billing, shipping, username)
        cursor.execute("SELECT ISBN, quantity FROM CART_CONTAINS WHERE cartNumber = ?", (cartNumber,))
        orders = cursor.fetchall()
        for item in orders:
            addBookToOrder(connection, item[0], orderNumber, item[1])
        sellBooksFromCart(connection, cartNumber)
        deleteCart(connection, cartNumber)
        deleteCartContains(connection, cartNumber)

#Create a new order
def createOrder(connection, totalCost, billing, shipping, username):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO BOOKSTORE_ORDER(username, totalCost, billingInformation, shippingInformation, trackingInformation, datePlaced, estimatedArrival) VALUES(?, ?, ?, ?, ?, ?, ?)", (username, totalCost, billing, shipping, "Order is being processed at the warehouse", datetime.date.today(), datetime.date.today() + datetime.timedelta(days = 1)))
    return cursor.lastrowid

#Add a book to an order
def addBookToOrder(connection, isbn, orderNumber, quantity):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO ORDER_CONTAINS(ISBN, orderNumber, quantity) VALUES(?, ?, ?)", (isbn, orderNumber, quantity))
    return cursor.lastrowid

#Update books based on which ones have been sold and how many
def sellBooksFromCart(connection, cartNumber):
    cursor = connection.cursor()
    cursor.execute("SELECT CART_CONTAINS.ISBN, quantity FROM CART_CONTAINS LEFT JOIN BOOK ON CART_CONTAINS.ISBN = BOOK.ISBN WHERE cartNumber = ?", (cartNumber,))
    currentCart = cursor.fetchall()
    for item in currentCart:
        sellBook(connection, item[0], item[1])   

#Update a book based on which ones is being sold and how many and updating the publishers balance from bookstore earnings
def sellBook(connection, isbn, quantity):
    cursor = connection.cursor()
    cursor.execute("UPDATE BOOK SET stockQuantity = stockQuantity - ?, currentSales = currentSales + ? WHERE ISBN = ?", (quantity, quantity, isbn))
    cursor = connection.cursor()
    cursor.execute("SELECT price, publisherPercent, currentSales, publisher FROM BOOK WHERE ISBN = ?", (isbn,))
    book = cursor.fetchall()
    currentBook = book[0]
    totalPayout = ((float(currentBook[1]) / 100) * float(currentBook[0])) * currentBook[2]
    cursor = connection.cursor()
    cursor.execute("UPDATE PUBLISHER SET balanceFromBookstore = balanceFromBookstore + ? WHERE publisherName = ?", (float(totalPayout), currentBook[3]))

    editBook.orderBooksForStore(connection)    
    return cursor.lastrowid 

#Delete a cart
def deleteCart(connection, cartNumber):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM BOOKSTORE_CART WHERE cartNumber = ?", (cartNumber,)) 
    return cursor.lastrowid

#Delete a cartContains
def deleteCartContains(connection, cartNumber):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM CART_CONTAINS WHERE cartNumber = ?", (cartNumber,))
    connection.commit()    
    return cursor.lastrowid