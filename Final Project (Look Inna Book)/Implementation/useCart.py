#Create a new cart
def createCart(connection, total, loggedIn, username):
    if(loggedIn):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO BOOKSTORE_CART(username, totalCost) VALUES(?, ?)", (username, total)) 
    else:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO BOOKSTORE_CART(totalCost) VALUES(?)", (total,))
    return cursor.lastrowid

#View a carts contents
def viewCart(connection, cartNumber):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM CART_CONTAINS LEFT JOIN BOOK ON CART_CONTAINS.ISBN = BOOK.ISBN WHERE cartNumber = ?", (cartNumber,))
    currentCart = cursor.fetchall()
    if(currentCart):
        for item in currentCart:
            print("Title: " + item[4] + ", Price: $" + str("{:.2f}".format(item[5])) + ", In Stock: " + str(item[11]) + ", Quantity in cart: " + str(item[2]))
            print("\tISBN: " + item[3] + ", Author: " + item[6] + ", Publisher: " + item[7] + ", Genre: " + item[8] + "\n")       
        return True
    else:
        print("Your cart is empty...\n") 

#Get the  current user's cart number
def getCart(connection, hasCart, cartNumber, loggedIn, username):
    if (hasCart == False):
        cardRowId = createCart(connection, 0, loggedIn, username) 
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BOOKSTORE_CART WHERE rowid = ?", (cardRowId,))
        cart = cursor.fetchall()
        cartNumber = cart[0][0]
        hasCart = True
    return hasCart, cartNumber

#Edit cart if a user wants to remove books from their cart
def editCart(connection, cartNumber):
    editing = True
    while editing:
        isbn = str(input("Enter the ISBN of the book you would like to remove (Enter 0 to exit): "))
        if(isbn == "0"):
            print()
            break
        while True:
            try:
                quantity = int(input("Quantity to remove (Enter 0 to exit): "))
            except ValueError:
                print("Please enter a valid integer for the quantity\n")
                continue
            else:
                break
        if(quantity == 0):
            print()
            break
            
        cursor = connection.cursor()
        cursor.execute("SELECT quantity FROM CART_CONTAINS WHERE ISBN = ?", (isbn,))
        bookInCart = cursor.fetchall() 
        if(bookInCart):
            book = bookInCart[0]
            if(book[0] < quantity or quantity < 0):
                print("Invalid quantity\n")
                continue
            elif(book[0] == quantity):
                cursor = connection.cursor()
                cursor.execute("DELETE FROM CART_CONTAINS WHERE ISBN = ? and cartNumber = ?", (isbn, cartNumber)) 
                if(quantity == 1):
                    print("Book removed!\n")
                else:
                    print("Books removed!\n")
            else:
                cursor = connection.cursor()
                cursor.execute("UPDATE CART_CONTAINS SET quantity = quantity - ? WHERE ISBN = ? and cartNumber = ?", (quantity, isbn, cartNumber))                               
                if(quantity == 1):
                    print("Book removed!\n")
                else:
                    print("Books removed!\n")
        else:
            print("Book with ISBN " + isbn + " not in cart\n")