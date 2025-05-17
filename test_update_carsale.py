import pytest
from datetime import date, timedelta
from database import updateCarSale, findCarSales

def find_matching_carsale(search_str, expected_id):
    results = findCarSales(search_str)
    if results is None:
        return None
    for row in results:
        if row["carsale_id"] == expected_id:
            return row
    return None

@pytest.mark.parametrize("carsaleid, customer, salesperson, saledate, expected_result, expected_search, expect_in_db", [
    # Test Case 1: Valid update
    (5, 'c001', 'jdoe', '01-03-2024', True, 'defender', {
        'buyer': 'david wilson', 'salesperson': 'john doe', 'isSold': True, 'sale_date': '01-03-2024'
    }),

    # Test Case 2: Empty customer → buyer:='' and not sold
    (5, '', 'jdoe', '01-03-2024', True, 'defender', {
        'buyer': '', 'salesperson': 'john doe', 'isSold': False, 'sale_date': '01-03-2024'
    }),

    # Test Case 3: Empty salesperson → salesperson:='' and not sold
    (5, '', '', '01-03-2024', True, 'defender', {
        'buyer': '', 'salesperson': '', 'isSold': False, 'sale_date': '01-03-2024'
    }),

    # Test Case 4: Empty saledate → saledate:='' and not sold
    (5, '', '', None, True, 'defender', {
        'buyer': '', 'salesperson': '', 'isSold': False, 'sale_date': ''
    }),
    # Test Case 5: Invalid customer ID (not in database) -> invalid -> no update
    (5, 'invalidID', 'jdoe', '01-03-2024', False, 'defender', {
        'buyer': '', 'salesperson': '', 'isSold': False, 'sale_date': ''
    }),

    # Test Case 6: Invalid salesperson -> no update
    (5, 'c001', 'notarealuser', '01-03-2024', False, 'defender', {
        'buyer': '', 'salesperson': '', 'isSold': False, 'sale_date': ''
    }),

    # Test Case 7: Future date -> invalid -> no update
    (5, 'c001', 'jdoe', (date.today() + timedelta(days=1)).strftime('%d-%m-%Y'), False, 'defender', {
        'buyer': '', 'salesperson': '', 'isSold': False, 'sale_date': ''
    }),

    # Test Case 8: Valid update -> parital -> isSold = False
    (5, 'C899', '', None, True, 'defender', {
        'buyer': 'eva taylor', 'salesperson': '', 'isSold': False, 'sale_date': ''
    }),

    # Test Case 9: Valid update -> parital -> isSold = False
    (5, 'c899', 'bRown', None, True, 'defender', {
        'buyer': 'eva taylor', 'salesperson': 'bob brown', 'isSold': False, 'sale_date': ''
    }),

    # Test Case 10: Valid update
    (5, 'c899', 'brown', '02-03-2024', True, 'defender', {
        'buyer': 'eva taylor', 'salesperson': 'bob brown', 'isSold': True, 'sale_date': '02-03-2024'
    }),

])
def test_updateCarSale_and_verify(carsaleid, customer, salesperson, saledate, expected_result, expected_search, expect_in_db):
    # Convert DD-MM-YYYY to ISO for function
    if saledate is not None:
        d, m, y = map(int, saledate.split("-"))
        iso_date = f"{y:04d}-{m:02d}-{d:02d}"
    else:
        iso_date = None

    result = updateCarSale(carsaleid, customer, salesperson, iso_date)
    assert result is expected_result
    
    record = find_matching_carsale(expected_search.lower(), carsaleid)
    assert record is not None
    assert record["isSold"] is expect_in_db['isSold']
    assert record["buyer"].lower() == expect_in_db["buyer"]
    assert record["salesperson"].lower() == expect_in_db["salesperson"]
    assert record["sale_date"] == expect_in_db["sale_date"]
