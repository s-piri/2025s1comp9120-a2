SET datestyle = 'ISO, DMY';
DROP TABLE IF EXISTS Make CASCADE;
DROP TABLE IF EXISTS Model CASCADE;
DROP TABLE IF EXISTS Salesperson CASCADE;
DROP TABLE IF EXISTS Customer CASCADE;
DROP TABLE IF EXISTS CarSales CASCADE;
DROP FUNCTION IF EXISTS find_car_sales(TEXT);
DROP FUNCTION IF EXISTS check_future_saledate;
DROP FUNCTION IF EXISTS updateCarSale;
DROP FUNCTION IF EXISTS addCarSale;
DROP FUNCTION IF EXISTS update_isSold;
DROP FUNCTION IF EXISTS check_positive_price;
DROP FUNCTION IF EXISTS check_positive_odometer;

CREATE TABLE Salesperson (
    UserName VARCHAR(10) PRIMARY KEY,
    Password VARCHAR(20) NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
	UNIQUE(FirstName, LastName)
);

INSERT INTO Salesperson VALUES 
('jdoe', 'Pass1234', 'John', 'Doe'),
('brown', 'Passwxyz', 'Bob', 'Brown'),
('ksmith1', 'Pass5566', 'Karen', 'Smith');

CREATE TABLE Customer (
    CustomerID VARCHAR(10) PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Mobile VARCHAR(20) NOT NULL
);

INSERT INTO Customer VALUES 
('c001', 'David', 'Wilson', '4455667788'),
('c899', 'Eva', 'Taylor', '5566778899'),
('c199',  'Frank', 'Anderson', '6677889900'),
('c910', 'Grace', 'Thomas', '7788990011'),
('c002',  'Stan', 'Martinez', '8899001122'),
('c233', 'Laura', 'Roberts', '9900112233'),
('c123', 'Charlie', 'Davis', '7712340011'),
('c321', 'Jane', 'Smith', '9988990011'),
('c211', 'Alice', 'Johnson', '7712222221');

CREATE TABLE Make (
    MakeCode VARCHAR(5) PRIMARY KEY,
    MakeName VARCHAR(20) UNIQUE NOT NULL
);

INSERT INTO Make VALUES ('MB', 'Mercedes Benz');
INSERT INTO Make VALUES ('TOY', 'Toyota');
INSERT INTO Make VALUES ('VW', 'Volkswagen');
INSERT INTO Make VALUES ('LEX', 'Lexus');
INSERT INTO Make VALUES ('LR', 'Land Rover');

CREATE TABLE Model (
    ModelCode VARCHAR(10) PRIMARY KEY,
    ModelName VARCHAR(20) UNIQUE NOT NULL,
    MakeCode VARCHAR(10) NOT NULL,  
    FOREIGN KEY (MakeCode) REFERENCES Make(MakeCode)
);

INSERT INTO Model (ModelCode, ModelName, MakeCode) VALUES
('aclass', 'A Class', 'MB'),
('cclass', 'C Class', 'MB'),
('eclass', 'E Class', 'MB'),
('camry', 'Camry', 'TOY'),
('corolla', 'Corolla', 'TOY'),
('rav4', 'RAV4', 'TOY'),
('defender', 'Defender', 'LR'),
('rangerover', 'Range Rover', 'LR'),
('discosport', 'Discovery Sport', 'LR'),
('golf', 'Golf', 'VW'),
('passat', 'Passat', 'VW'),
('troc', 'T Roc', 'VW'),
('ux', 'UX', 'LEX'),
('gx', 'GX', 'LEX'),
('nx', 'NX', 'LEX');

CREATE TABLE CarSales (
  CarSaleID SERIAL primary key,
  MakeCode VARCHAR(10) NOT NULL REFERENCES Make(MakeCode),
  ModelCode VARCHAR(10) NOT NULL REFERENCES Model(ModelCode),
  BuiltYear INTEGER NOT NULL CHECK (BuiltYear BETWEEN 1950 AND EXTRACT(YEAR FROM CURRENT_DATE)),
  Odometer INTEGER NOT NULL,
  Price Decimal(10,2) NOT NULL,
  IsSold Boolean NOT NULL,
  BuyerID VARCHAR(10) REFERENCES Customer,
  SalespersonID VARCHAR(10) REFERENCES Salesperson,
  SaleDate Date
);

