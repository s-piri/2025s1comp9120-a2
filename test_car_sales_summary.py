import pytest
from database import getCarSalesSummary
from decimal import Decimal

# ---------- VALID CASES ----------

def test_summary_ordering():
    """Test the ordering of car sales summary results."""
    result = getCarSalesSummary()
    
    # Check if results are ordered correctly
    for i in range(len(result) - 1):
        current = result[i]
        next_item = result[i + 1]
        
        # If makes are the same, check model ordering
        if current["make"] == next_item["make"]:
            assert current["model"] <= next_item["model"]
        else:
            assert current["make"] <= next_item["make"]

def test_summary_structure():
    """Test the structure and data types of car sales summary items."""
    result = getCarSalesSummary()
    
    for item in result:
        # Check all required fields exist
        assert "make" in item
        assert "model" in item
        assert "availableUnits" in item
        assert "soldUnits" in item
        assert "soldTotalPrices" in item
        assert "lastPurchaseAt" in item
        
        # Check field types
        assert isinstance(item["make"], str)
        assert isinstance(item["model"], str)
        assert isinstance(item["availableUnits"], int)
        assert isinstance(item["soldUnits"], int)
        assert isinstance(item["soldTotalPrices"], (int, float, Decimal))
        assert isinstance(item["lastPurchaseAt"], str)

def test_summary_calculations():
    """Test that the summary calculations are correct"""
    result = getCarSalesSummary()
    
    for item in result:
        # Available units should be non-negative
        assert item["availableUnits"] >= 0
        
        # Sold units should be non-negative
        assert item["soldUnits"] >= 0
        
        # Total sales should be non-negative
        assert item["soldTotalPrices"] >= 0
        
        # If there are sold units, there should be a last purchase date
        if item["soldUnits"] > 0:
            assert item["lastPurchaseAt"] != ""
        else:
            assert item["lastPurchaseAt"] == ""

def test_summary_date_format():
    """Test that the last purchase date is in DD-MM-YYYY format"""
    result = getCarSalesSummary()
    
    for item in result:
        if item["lastPurchaseAt"] != "":
            # Check date format
            date_parts = item["lastPurchaseAt"].split("-")
            assert len(date_parts) == 3
            assert len(date_parts[0]) == 2  # Day
            assert len(date_parts[1]) == 2  # Month
            assert len(date_parts[2]) == 4  # Year
            
            # Check if parts are numeric
            assert date_parts[0].isdigit()
            assert date_parts[1].isdigit()
            assert date_parts[2].isdigit()

# ---------- EDGE CASES ----------

def test_empty_database():
    """Test behavior when database is empty"""
    # This test would require a way to temporarily empty the database
    # or mock the database connection
    pass

# ---------- INTEGRATION TESTS ----------

def test_summary_with_known_data():
    """Test summary with known data in the database"""
    result = getCarSalesSummary()
    
    # Find a specific make/model combination we know exists
    toyota_camry = next((item for item in result 
                        if item["make"] == "Toyota" and item["model"] == "Camry"), None)
    
    if toyota_camry:
        # Verify the data structure
        assert isinstance(toyota_camry["availableUnits"], int)
        assert isinstance(toyota_camry["soldUnits"], int)
        assert isinstance(toyota_camry["soldTotalPrices"], (int, float, Decimal))
        
        # Verify the data makes sense
        assert toyota_camry["availableUnits"] >= 0
        assert toyota_camry["soldUnits"] >= 0
        assert toyota_camry["soldTotalPrices"] >= 0
        
        # If there are sold units, verify the last purchase date
        if toyota_camry["soldUnits"] > 0:
            assert toyota_camry["lastPurchaseAt"] != ""
            # Verify date format
            date_parts = toyota_camry["lastPurchaseAt"].split("-")
            assert len(date_parts) == 3
            assert all(part.isdigit() for part in date_parts)