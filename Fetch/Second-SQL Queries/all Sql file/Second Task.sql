/*---1.What are the top 5 brands by receipts scanned for most recent month?*/
WITH RecentMonthReceipts AS (
    SELECT *
    FROM Receipts
    WHERE MONTH(purchaseDate) = (
        SELECT MONTH(MAX(purchaseDate))
        FROM Receipts
    )
    AND YEAR(purchaseDate) = (
        SELECT YEAR(MAX(purchaseDate))
        FROM Receipts
    )
),
BrandReceiptCount AS (
    SELECT b.Brand, COUNT(*) AS ReceiptCount,
           ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rn
    FROM RecentMonthReceipts r
    JOIN TransactionS t ON r._id = t.Receipt_id
    JOIN Brands b ON t.Brand_id = b._id
    GROUP BY b.Brand
)
SELECT Brand, ReceiptCount
FROM BrandReceiptCount
WHERE rn <= 5;

/* ---- 2 How does the ranking of the top 5 brands by receipts scanned for the recent month compare to the ranking for the previous month?*/
WITH RecentMonth AS (
    SELECT 
        MAX(purchaseDate) AS MaxDate
    FROM 
        Receipts
),
DateRanges AS (
    SELECT
        YEAR(MaxDate) AS RecentYear,
        MONTH(MaxDate) AS RecentMonth,
        YEAR(DATEADD(MONTH, -1, MaxDate)) AS PreviousYear,
        MONTH(DATEADD(MONTH, -1, MaxDate)) AS PreviousMonth
    FROM
        RecentMonth
),
RecentMonthReceipts AS (
    SELECT *
    FROM Receipts, DateRanges
    WHERE YEAR(purchaseDate) = RecentYear AND MONTH(purchaseDate) = RecentMonth
),
PreviousMonthReceipts AS (
    SELECT *
    FROM Receipts, DateRanges
    WHERE YEAR(purchaseDate) = PreviousYear AND MONTH(purchaseDate) = PreviousMonth
),
RecentMonthBrandCount AS (
    SELECT 
        b.Brand, 
        COUNT(*) AS ReceiptCount,
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS Rank
    FROM 
        RecentMonthReceipts r
        JOIN TransactionS t ON r._id = t.Receipt_id
        JOIN Brands b ON t.Brand_id = b._id
    GROUP BY 
        b.Brand
),
PreviousMonthBrandCount AS (
    SELECT 
        b.Brand, 
        COUNT(*) AS ReceiptCount,
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS Rank
    FROM 
        PreviousMonthReceipts r
        JOIN TransactionS t ON r._id = t.Receipt_id
        JOIN Brands b ON t.Brand_id = b._id
    GROUP BY 
        b.Brand
)
SELECT 
    r.Brand, 
    r.ReceiptCount AS RecentMonthCount, 
    r.Rank AS RecentMonthRank,
    p.ReceiptCount AS PreviousMonthCount, 
    p.Rank AS PreviousMonthRank
FROM 
    RecentMonthBrandCount r
    LEFT JOIN PreviousMonthBrandCount p ON r.Brand = p.Brand
WHERE 
    r.Rank <= 5
ORDER BY 
    r.Rank;

/*--- 3.When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?*/
SELECT
    rewardsReceiptStatus,
    AVG(totalSpent) AS AverageSpend
FROM
    Receipts
WHERE
    rewardsReceiptStatus IN ('Accepted', 'Rejected')
GROUP BY
    rewardsReceiptStatus;


/*----4. When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?*/
SELECT
    rewardsReceiptStatus,
    SUM(purchasedItemCount) AS TotalItemsPurchased
FROM
    Receipts
WHERE
    rewardsReceiptStatus IN ('Accepted', 'Rejected')
GROUP BY
    rewardsReceiptStatus;


/*----5.Which brand has the most spend among users who were created within the past 6 months?*/
WITH RecentUsers AS (
    SELECT _id
    FROM Users
    WHERE createdDate >= DATEADD(MONTH, -6, GETDATE())
),
UserReceipts AS (
    SELECT r.*
    FROM Receipts r
    JOIN RecentUsers u ON r.userId = u._id
),
BrandSpend AS (
    SELECT 
        b.Brand,
        SUM(i.finalPrice * i.quantityPurchased) AS TotalSpend
    FROM 
        UserReceipts r
        JOIN TransactionS t ON r._id = t.Receipt_id
        JOIN Items i ON t.Barcode = i.Barcode
        JOIN Brands b ON i.brand_id = b._id
    GROUP BY 
        b.Brand
)
SELECT 
    TOP 1 Brand, 
    TotalSpend
FROM 
    BrandSpend
ORDER BY 
    TotalSpend DESC;

/*-----6.Which brand has the most transactions among users who were created within the past 6 months?*/
WITH RecentUsers AS (
    SELECT _id
    FROM Users
    WHERE createdDate >= DATEADD(MONTH, -6, GETDATE())
),
UserTransactions AS (
    SELECT t.*
    FROM TransactionS t
    JOIN RecentUsers u ON t.User_id = u._id
),
BrandTransactions AS (
    SELECT 
        b.Brand,
        COUNT(*) AS TransactionCount
    FROM 
        UserTransactions t
        JOIN Brands b ON t.Brand_id = b._id
    GROUP BY 
        b.Brand
)
SELECT 
    Brand, 
    TransactionCount
FROM 
    BrandTransactions
ORDER BY 
    TransactionCount DESC
OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY;
