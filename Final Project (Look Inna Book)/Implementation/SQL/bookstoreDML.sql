--Clear 
delete from PUBLISHER;
delete from BOOK;
delete from BOOKSTORE_USER;
delete from BOOKSTORE_ORDER;
delete from ORDER_CONTAINS;
delete from BOOKSTORE_CART;
delete from CART_CONTAINS;
delete from PUBLISHER;
delete from PUBLISHER_PHONE_NUMBERS;

--Create default user values to test user interface
insert into BOOKSTORE_USER values('customer1', 'c1', '1231 2312 3123 1231 01/20 123', '123 User Avenue, Usertown, User, USR-123', false);
insert into BOOKSTORE_USER values('customer2', 'c2', '2342 3423 4234 2342 02/20 234', '234 User Road, Userville, User, USR-234', false);
insert into BOOKSTORE_USER values('customer3', 'c3', '3453 4534 5345 3453 03/20 345', '345 User Street, Userford, User, USR-345', false);
insert into BOOKSTORE_USER values('customer4', 'c4', '4564 5645 6456 4564 04/20 456', '456 User Lane, Userborough, User, USR-456', false);
insert into BOOKSTORE_USER values('customer5', 'c5', '5675 6756 7567 5675 05/20 567', '678 User Circle, Usercester, User, USR-678', false);

--Create default owner values to test owner interface
insert into BOOKSTORE_USER values('owner1', 'o1', '6786 7867 8678 6786 06/20 678', '123 Owner Avenue, Ownerville, Owner, OWN-123', true);
insert into BOOKSTORE_USER values('owner2', 'o2', '7897 8978 9789 7897 07/20 789', '234 Owner Street, Ownertown, Owner, OWN-234', true);
insert into BOOKSTORE_USER values('owner3', 'o3', '8908 9089 0890 8908 08/20 890', '456 Owner Road, Ownerford, Owner, OWN-456', true);

--Create default publisher values to test bookstore
insert into PUBLISHER values('Publisher Co.', '123 Publisher Road, Publisher, Publishertown, PUB-123', 'PublisherCO@email.com', '1111 2222 3333 1111 10/20 321', 120300);
insert into PUBLISHER values('Pubbie Press', '234 Publisher Lane, Publisher, Publisherford, PUB-234', 'PubbiePress@email.com', '2222 3333 4444 2222 11/20 432', 234000);
insert into PUBLISHER values('Pub Lisher Group', '345 Publisher Avenue, Publisher, Publisherhaven, PUB-345', 'PubLisherGroup@email.com', '3333 4444 5555 3333 12/20 554', 34050);

--Create default publisher numbers values to test bookstore
insert into PUBLISHER_PHONE_NUMBERS values('123-123-123', 'Publisher Co.');
insert into PUBLISHER_PHONE_NUMBERS values('234-234-234', 'Publisher Co.');
insert into PUBLISHER_PHONE_NUMBERS values('345-345-345', 'Pubbie Press');
insert into PUBLISHER_PHONE_NUMBERS values('456-456-456', 'Pubbie Press');
insert into PUBLISHER_PHONE_NUMBERS values('567-567-567', 'Pub Lisher Group');


--Create default book numbers values to test bookstore
insert into BOOK values('1231231231231', 'Beauty and The Book', 10.99, 'R.J Author', 'Publisher Co.', 'Books', 254, 50.00, 10, 5, 0, 2.49);
insert into BOOK values('2342342342342', 'Bookerella', 5.00, 'Bruce Bookwriter', 'Publisher Co.', 'Paper', 1000, 5.00, 9, 8, 0, 1.00);
insert into BOOK values('3453453453453', 'The Princess and the Book', 24.98, 'Ty Storysmith', 'Pubbie Press', 'Paper', 57, 25.00, 21, 23, 0, 5.47);
insert into BOOK values('4564564564564', 'Snow White and the Seven Books', 15.50, 'Harry Hardcover', 'Pubbie Press', 'Books', 355, 10.00, 4, 0, 0, 4.15);
insert into BOOK values('5675675675675', 'Book Hero 6', 29.49, 'Tina Pageturner', 'Pub Lisher Group', 'Reading', 787, 35.00, 19, 10, 0, 7.50);
