import pytest
from datetime import datetime
from decimal import Decimal
from database import findCarSales  # Replace with the actual module name

# ---------- VALID CASES ----------

# Testing the search function is connected to database and is producing accurate result. 
# Is not dynamic, manually inserted expected data
# If this fails, all other tests may not be accurate
def test_search_function():
    expected = [
        {'carsale_id': 6, 'make': 'Volkswagen', 'model': 'Golf', 'builtYear': 2023, 'odometer': 22000, 'price': Decimal('33000.00'), 'isSold': True, 'sale_date': '06-11-2023', 'buyer': 'Laura Roberts', 'salesperson': 'John Doe'}, 
        {'carsale_id': 1, 'make': 'Mercedes Benz', 'model': 'C Class', 'builtYear': 2020, 'odometer': 64210, 'price': Decimal('72000.00'), 'isSold': True, 'sale_date': '01-03-2024', 'buyer': 'David Wilson', 'salesperson': 'John Doe'}, 
        {'carsale_id': 4, 'make': 'Toyota', 'model': 'Corolla', 'builtYear': 2022, 'odometer': 65000, 'price': Decimal('35000.00'), 'isSold': True, 'sale_date': '21-09-2024', 'buyer': 'Grace Thomas', 'salesperson': 'John Doe'}, 
        {'carsale_id': 10, 'make': 'Mercedes Benz', 'model': 'A Class', 'builtYear': 2022, 'odometer': 47000, 'price': Decimal('57000.00'), 'isSold': True, 'sale_date': '01-03-2025', 'buyer': 'Frank Anderson', 'salesperson': 'John Doe'}
    ]
    assert findCarSales("John Doe") == expected
    
@pytest.mark.parametrize("query", [
    "mercedes benz", 
    "MERCEDES BENZ"
])
def test_case_insensitive_make_name(query):
    expected = findCarSales("Mercedes Benz")  # trusted reference
    assert findCarSales(query) == expected

@pytest.mark.parametrize("query", [
    "a class", 
    "A CLASS"
])
def test_case_insensitive_model_name(query):
    expected = findCarSales("A Class")  # trusted reference
    assert findCarSales(query) == expected

@pytest.mark.parametrize("query", [
    "david wilson", 
    "david",
    "wilson"
])
def test_case_buyer_name(query):
    expected = findCarSales("David Wilson")  # trusted reference
    assert findCarSales(query) == expected

@pytest.mark.parametrize("query", [
    "john doe", 
    "john",
    "doe"
])
def test_case_salesperson_name(query):
    expected = findCarSales("John Doe")  # trusted reference
    assert findCarSales(query) == expected

def test_ordering_of_findCarSales_results():
    results = findCarSales("toyota")

    # Step 1: Split into unsold and sold
    unsold = [r for r in results if not r['isSold']]
    sold = [r for r in results if r['isSold']]

    # ✅ Check unsold appear first
    assert results[:len(unsold)] == unsold
    assert results[len(unsold):] == sold

    # ✅ Check sold cars are ordered by SaleDate ASC
    sale_dates = [datetime.strptime(r['sale_date'], "%d-%m-%Y") for r in sold if r['sale_date']]
    assert sale_dates == sorted(sale_dates)

    # ✅ Check each group is sorted by Make then Model
    def make_model_key(r):
        return (r['make'].lower(), r['model'].lower())

    unsold_sorted = sorted(unsold, key=make_model_key)
    sold_sorted = sorted(sold, key=make_model_key)

    assert unsold == unsold_sorted
    assert sold == sold_sorted

def test_sold_cars_within_3_years():
    result = findCarSales("A Class")  # Replace with the actual call

    today = datetime.today()
    for car in result:
        if car["isSold"]:
            sale_date_str = car["sale_date"]
            assert sale_date_str != '', "Sold car must have a sale_date"
            sale_date = datetime.strptime(sale_date_str, "%d-%m-%Y")
            age_in_days = (today - sale_date).days
            assert age_in_days <= 3 * 365, f"Sold car {car} is older than 3 years"

def test_findCarSale_sale_date_format():
    result = findCarSales("John Doe")  # Replace with actual call

    for car in result:
        sale_date = car.get("sale_date", "")
        if sale_date:  # Only validate non-empty sale dates
            try:
                datetime.strptime(sale_date, "%d-%m-%Y")
            except ValueError:
                pytest.fail(f"Invalid sale_date format: {sale_date} in car {car}")

# ---------- INVALID CASES ----------

@pytest.mark.parametrize("query", [
    "Mercedes", 
    "M"
])
def test_partial_keyword_make(query):
    assert findCarSales(query) is None

@pytest.mark.parametrize("query", [
    "Joh", 
    "Do"
])
def test_partial_keyword_model(query):
    assert findCarSales(query) is None