INSERT INTO CarSales (MakeCode, ModelCode, BuiltYear, Odometer, Price, IsSold, BuyerID, SalespersonID, SaleDate) VALUES
('MB', 'cclass', 2020, 64210, 72000.00, TRUE, 'c001', 'jdoe', '01/03/2024'),
('MB', 'eclass', 2019, 31210, 89000.00, FALSE, NULL, NULL, NULL),
('TOY', 'camry', 2021, 98200, 37200.00, TRUE, 'c123', 'brown', '07/12/2023'),
('TOY', 'corolla', 2022, 65000, 35000.00, TRUE, 'c910', 'jdoe', '21/09/2024'),
('LR', 'defender', 2018, 115000, 97000.00, FALSE, NULL, NULL, NULL),
('VW', 'golf', 2023, 22000, 33000.00, TRUE, 'c233', 'jdoe', '06/11/2023'),
('LEX', 'nx', 2020, 67000, 79000.00, TRUE, 'c321', 'brown', '01/01/2025'),
('LR', 'discosport', 2021, 43080, 85000.00, TRUE, 'c211', 'ksmith1', '27/01/2021'),
('TOY', 'rav4', 2019, 92900, 48000.00, FALSE, NULL, NULL, NULL),
('MB', 'aclass', 2022, 47000, 57000.00, TRUE, 'c199', 'jdoe', '01/03/2025'),
('LEX', 'ux', 2023, 23000, 70000.00, TRUE, 'c899', 'brown', '01/01/2023'),
('VW', 'passat', 2020, 63720, 42000.00, FALSE, NULL, NULL, NULL),
('MB', 'eclass', 2021, 12000, 155000.00, TRUE, 'c002', 'ksmith1', '01/10/2024'),
('LR', 'rangerover', 2017, 60000, 128000.00, FALSE, NULL, NULL, NULL),
('TOY', 'camry', 2025, 10, 49995.00, FALSE, NULL, NULL, NULL),
('LR', 'discosport', 2022, 53000, 89900.00, FALSE, NULL, NULL, NULL),
('MB', 'cclass', 2023, 55000, 82100.00, FALSE, NULL, NULL, NULL),
('MB', 'aclass', 2025, 5, 78000.00, FALSE, NULL, NULL, NULL),
('MB', 'aclass', 2015, 8912, 12000.00, TRUE, 'c199', 'jdoe', '11/03/2020'),
('TOY', 'camry', 2024, 21000, 42000.00, FALSE, NULL, NULL, NULL),
('LEX', 'gx', 2025, 6, 128085.00, FALSE, NULL, NULL, NULL),
('MB', 'eclass', 2019, 99220, 105000.00, FALSE, NULL, NULL, NULL),
('VW', 'golf', 2023, 53849, 43000.00, FALSE, NULL, NULL, NULL),
('MB', 'cclass', 2022, 89200, 62000.00, FALSE, NULL, NULL, NULL);

CREATE OR REPLACE FUNCTION updateCarSale(
	IN in_carsaleid INT, 
	IN in_customer VARCHAR, 
	IN in_salesperson VARCHAR, 
	IN in_saledate TEXT, 
	OUT result BOOLEAN) AS $$
    DECLARE
        l_customer VARCHAR;
        l_salesperson VARCHAR;
        format_saledate DATE;
    BEGIN
        l_customer := LOWER(in_customer);
        l_salesperson := LOWER(in_salesperson);
        format_saledate := TO_DATE(in_saledate, 'YYYY-MM-DD');
        
        IF l_customer = '' THEN
            l_customer := NULL;
        END IF;
        IF l_salesperson = '' THEN
            l_salesperson := NULL;
        END IF;

        IF format_saledate > CURRENT_DATE AND format_saledate is not NULL THEN 
            result := FALSE;
        ELSIF NOT EXISTS (SELECT * FROM Customer c WHERE LOWER(c.CustomerID)=l_customer) AND l_customer is not NULL THEN 
            result := FALSE;
        ELSIF NOT EXISTS (SELECT * FROM Salesperson s WHERE LOWER(s.UserName)=l_salesperson) AND l_salesperson is not NULL THEN 
            result := FALSE;
        ELSIF NOT EXISTS (SELECT * FROM CarSales cs WHERE cs.CarSaleID=in_carsaleid) THEN result := FALSE;
        ELSE
            UPDATE CarSales -- Seems UPDATE can't be use with alias :/ 
            SET IsSold=TRUE, BuyerID=l_customer, SalespersonID=l_salesperson, SaleDate=format_saledate
            WHERE CarSales.CarSaleID=in_carsaleid;
            result := TRUE;
        END IF;
    END; $$
 LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION addCarSale(
	IN in_makename VARCHAR, 
	IN in_modelname VARCHAR, 
	IN in_builtyear INT, 
	IN in_odometer INT,
    IN in_price DECIMAL, 
	OUT result BOOLEAN) AS $$
    DECLARE
        res_makecode VARCHAR;
        res_modelcode VARCHAR;
    BEGIN
        SELECT ma.MakeCode, mo.ModelCode
        INTO res_makecode, res_modelcode
        FROM Make ma JOIN Model mo ON LOWER(ma.MakeCode) = LOWER(mo.MakeCode)
        WHERE LOWER(ma.MakeName) = LOWER(in_makename)
        AND LOWER(mo.ModelName) = LOWER(in_modelname);
        -- JOIN make and model to check that the model belong in the make!

        IF res_makecode IS NULL OR res_modelcode IS NULL THEN
            result := FALSE;
        ELSE
			BEGIN
	            INSERT INTO 
	                CarSales (MakeCode, ModelCode, BuiltYear, Odometer, Price, IsSold, BuyerID, SalespersonID, SaleDate)
	            VALUES 
	                (res_makecode, res_modelcode, in_builtyear, in_odometer, in_price, False, NULL, NULL, NULL);
	                result := TRUE;
	            EXCEPTION WHEN OTHERS THEN  -- Catch cases where price <=0 or odometer <= 0 or builtyear < 1950 which lead to INSERT failure
	                    result := FALSE;
			END;
        END IF;
    END; $$
 LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_future_saledate() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.SaleDate <= CURRENT_DATE OR NEW.SaleDate is NULL THEN
        RETURN NEW;
    ELSE
        RAISE EXCEPTION 'Sale date cannot be in the future';
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_check_future_saledate
BEFORE INSERT OR UPDATE ON CarSales --Must check before insert to prevent invalid data!
FOR EACH ROW
    EXECUTE FUNCTION check_future_saledate ();

