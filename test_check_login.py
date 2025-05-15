import pytest
from database import checkLogin  # Replace with the actual module name


# ---------- VALID CASES ----------

def test_valid_login_exact_match():
    result = checkLogin('jdoe', 'Pass1234')
    assert result == ['jdoe', 'John', 'Doe']

def test_valid_login_username_case_insensitive():
    result = checkLogin('JDOE', 'Pass1234')
    assert result == ['jdoe', 'John', 'Doe']

def test_valid_login_username_with_spaces_trimmed():
    result = checkLogin('  jdoe  '.strip(), 'Pass1234')  # simulate manual trimming
    assert result == ['jdoe', 'John', 'Doe']


# ---------- INVALID CASES ----------

def test_invalid_login_wrong_password():
    result = checkLogin('jdoe', 'WrongPass')
    assert result is None

def test_invalid_login_nonexistent_username():
    result = checkLogin('notarealuser', 'Pass1234')
    assert result is None

def test_invalid_login_extra_spaces_not_trimmed():
    result = checkLogin('  jdoe  ', 'Pass1234')  # Not stripped: should fail
    assert result is None

def test_invalid_login_empty_username():
    result = checkLogin('', 'Pass1234')
    assert result is None

def test_invalid_login_empty_password():
    result = checkLogin('jdoe', '')
    assert result is None

def test_invalid_login_both_empty():
    result = checkLogin('', '')
    assert result is None
