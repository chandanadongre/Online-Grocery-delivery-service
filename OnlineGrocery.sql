CREATE SCHEMA GROCERY;
USE GROCERY;

CREATE TABLE Admins (
	AdminID INT PRIMARY KEY,
	FirstName VARCHAR(255),
    LastName VARCHAR(255),
    EmailID UNIQUE VARCHAR(255) ,
    Username VARCHAR(255),
    Password VARCHAR(255),
    PhoneNo VARCHAR(20),
    Address VARCHAR(255)
);

CREATE TABLE Customer (
	CustomerID INT PRIMARY KEY,
	FirstName VARCHAR(255),
    LastName VARCHAR(255),
    EmailID VARCHAR(255) UNIQUE,
    Username VARCHAR(255),
    Password VARCHAR(255),
    PhoneNo VARCHAR(20),
    Address VARCHAR(255)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    PaymentMethod VARCHAR(50),
    PaymentStatus VARCHAR(50),
    DeliveryAddress VARCHAR(255),
    CustomerID INT,
    Amount DECIMAL(10, 2),
    OrderDateTime TIMESTAMP,
    OrderStatus VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE Product (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(255),
    Price DECIMAL(10, 2),
    QuantityInStock INT,
    Description TEXT
);

CREATE TABLE OrderItem (
    OrderItemID INT PRIMARY KEY,
    OrderID INT,
    Quantity INT,
    ProductID INT,
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE Transaction (
    TransactionID INT PRIMARY KEY,
    OrderID INT,
    PaymentDateTime TIMESTAMP,
    Amount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    PaymentStatus VARCHAR(50),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

CREATE TABLE DeliveryDriver (
    DeliveryID INT PRIMARY KEY,
    Name VARCHAR(255),
    Address VARCHAR(255),
    EmailID VARCHAR(255) UNIQUE,
    PhoneNo VARCHAR(20),
    VehicleInfo VARCHAR(255)
);

CREATE TABLE DeliveryAssignment (
    AssignmentID INT PRIMARY KEY,
    OrderID INT,
    DeliveryID INT,
    DeliveryAddress VARCHAR(255),
    AssignmentDateTime TIMESTAMP,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (DeliveryID) REFERENCES DeliveryDriver(DeliveryID)
);

SHOW TABLES;

INSERT INTO Admins (AdminID, FirstName, LastName, EmailID, Username, Password, PhoneNo, Address)
VALUES
(5, 'Chandana', 'Chandana', 'chandana@example.com', 'Chandana', 'Chandana', '555-555-5559', '202 Banglore'),
(6, 'Bhodhitha', 'Bhodhitha', 'Bhodhitha@example.com', 'Bhodhitha', 'Bhodhitha', '555-555-5560', '303 Banglore'),
(7, 'Rajesh', 'Kumar', 'rajesh.kumar@example.com', 'rajeshkumar', 'rajesh789', '555-555-5561', '404 Lily Road'),
(8, 'Priyanka', 'Singh', 'priyanka.singh@example.com', 'priyankasingh', 'priyanka123', '555-555-5562', '505 Orchid Lane');

INSERT INTO Customer (CustomerID, FirstName, LastName, EmailID, Username, Password, PhoneNo, Address)
VALUES 
(1, 'John', 'Doe', 'john.doe@example.com', 'johndoe123', 'password123', '1234567890', '123 Main St'),
(2, 'Alice', 'Johnson', 'alice.j@example.com', 'alice123', 'securepass', '9876543210', '456 Elm St'),
(3, 'Michael', 'Smith', 'michael.smith@example.com', 'mike123', 'pass123', '2345678901', '789 Oak St'),
(4, 'Emily', 'Davis', 'emily.d@example.com', 'emily456', 'secure123', '3456789012', '101 Pine St'),
(5, 'David', 'Brown', 'david.b@example.com', 'david789', 'davidpass', '4567890123', '222 Maple St'),
(6, 'Emma', 'Johnson', 'emma.j@example.com', 'emma101', 'emma123', '5678901234', '333 Pine St'),
(7, 'Sophia', 'Lee', 'sophia.l@example.com', 'sophia123', 'sophiapass', '6789012345', '444 Elm St'),
(8, 'Noah', 'Williams', 'noah.w@example.com', 'noah789', 'noahpass', '7890123456', '555 Oak St'),
(9, 'Olivia', 'Martin', 'olivia.m@example.com', 'olivia123', 'oliviapass', '8901234567', '666 Maple St'),
(10, 'Liam', 'Thomas', 'liam.t@example.com', 'liam789', 'liampass', '9012345678', '777 Pine St');

SELECT * FROM Customer;

INSERT INTO Orders (OrderID, PaymentMethod, PaymentStatus, DeliveryAddress, CustomerID, Amount, OrderDateTime, OrderStatus)
VALUES 
(1, 'Credit Card', 'Paid', '123 Main St', 1, 75.50, '2023-10-07 14:30:00', 'Delivered'),
(2, 'PayPal', 'Paid', '456 Elm St', 2, 92.20, '2023-10-08 12:45:00', 'In Progress'),
(3, 'Debit Card', 'Pending', '789 Oak St', 3, 120.75, '2023-10-09 15:20:00', 'Processing'),
(4, 'Cash on Delivery', 'Pending', '101 Pine St', 4, 45.60, '2023-10-10 17:10:00', 'Pending'),
(5, 'Credit Card', 'Paid', '222 Maple St', 5, 88.90, '2023-10-11 11:55:00', 'Delivered');

INSERT INTO Product (ProductID, ProductName, Price, QuantityInStock, Description)
VALUES 
(1, 'Apples', 3.50, 200, 'Fresh and juicy apples'),
(2, 'Milk', 2.00, 150, 'Fresh dairy milk'),
(3, 'Bread', 1.75, 180, 'Whole wheat bread'),
(4, 'Eggs', 2.25, 250, 'Farm-fresh eggs'),
(5, 'Chicken', 5.75, 120, 'Boneless chicken breast'),
(6, 'Bananas', 1.25, 300, 'Sweet and ripe bananas'),
(7, 'Oranges', 2.00, 250, 'Juicy and fresh oranges'),
(8, 'Tomatoes', 1.75, 200, 'Farm-fresh tomatoes'),
(9, 'Potatoes', 1.50, 180, 'Organic potatoes'),
(10, 'Carrots', 1.20, 220, 'Crunchy and nutritious carrots');

INSERT INTO OrderItem (OrderItemID, OrderID, Quantity, ProductID, TotalAmount)
VALUES 
(1, 1, 2, 1, 60.00),
(2, 1, 1, 2, 15.50),
(3, 2, 3, 3, 75.75),
(4, 3, 1, 4, 30.25),
(5, 4, 2, 5, 45.80);

INSERT INTO Transaction (TransactionID, OrderID, PaymentDateTime, Amount, PaymentMethod, PaymentStatus)
VALUES 
(1, 1, '2023-10-07 14:40:00', 75.50, 'Credit Card', 'Success'),
(2, 2, '2023-10-08 13:00:00', 92.20, 'PayPal', 'Success'),
(3, 3, '2023-10-09 15:30:00', 120.75, 'Debit Card', 'Pending'),
(4, 4, '2023-10-10 17:20:00', 45.60, 'Cash on Delivery', 'Pending'),
(5, 5, '2023-10-11 12:00:00', 88.90, 'Credit Card', 'Success');

INSERT INTO DeliveryDriver (DeliveryID, Name, Address, EmailID, PhoneNo, VehicleInfo)
VALUES 
(1, 'Michael Johnson', '123 Main St', 'michael.j@example.com', '555-1234', 'Van - ABC123'),
(2, 'Emily Davis', '456 Elm St', 'emily.d@example.com', '555-5678', 'Car - XYZ789'),
(3, 'Daniel Smith', '789 Oak St', 'daniel.s@example.com', '555-9101', 'Bike - QRS456'),
(4, 'Olivia Brown', '101 Pine St', 'olivia.b@example.com', '555-1122', 'Scooter - UVW789'),
(5, 'Ethan Johnson', '222 Maple St', 'ethan.j@example.com', '555-3344', 'Truck - DEF123');

INSERT INTO DeliveryAssignment (AssignmentID, OrderID, DeliveryID, DeliveryAddress, AssignmentDateTime)
VALUES 
(1, 1, 1, '123 Main St', '2023-10-07 14:40:00'),
(2, 2, 2, '456 Elm St', '2023-10-08 13:00:00'),
(3, 3, 3, '789 Oak St', '2023-10-09 15:30:00'),
(4, 4, 4, '101 Pine St', '2023-10-10 17:20:00'),
(5, 5, 5, '222 Maple St', '2023-10-11 12:00:00');

CREATE TRIGGER update_product_quantity_on_delete
BEFORE DELETE ON Product
FOR EACH ROW
BEGIN
    DECLARE current_quantity INT;
    SET current_quantity = (SELECT QuantityInStock FROM Product WHERE ProductID = OLD.ProductID);
    
    -- Ensure that the current_quantity is not negative after the update
    IF current_quantity >= OLD.Quantity THEN
        UPDATE Product
        SET QuantityInStock = current_quantity - OLD.Quantity
        WHERE ProductID = OLD.ProductID;
    END IF;
END;
CREATE TRIGGER add_new_item_by_admin
AFTER INSERT ON Product
FOR EACH ROW
BEGIN
    -- Set default values or perform additional actions based on your requirements
    UPDATE Product
    SET SomeColumn = DefaultValue
    WHERE ProductID = NEW.ProductID;
END;
