import pytest
import datetime
from database import addCarSale

# ---------- VALID CASES ----------

def test_valid_toyota_corolla():
    assert addCarSale("Toyota", "Corolla", 2020, 30000, 15000.00) is True

def test_valid_case_insensitive_make_model():
    assert addCarSale("toyota", "corolla", 2020, 20000, 10000.00) is True

def test_valid_other_make_model():
    assert addCarSale("Lexus", "NX", 2022, 12000, 38000.00) is True

def test_valid_other_make_model2():
    assert addCarSale("Land rOver", "rAnge RovEr", 1995, 10, 38000.000) is True


# ---------- INVALID CASES: Make/Model RELATION ----------

def test_model_does_not_belong_to_make():
    # Corolla is a Toyota model, not Mercedes Benz
    assert addCarSale("Mercedes Benz", "Corolla", 2020, 25000, 18000.00) is False

def test_nonexistent_make():
    assert addCarSale("FakeMake", "Camry", 2020, 20000, 15000.00) is False

def test_nonexistent_model():
    assert addCarSale("Toyota", "FakeModel", 2020, 20000, 15000.00) is False


# ---------- INVALID CASES: Constraints ----------

def test_built_year_too_old():
    assert addCarSale("Toyota", "Camry", 1949, 50000, 8000.00) is False

def test_built_year_in_future():
    next_year = datetime.datetime.now().year + 1
    assert addCarSale("Toyota", "Camry", next_year, 5000, 9000.00) is False

def test_zero_odometer():
    assert addCarSale("Toyota", "Camry", 2020, 0, 9000.00) is False

def test_negative_odometer():
    assert addCarSale("Toyota", "Camry", 2020, -5000, 9000.00) is False

def test_zero_price():
    assert addCarSale("Toyota", "Camry", 2020, 10000, 0.00) is False

def test_negative_price():
    assert addCarSale("Toyota", "Camry", 2020, 10000, -1.00) is False
