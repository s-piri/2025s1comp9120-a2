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
    conn = openConnection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT username, firstname, lastname
            FROM Salesperson
            WHERE LOWER(username) = LOWER(%s) AND password = %s
        """, (login, password))
        result = cur.fetchone()
        if result:
            return list(result)
        else:
            return None
    except Exception as e:
        print("Error during login:", e)
        return None
    finally:
        cur.close()
        conn.close()

"""
    Retrieves the summary of car sales.

    This method fetches the summary of car sales from the database and returns it 
    as a collection of summary objects. Each summary contains key information 
    about a particular car sale.

    :return: A list of car sale summaries.
"""
def getCarSalesSummary():
    conn = openConnection()
    if not conn:
        return []

    cur = conn.cursor()
    query = """
        SELECT
            mk.MakeName AS make,
            md.ModelName AS model,
            COUNT(CASE WHEN cs.IsSold = FALSE THEN 1 END) AS available_units,
            COUNT(CASE WHEN cs.IsSold = TRUE THEN 1 END) AS sold_units,
            COALESCE(SUM(CASE WHEN cs.IsSold = TRUE THEN cs.Price END), 0) AS total_sales,
            COALESCE(MAX(CASE WHEN cs.IsSold = TRUE THEN TO_CHAR(cs.SaleDate, 'DD-MM-YYYY') END), '') AS last_purchased_at
        FROM
            CarSales cs
            JOIN Make mk ON cs.MakeCode = mk.MakeCode
            JOIN Model md ON cs.ModelCode = md.ModelCode
        GROUP BY
            mk.MakeName, md.ModelName
        ORDER BY
            mk.MakeName ASC, md.ModelName ASC;
    """
    cur.execute(query)
    results = cur.fetchall()
    summary = []
    for row in results:
        total_sales = row[4]
        last_purchased_at = row[5]
        
        summary.append({
            "make": row[0],
            "model": row[1],
            "availableUnits": row[2],
            "soldUnits": row[3],
            "soldTotalPrices": total_sales,
            "lastPurchaseAt": last_purchased_at
        })
    cur.close()
    conn.close()
    return summary

"""
    Finds car sales based on the provided search string.

    This method searches the database for car sales that match the provided search 
    string. See assignment description for search specification

    :param search_string: The search string to use for finding car sales in the database.
    :return: A list of car sales matching the search string.
"""
def findCarSales(searchString):
    try:
        conn = openConnection()
        if not conn:
            return None

        cursor = conn.cursor()
        cursor.callproc("find_car_sales", [searchString])
        res = cursor.fetchall()
        if res == []:
            return None

        attributes = ['carsale_id', 'make', 'model', 'builtYear', 'odometer', 'price', 'isSold', 'sale_date', 'buyer', 'salesperson']  
        res = [dict(zip(attributes, row)) for row in res]
        
        return res

    except Exception as e:
        print(f"Exception: {e}")
        return None
    
    finally:
        cursor.close()
        conn.close()

"""
    Adds a new car sale to the database.

    This method accepts a CarSale object, which contains all the necessary details 
    for a new car sale. It inserts the data into the database and returns a confirmation 
    of the operation.

    :param car_sale: The CarSale object to be added to the database.
    :return: A boolean indicating if the operation was successful or not.
"""
def addCarSale(make, model, builtYear, odometer, price):
    try:
        conn = openConnection()
        if not conn:
            return False
        curs = conn.cursor() 
        curs.callproc("addCarSale", [make, model, builtYear, odometer, price])
        conn.commit()
        output = curs.fetchone()
        return output[0]
    
    except Exception as e:
        print(f"Exception: {e}")
        return False
    
    finally:
        curs.close()
        conn.close()

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