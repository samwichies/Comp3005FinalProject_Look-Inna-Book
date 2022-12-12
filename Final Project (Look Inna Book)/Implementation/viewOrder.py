#View the users completed orders
def viewOrderList(connection, username):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM BOOKSTORE_ORDER WHERE username = ?", (username,))
    orders = cursor.fetchall()
    for item in orders:
        print("Order placed: " + item[6] + ", Order number: " + str(item[0]) + "\n")
    lookingAtOrders = True
    while (lookingAtOrders == True):
        userOrder = input("Enter an order number to view details (Enter 0 to exit): ")
        print()
        if(userOrder == "0"):
            lookingAtOrders == False
            break
        cursor.execute("SELECT * FROM BOOKSTORE_ORDER WHERE orderNumber = ?", (userOrder,))
        order = cursor.fetchall()
        if(order):
            item = order[0]
            print("Order placed: " + item[6] + ", Order number: " + str(item[0]) + ", Total: $" + "{:.2f}".format(item[2]))
            print("Billing Information: " + item[3])
            print("Shipping Information: " + item[4])
            print("Estimated Arrival: " + item[7] + ", Tracking Information: " + item[5])
            viewAOrder(connection, userOrder)
        else:
            print("Order not found :(\n")
    
#View more details on a specific order
def viewAOrder(connection, orderNumber):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ORDER_CONTAINS LEFT JOIN BOOK ON ORDER_CONTAINS.ISBN = BOOK.ISBN WHERE orderNumber = ?", (orderNumber,))
    currentOrder = cursor.fetchall()
    print("Books Ordered:")
    for item in currentOrder:
            print("Title: " + item[4] + ", Price: $" + str("{:.2f}".format(item[5])) + ", Quantity in order: " + str(item[2]))
            print("\tISBN: " + item[3] + ", Author: " + item[6] + ", Publisher: " + item[7] + ", Genre: " + item[8] + "\n") 