-- Users Table
CREATE TABLE Users (
    _id INT PRIMARY KEY,
    State VARCHAR(2),
    createdDate DATE,
    lastLogin DATE,
    role VARCHAR(50),
    Active BIT,
    signUpSource VARCHAR(100)
);

-- Categories Table
CREATE TABLE Categories (
    _id INT PRIMARY KEY,
    category VARCHAR(100),
    categoryCode VARCHAR(50)
);

-- Brands Table
CREATE TABLE Brands (
    _id INT PRIMARY KEY,
    Brand VARCHAR(100),
    CodeCategory VARCHAR(50),
    Cpgtop VARCHAR(100),
    Brandname VARCHAR(100),
    Barcode VARCHAR(50),
    categoryCode INT,
    FOREIGN KEY (categoryCode) REFERENCES Categories(_id)
);

-- Items Table
CREATE TABLE Items (
    Barcode VARCHAR(50) PRIMARY KEY,
    Description VARCHAR(255),
    itemPrice DECIMAL(10, 2),
    finalPrice DECIMAL(10, 2),
    quantityPurchased INT,
    needsFetchReview BIT,
    Partneritemid VARCHAR(50),
    preventTargetGapPoints BIT,
    userFlaggedNewItem BIT,
    brand_id INT,
    FOREIGN KEY (brand_id) REFERENCES Brands(_id)
);

-- Receipts Table
CREATE TABLE Receipts (
    _id INT PRIMARY KEY,
    bonusPointsEarned INT,
    bonusPointsEarnedReason VARCHAR(255),
    createDate DATE,
    dateScanned DATE,
    finishedDate DATE,
    pointsAwardedDate DATE,
    pointsEarned INT,
    purchaseDate DATE,
    purchasedItemCount INT,
    rewardsReceiptItemList TEXT,
    rewardsReceiptStatus VARCHAR(50),
    totalSpent DECIMAL(10, 2),
    userId INT,
    FOREIGN KEY (userId) REFERENCES Users(_id)
);

-- Transaction Table
CREATE TABLE TransactionS (
    Receipt_id INT,
    User_id INT,
    Barcode VARCHAR(50),
    Brand_id INT,
    FOREIGN KEY (Receipt_id) REFERENCES Receipts(_id),
    FOREIGN KEY (User_id) REFERENCES Users(_id),
    FOREIGN KEY (Barcode) REFERENCES Items(Barcode),
    FOREIGN KEY (Brand_id) REFERENCES Brands(_id),
    PRIMARY KEY (Receipt_id, User_id, Barcode, Brand_id)
);
