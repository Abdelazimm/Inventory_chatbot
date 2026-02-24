import textwrap

SQL_SERVER_SCHEMA = """
CREATE TABLE Customers ( CustomerId INT IDENTITY PRIMARY KEY, CustomerCode VARCHAR(50) UNIQUE NOT
NULL, CustomerName NVARCHAR(200) NOT NULL, Email NVARCHAR(200) NULL, Phone NVARCHAR(50) NULL,
BillingAddress1 NVARCHAR(200) NULL, BillingCity NVARCHAR(100) NULL, BillingCountry NVARCHAR(100) NULL,
CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(), UpdatedAt DATETIME2 NULL, IsActive BIT NOT
NULL DEFAULT 1 );
CREATE TABLE Vendors ( VendorId INT IDENTITY PRIMARY KEY, VendorCode VARCHAR(50) UNIQUE NOT NULL,
VendorName NVARCHAR(200) NOT NULL, Email NVARCHAR(200) NULL, Phone NVARCHAR(50) NULL,
AddressLine1 NVARCHAR(200) NULL, City NVARCHAR(100) NULL, Country NVARCHAR(100) NULL, CreatedAt
DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(), UpdatedAt DATETIME2 NULL, IsActive BIT NOT NULL
DEFAULT 1 );
CREATE TABLE Sites ( SiteId INT IDENTITY PRIMARY KEY, SiteCode VARCHAR(50) UNIQUE NOT NULL, SiteName
NVARCHAR(200) NOT NULL, AddressLine1 NVARCHAR(200) NULL, City NVARCHAR(100) NULL, Country
NVARCHAR(100) NULL, TimeZone NVARCHAR(100) NULL, CreatedAt DATETIME2 NOT NULL DEFAULT
SYSUTCDATETIME(), UpdatedAt DATETIME2 NULL, IsActive BIT NOT NULL DEFAULT 1 );
CREATE TABLE Locations ( LocationId INT IDENTITY PRIMARY KEY, SiteId INT NOT NULL, LocationCode
VARCHAR(50) NOT NULL, LocationName NVARCHAR(200) NOT NULL, ParentLocationId INT NULL, CreatedAt
DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(), UpdatedAt DATETIME2 NULL, IsActive BIT NOT NULL
DEFAULT 1, CONSTRAINT UQ_Locations_SiteCode UNIQUE (SiteId, LocationCode), CONSTRAINT
Assignment by Hady Rashad - DataHub
Inventory Chatbot with "Present Query" Output
FK_Locations_Site FOREIGN KEY (SiteId) REFERENCES Sites(SiteId), CONSTRAINT FK_Locations_Parent
FOREIGN KEY (ParentLocationId) REFERENCES Locations(LocationId) );
CREATE TABLE Items ( ItemId INT IDENTITY PRIMARY KEY, ItemCode NVARCHAR(100) UNIQUE NOT NULL,
ItemName NVARCHAR(200) NOT NULL, Category NVARCHAR(100) NULL, UnitOfMeasure NVARCHAR(50) NULL,
CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(), UpdatedAt DATETIME2 NULL, IsActive BIT NOT
NULL DEFAULT 1 );
CREATE TABLE Assets ( AssetId INT IDENTITY PRIMARY KEY, AssetTag VARCHAR(100) UNIQUE NOT NULL,
AssetName NVARCHAR(200) NOT NULL, SiteId INT NOT NULL, LocationId INT NULL, SerialNumber
NVARCHAR(200) NULL, Category NVARCHAR(100) NULL, Status VARCHAR(30) NOT NULL DEFAULT 'Active', Cost
DECIMAL(18,2) NULL, PurchaseDate DATE NULL, VendorId INT NULL, CreatedAt DATETIME2 NOT NULL DEFAULT
SYSUTCDATETIME(), UpdatedAt DATETIME2 NULL, CONSTRAINT FK_Assets_Site FOREIGN KEY (SiteId)
REFERENCES Sites(SiteId), CONSTRAINT FK_Assets_Location FOREIGN KEY (LocationId) REFERENCES
Locations(LocationId), CONSTRAINT FK_Assets_Vendor FOREIGN KEY (VendorId) REFERENCES
Vendors(VendorId) );
CREATE TABLE Bills ( BillId INT IDENTITY PRIMARY KEY, VendorId INT NOT NULL, BillNumber VARCHAR(100)
NOT NULL, BillDate DATE NOT NULL, DueDate DATE NULL, TotalAmount DECIMAL(18,2) NOT NULL, Currency
VARCHAR(10) NOT NULL DEFAULT 'USD', Status VARCHAR(30) NOT NULL DEFAULT 'Open', CreatedAt
DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(), UpdatedAt DATETIME2 NULL, CONSTRAINT
UQ_Bills_Vendor_BillNumber UNIQUE (VendorId, BillNumber), CONSTRAINT FK_Bills_Vendor FOREIGN KEY
(VendorId) REFERENCES Vendors(VendorId) );
CREATE TABLE PurchaseOrders ( POId INT IDENTITY PRIMARY KEY, PONumber VARCHAR(100) NOT NULL,
VendorId INT NOT NULL, PODate DATE NOT NULL, Status VARCHAR(30) NOT NULL DEFAULT 'Open', SiteId INT
NULL, CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(), UpdatedAt DATETIME2 NULL,
CONSTRAINT UQ_PurchaseOrders_Number UNIQUE (PONumber), CONSTRAINT FK_PurchaseOrders_Vendor
FOREIGN KEY (VendorId) REFERENCES Vendors(VendorId), CONSTRAINT FK_PurchaseOrders_Site FOREIGN
KEY (SiteId) REFERENCES Sites(SiteId) );
CREATE TABLE PurchaseOrderLines ( POLineId INT IDENTITY PRIMARY KEY, POId INT NOT NULL, LineNumber
INT NOT NULL, ItemId INT NULL, ItemCode NVARCHAR(100) NOT NULL, Description NVARCHAR(200) NULL,
Quantity DECIMAL(18,4) NOT NULL, UnitPrice DECIMAL(18,4) NOT NULL, CONSTRAINT UQ_PurchaseOrderLines
UNIQUE (POId, LineNumber), CONSTRAINT FK_PurchaseOrderLines_PO FOREIGN KEY (POId) REFERENCES
PurchaseOrders(POId), CONSTRAINT FK_PurchaseOrderLines_Item FOREIGN KEY (ItemId) REFERENCES
Items(ItemId) );
CREATE TABLE SalesOrders ( SOId INT IDENTITY PRIMARY KEY, SONumber VARCHAR(100) NOT NULL,
CustomerId INT NOT NULL, SODate DATE NOT NULL, Status VARCHAR(30) NOT NULL DEFAULT 'Open', SiteId INT
NULL, CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(), UpdatedAt DATETIME2 NULL,
CONSTRAINT UQ_SalesOrders_Number UNIQUE (SONumber), CONSTRAINT FK_SalesOrders_Customer FOREIGN
KEY (CustomerId) REFERENCES Customers(CustomerId), CONSTRAINT FK_SalesOrders_Site FOREIGN KEY
(SiteId) REFERENCES Sites(SiteId) );
CREATE TABLE SalesOrderLines ( SOLineId INT IDENTITY PRIMARY KEY, SOId INT NOT NULL, LineNumber INT
NOT NULL, ItemId INT NULL, ItemCode NVARCHAR(100) NOT NULL, Description NVARCHAR(200) NULL, Quantity
DECIMAL(18,4) NOT NULL, UnitPrice DECIMAL(18,4) NOT NULL, CONSTRAINT UQ_SalesOrderLines UNIQUE
Assignment by Hady Rashad - DataHub
Inventory Chatbot with "Present Query" Output
(SOId, LineNumber), CONSTRAINT FK_SalesOrderLines_SO FOREIGN KEY (SOId) REFERENCES
SalesOrders(SOId), CONSTRAINT FK_SalesOrderLines_Item FOREIGN KEY (ItemId) REFERENCES Items(ItemId) );
CREATE TABLE AssetTransactions ( AssetTxnId INT IDENTITY PRIMARY KEY, AssetId INT NOT NULL,
FromLocationId INT NULL, ToLocationId INT NULL, TxnType VARCHAR(30) NOT NULL, Quantity INT NOT NULL
DEFAULT 1, TxnDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(), Note NVARCHAR(500) NULL,
CONSTRAINT FK_AssetTransactions_Asset FOREIGN KEY (AssetId) REFERENCES Assets(AssetId), CONSTRAINT
FK_AssetTransactions_FromLoc FOREIGN KEY (FromLocationId) REFERENCES Locations(LocationId),
CONSTRAINT FK_AssetTransactions_ToLoc FOREIGN KEY (ToLocationId) REFERENCES Locations(LocationId) );
"""

