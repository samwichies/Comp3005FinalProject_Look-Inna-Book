--User data
create table BOOKSTORE_USER 
    (username                varchar(30) not null unique,
    userPassword             varchar(30) not null,
    billingInformation       varchar(35) not null,
    shippingInformation      varchar(100) not null,
    userPrivileges           boolean,
    primary key (username)
    );

--Order data
create table BOOKSTORE_ORDER 
    (orderNumber             integer primary key autoincrement,
    username                 varchar(30) not null,
    totalCost                numeric(6, 2) not null,
    billingInformation       varchar(35) not null,
    shippingInformation      varchar(100) not null,
    trackingInformation      varchar(100) not null,
    datePlaced               varchar(10) not null,
    estimatedArrival         varchar(10) not null,
	foreign key (username) references BOOKSTORE_USER (username)
    );

--Publisher data
create table PUBLISHER 
    (publisherName           varchar(30) not null unique,
    address                  varchar(100) not null,
    emailAddress             varchar(100) not null,
    bankingAccount           varchar(35) not null,
    balanceFromBookstore     numeric(10, 2) not null,
    primary key (publisherName)
    );

--Publisher's phone numbers
create table PUBLISHER_PHONE_NUMBERS 
    (phoneNumber             char(11) not null unique,
    publisherName            varchar(30) not null, 
    primary key (phoneNumber, publisherName),
    foreign key (publisherName) references PUBLISHER
    );

--Book data
create table BOOK 
    (ISBN                     char(13) not null unique,
    title                     varchar(100) not null,
    price                     numeric(5, 2) not null,
    author                    varchar(100) not null,
    publisher                 varchar(100) not null,
    genre                     varchar(100) not null,
    numberOfPages             int not null,
    publisherPercent          numeric(5, 2),
    stockQuantity             int not null,
    salesLastMonth            int not null,
    currentSales              int not null,
    warehousePrice            int not null,
    primary key (ISBN),
    foreign key (publisher) references PUBLISHER (publisherName)
    );

--Items contained in a specific order
create table ORDER_CONTAINS 
    (ISBN                    varchar(13) not null,
    orderNumber              int not null,
    quantity                 int not null,
    primary key (ISBN, orderNumber),
    foreign key (ISBN) references BOOK,
    foreign key (orderNumber) references BOOKSTORE_ORDER
    );

--Cart data
create table BOOKSTORE_CART 
    (cartNumber              integer primary key autoincrement,
    username                 varchar(30),
    totalCost                numeric(6, 2) not null,
	foreign key (username) references BOOKSTORE_USER (username)
    );

--Items contained in a specific cart
create table CART_CONTAINS 
    (ISBN                    varchar(13) not null,
    cartNumber               int not null,
    quantity                 int not null,
    primary key (ISBN, cartNumber),
    foreign key (ISBN) references BOOK,
    foreign key (cartNumber) references BOOKSTORE_ORDER
    );
