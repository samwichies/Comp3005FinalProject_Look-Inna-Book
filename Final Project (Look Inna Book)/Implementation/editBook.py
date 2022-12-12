#Allow owner to add a book to the catalog
def addBook(connection, isbn, title, price, author, publisher, genre, numberOfPages, publisherPercent, stockQuantity, salesLastMonth, currentSales, warehousePrice):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM BOOK WHERE ISBN = ?", (isbn,))
    bookExists = cursor.fetchall()
    if(bookExists):
        return False
    cursor = connection.cursor()
    cursor.execute("INSERT INTO BOOK(ISBN, title, price, author, publisher, genre, numberOfPages, publisherPercent, stockQuantity, salesLastMonth, currentSales, warehousePrice) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (isbn, title, price, author, publisher, genre, numberOfPages, publisherPercent, stockQuantity, salesLastMonth, currentSales, warehousePrice))
    return cursor.lastrowid

#Allow owner to delete a book from the catalog
def deleteBook(connection, isbn):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM BOOK WHERE ISBN = ?", (isbn,))
    bookExists = cursor.fetchall()
    if(bookExists):
        sql = ''' DELETE FROM BOOK WHERE ISBN = ?'''
        cursor = connection.cursor()
        cursor.execute(sql, (isbn,))
        cursor = connection.cursor()
        cursor.execute("DELETE FROM CART_CONTAINS WHERE ISBN = ?", (isbn,))
        return cursor.lastrowid
    else:
        return False

#If a book quantity is less than 10, order more of that book based on last months sales
def orderBooksForStore(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT ISBN, stockQuantity, salesLastMonth FROM BOOK")
    updateBooks = cursor.fetchall()
    for book in updateBooks:
        if(int(book[1]) < 10):
            if((int(book[1]) + int(book[2]) >= 10)):
                sql = ''' UPDATE BOOK SET stockQuantity = stockQuantity + salesLastMonth WHERE ISBN = ?'''
                cursor = connection.cursor()
                cursor.execute(sql, (book[0],))
            else:        
                sql = ''' UPDATE BOOK SET stockQuantity = 10 WHERE ISBN = ?'''
                cursor = connection.cursor()
                cursor.execute(sql, (book[0],))