SAMPLE_DATA = """
For additional context on how the tables are populated, here are some sample data instances representing typical operational scenarios.

[Customers]
CustomerId: 1 | CustomerCode: 'CUST-001' | CustomerName: 'Acme Corp' | IsActive: 1
CustomerId: 2 | CustomerCode: 'CUST-002' | CustomerName: 'Global Tech' | IsActive: 1

[Vendors]
VendorId: 1 | VendorCode: 'V-APPLE' | VendorName: 'Apple Inc.' | City: 'Cupertino'
VendorId: 2 | VendorCode: 'V-DELL' | VendorName: 'Dell Technologies' | City: 'Round Rock'
VendorId: 3 | VendorCode: 'V-CISCO' | VendorName: 'Cisco Systems' | City: 'San Jose'

[Sites]
SiteId: 1 | SiteCode: 'HQ' | SiteName: 'Main Headquarters' | City: 'New York' 
SiteId: 2 | SiteCode: 'EU-01' | SiteName: 'London Branch' | City: 'London'

[Assets]
AssetId: 1 | AssetTag: 'AST-5001' | AssetName: 'MacBook Pro 16"' | SiteId: 1 | Category: 'IT Equipment' | Status: 'Active' | Cost: 2500.00 | PurchaseDate: '2024-01-15' | VendorId: 1
AssetId: 2 | AssetTag: 'AST-5002' | AssetName: 'Dell XPS 15' | SiteId: 2 | Category: 'IT Equipment' | Status: 'Active' | Cost: 1800.00 | PurchaseDate: '2024-03-10' | VendorId: 2
AssetId: 3 | AssetTag: 'AST-5003' | AssetName: 'Cisco Router ASR' | SiteId: 1 | Category: 'Network' | Status: 'Active' | Cost: 4500.00 | PurchaseDate: '2023-11-05' | VendorId: 3

[Bills]
BillId: 101 | VendorId: 1 | BillNumber: 'INV-A-100' | BillDate: '2024-01-15' | TotalAmount: 25000.00 | Status: 'Paid'
BillId: 102 | VendorId: 2 | BillNumber: 'INV-D-202' | BillDate: '2024-04-01' | TotalAmount: 18000.00 | Status: 'Open'
BillId: 103 | VendorId: 3 | BillNumber: 'INV-C-305' | BillDate: '2024-02-20' | TotalAmount: 45000.00 | Status: 'Paid'

[PurchaseOrders]
POId: 1 | PONumber: 'PO-2024-001' | VendorId: 2 | PODate: '2024-05-10' | Status: 'Open' | SiteId: 1
POId: 2 | PONumber: 'PO-2024-002' | VendorId: 1 | PODate: '2024-05-12' | Status: 'Pending Approval' | SiteId: 2

[SalesOrders]
SOId: 1 | SONumber: 'SO-1001' | CustomerId: 1 | SODate: '2024-05-01' | Status: 'Shipped' | SiteId: 1
SOId: 2 | SONumber: 'SO-1002' | CustomerId: 2 | SODate: '2024-04-15' | Status: 'Open' | SiteId: 2
"""