CREATE OR REPLACE FUNCTION update_isSold() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.BuyerID IS NOT NULL
       AND NEW.SalespersonID IS NOT NULL
       AND NEW.SaleDate <= CURRENT_DATE THEN
        NEW.IsSold := TRUE;
    ELSE
        NEW.IsSold := FALSE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_update_isSold
BEFORE INSERT OR UPDATE ON CarSales --Actually have to use BEFORE, because AFTER can't modify NEW
FOR EACH ROW
    EXECUTE FUNCTION update_isSold ();

CREATE OR REPLACE FUNCTION check_positive_odometer () RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.Odometer <= 0 THEN
            RAISE EXCEPTION 'Odometer value must be positive';
        END IF;
        RETURN NEW;
    END;   
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_positive_price () RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.Price <= 0 THEN
            RAISE EXCEPTION 'Price value must be positive';
        END IF;
        RETURN NEW;
    END;   
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_odometer_must_be_positive
BEFORE INSERT OR UPDATE ON CarSales
FOR EACH ROW
    EXECUTE FUNCTION check_positive_odometer();

CREATE OR REPLACE TRIGGER trg_price_must_be_positive
BEFORE INSERT OR UPDATE ON CarSales
FOR EACH ROW
    EXECUTE FUNCTION check_positive_price();

CREATE OR REPLACE FUNCTION find_car_sales(search_text TEXT)
RETURNS TABLE (
    carsale_id INT,
    make VARCHAR,
    model VARCHAR,
    builtYear INT,
    odometer INT,
    price NUMERIC,
    isSold BOOLEAN,
    sale_date TEXT,
    buyer TEXT,
    salesperson TEXT
) AS $$
DECLARE
    keyword TEXT;
BEGIN
    keyword := '%' || LOWER(search_text) || '%';
    RAISE NOTICE 'Searching with keyword: %', keyword;
    RETURN QUERY
    SELECT
        Sales.CarSaleID,
        Make.MakeName,
        Model.ModelName,
        Sales.BuiltYear,
        Sales.Odometer,
        Sales.Price,
        Sales.IsSold,
        COALESCE(TO_CHAR(Sales.SaleDate, 'DD-MM-YYYY'), '') AS SaleDate,
        COALESCE(C.FirstName || ' ' || C.LastName, '') AS Buyer,
        COALESCE(S.FirstName || ' ' || S.LastName, '') AS Salesperson
    FROM CarSales Sales
        JOIN Make ON Make.MakeCode = Sales.MakeCode 
        JOIN Model ON Model.ModelCode = Sales.ModelCode
        LEFT JOIN Customer C ON C.CustomerID = Sales.BuyerID
        LEFT JOIN Salesperson S ON S.UserName = Sales.SalespersonID
    WHERE (
        LOWER(Make.MakeName) LIKE keyword
        OR LOWER(Model.ModelName) LIKE keyword
        OR LOWER(C.FirstName) LIKE keyword
        OR LOWER(C.LastName) LIKE keyword
        OR LOWER(S.FirstName) LIKE keyword
        OR LOWER(S.LastName) LIKE keyword
        OR LOWER(C.FirstName || ' ' || C.LastName) LIKE keyword
        OR LOWER(S.FirstName || ' ' || S.LastName) LIKE keyword
    )
    AND (
        Sales.IsSold = FALSE
        OR (Sales.IsSold = TRUE AND Sales.SaleDate >= CURRENT_DATE - INTERVAL '3 years')
    )
    ORDER BY Sales.IsSold ASC, 
             Sales.SaleDate ASC NULLS FIRST, 
             Make.MakeName ASC, 
             Model.ModelName ASC;
END;
$$ LANGUAGE plpgsql;
