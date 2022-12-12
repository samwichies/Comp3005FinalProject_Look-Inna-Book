#Create a report of sales by genre
def createGenreView(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE VIEW genreView as
                    SELECT genre, SUM(currentSales), SUM(currentSales*price) FROM BOOK
                    GROUP BY genre""")

#Create a report of sales by author
def createAuthorView(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE VIEW authorView as
                    SELECT author, SUM(currentSales), SUM(currentSales*price) FROM BOOK
                    GROUP BY author""")

#Create a report of sales by publisher
def createPublisherView(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE VIEW publisherView as
                    SELECT publisher, SUM(currentSales), SUM(currentSales*price) FROM BOOK
                    GROUP BY publisher""")

#Create a report of sales vs. expenditures
def createSalesView(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE VIEW salesView as
                    SELECT SUM(currentSales*price) AS sales, SUM(((publisherPercent * 1.00/100)*currentSales*price) + ((stockQuantity+currentSales)*warehousePrice)) AS expenditures FROM BOOK""")

#Drop report of sales by genre view
def dropGenreView(connection):
    cursor = connection.cursor()
    cursor.execute("DROP VIEW genreView")

#Drop report of sales by author view
def dropAuthorView(connection):
    cursor = connection.cursor()
    cursor.execute("DROP VIEW authorView")  

#Drop report of sales by publisher view
def dropPublisherView(connection):
    cursor = connection.cursor()
    cursor.execute("DROP VIEW publisherView")

#Drop report of sales vs. expenditures view
def dropSalesView(connection):
    cursor = connection.cursor()
    cursor.execute("DROP VIEW salesView")

#Prints data from report of sales vs. expenditures
def salesAndExp(connection):
    dropSalesView(connection)
    createSalesView(connection)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM salesView")
    data = cursor.fetchall()
    dataPoint = data[0]
    print("Sales: $" + str("{:.2f}".format(dataPoint[0])))
    print("Expenditures: $" + str("{:.2f}".format(dataPoint[1])) + "\n")

#Prints data from report of sales by genre
def salesPerGenre(connection):
    dropGenreView(connection)
    createGenreView(connection)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM genreView")
    data = cursor.fetchall()
    for item in data:
        print("Genre: " + item[0] + ", Books sold: " + str(item[1]) + ", Earnings: $" + str("{:.2f}".format(item[2])))
        print()

#Prints data from report of sales by author
def salesPerAuthor(connection):
    dropAuthorView(connection)
    createAuthorView(connection)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM authorView")
    data = cursor.fetchall()
    for item in data:
        print("Author: " + item[0] + ", Books sold: " + str(item[1]) + ", Earnings: $" + str("{:.2f}".format(item[2])))
        print()

#Prints data from report of sales by publisher
def salesPerPublisher(connection):
    dropPublisherView(connection)
    createPublisherView(connection)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM publisherView")
    data = cursor.fetchall()
    for item in data:
        print("Publisher: " + item[0] + ", Books sold: " + str(item[1]) + ", Earnings: $" + str("{:.2f}".format(item[2])))
        print()