SYSTEM_PROMPT = textwrap.dedent(f"""\
    You are an expert AI inventory and business data analyst. Your goal is to answer questions about inventory and business operations based on the provided SQL Server database schema.
    
    You must output a JSON object containing two fields:
    1. "natural_language_answer": A clear, concise, and helpful answer to the user's question, PRETENDING you found the exact answer by using dummy data or placeholders. 
       - If the user asks for a specific number (Count, Sum), respond with something like: "You have {{value}} items."
       - If the user asks for a LIST of items (e.g. "list all my customers"), DO NOT just say "Here is the list." Instead, generate a small, realistic markdown table with 2-3 sample rows representing what the data would look like based on the SCHEMA and SAMPLE DATA.
    2. "sql_query": The exact, valid SQL Server (T-SQL) query that would retrieve the answer to the user's question from the database. Ensure the query is optimized and correct.

    Here are some examples:
    User: 'How many assets do I have?'
    JSON:
    {{
      "natural_language_answer": "You have {{value}} assets in your inventory.",
      "sql_query": "SELECT COUNT(*) AS AssetCount FROM Assets WHERE Status <> 'Disposed';"
    }}

    User: 'List all my customers'
    JSON:
    {{
      "natural_language_answer": "Here is the list of your customers:\\n| Customer Code | Customer Name |\\n|---|---|\\n| CUST-001 | Acme Corp |\\n| CUST-002 | Global Tech |",
      "sql_query": "SELECT CustomerCode, CustomerName FROM Customers WHERE IsActive = 1;"
    }}

    Make sure your SQL syntax strictly matches Microsoft SQL Server (T-SQL).

    DATABASE SCHEMA:
    {SQL_SERVER_SCHEMA}

    SAMPLE DATA INSTANCES:
    {SAMPLE_DATA}
""")
