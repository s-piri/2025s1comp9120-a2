#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

'''
Connect to the database using the connection string
'''
def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE

    myHost = ""
    userid = ""
    passwd = ""
    
    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    
    # return the connection to use
    return conn

'''
Validate salesperson based on username and password
'''
def checkLogin(login, password):

    return ['jdoe', 'John', 'Doe']


"""
    Retrieves the summary of car sales.

    This method fetches the summary of car sales from the database and returns it 
    as a collection of summary objects. Each summary contains key information 
    about a particular car sale.

    :return: A list of car sale summaries.
"""
def getCarSalesSummary():
    return

"""
    Finds car sales based on the provided search string.

    This method searches the database for car sales that match the provided search 
    string. See assignment description for search specification

    :param search_string: The search string to use for finding car sales in the database.
    :return: A list of car sales matching the search string.
"""
def findCarSales(searchString):
    conn = openConnection()
    if not conn:
        return None

    cursor = conn.cursor()
    searchString = f"%{searchString}%"
    query = """
        SELECT Sales.CarSaleID,
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
            LOWER(Make.MakeName) LIKE LOWER(%s)
            OR LOWER(Model.ModelName) LIKE LOWER(%s)
            OR LOWER(C.FirstName) LIKE LOWER(%s) 
            OR LOWER(C.LastName) LIKE LOWER(%s)
            OR LOWER(S.FirstName) LIKE LOWER(%s)
            OR LOWER(S.LastName) LIKE LOWER(%s)
            OR LOWER(C.FirstName || ' ' || C.LastName) LIKE LOWER(%s)
            OR LOWER(S.FirstName || ' ' || S.LastName) LIKE LOWER(%s)
        )
        AND (
            Sales.IsSold = FALSE
            OR (Sales.IsSold = TRUE AND Sales.SaleDate >= CURRENT_DATE - INTERVAL '3 years')
        )
        ORDER BY Sales.IsSold ASC, 
                Sales.SaleDate ASC NULLS FIRST, 
                Make.MakeName ASC, 
                Model.ModelName ASC;
    """
    cursor.execute(query, [searchString] * 8)
    res = cursor.fetchall() 
    attributes = ['carsale_id', 'make', 'model', 'builtYear', 'odometer', 'price', 'isSold', 'sale_date', 'buyer', 'salesperson']  
    res = [dict(zip(attributes, row)) for row in res]
    cursor.close()
    conn.close()

    return res

"""
    Adds a new car sale to the database.

    This method accepts a CarSale object, which contains all the necessary details 
    for a new car sale. It inserts the data into the database and returns a confirmation 
    of the operation.

    :param car_sale: The CarSale object to be added to the database.
    :return: A boolean indicating if the operation was successful or not.
"""
def addCarSale(make, model, builtYear, odometer, price):
    return

"""
    Updates an existing car sale in the database.

    This method updates the details of a specific car sale in the database, ensuring
    that all fields of the CarSale object are modified correctly. It assumes that 
    the car sale to be updated already exists.

    :param car_sale: The CarSale object containing updated details for the car sale.
    :return: A boolean indicating whether the update was successful or not.
"""
def updateCarSale(carsaleid, customer, salesperosn, saledate):
    return
