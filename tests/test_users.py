import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_user_service
from app.services.user_service import UserService
from unittest.mock import patch
from app.models.user import UserModel

test_db = []


# Use test db
def override_get_user_service():
    return UserService(test_db)


app.dependency_overrides[get_user_service] = override_get_user_service


# Patch `save_data_to_json` to prevent writing to file and populate with dummy data
@pytest.fixture(scope="function", autouse=True)
def setup_test_environment():
    with patch("app.services.user_service.save_data_to_json") as mock_save:
        test_db.clear()
        test_db.append(
            UserModel(
                id=1, name="Alice", email="Alice@example.com", contact_number="61234567"
            )
        )
        yield
        test_db.clear()


# Test data - Actual users
new_user_bob = {
    "name": "Bob",
    "email": "Bob@example.com",
    "contact_number": "81234567",
}
new_user_charlie = {
    "name": "Charlie",
    "email": "Charlie@example.com",
}
new_user_debbie = {
    "name": "Debbie",
    "contact_number": "91234567",
}
# Test data - Error users
new_user_trouble_same_name = {
    "name": "Alice",
    "email": "Trouble@example.com",
}
new_user_trouble_same_number = {
    "name": "Trouble",
    "contact_number": "61234567",
}
new_user_trouble_same_email = {
    "name": "Trouble",
    "email": "Alice@example.com",
}
new_user_trouble_no_contact = {
    "name": "Trouble",
}
new_user_trouble_wrong_email = {
    "name": "Trouble",
    "email": "Trouble",
}
new_user_trouble_wrong_number = {
    "name": "Trouble",
    "contact_number": "123",
}

client = TestClient(app)


#####################################
##### TEST HELPER FUNCTION HERE #####
#####################################
def _test_add_user_ok(user_details):
    resp = client.post("/users/", json=user_details)
    assert resp.status_code == 201
    data = resp.json()

    # Check the response data
    assert data["name"] == user_details["name"]
    assert data["email"] == user_details.get("email")
    assert data["contact_number"] == user_details.get("contact_number")
    assert "id" in data


def _test_add_error_user(user_detail, expected_status_code):
    resp = client.post("/users/", json=user_detail)
    assert resp.status_code == expected_status_code


############################
##### TEST STARTS HERE #####
############################


# Test getting user
def test_post_get_users_ok():
    body_data = [{"id": 1}, {"id": 999}, {"ixd": 321}]
    resp = client.post("/users/get_users", json=body_data)
    assert resp.status_code == 200
    found_users = resp.json()
    assert len(found_users) == 1
    assert found_users[0]["name"] == "Alice"


# Test adding users
def test_add_user_full_contact():
    _test_add_user_ok(new_user_bob)


def test_add_user_email_only():
    _test_add_user_ok(new_user_charlie)


def test_add_user_phone_only():
    _test_add_user_ok(new_user_debbie)


# Test adding users with duplicate
def test_add_user_with_duplicate():
    expected_error_code = 400
    # Test for duplicate name
    _test_add_error_user(new_user_trouble_same_name, expected_error_code)

    # Test for duplicate contact number
    _test_add_error_user(new_user_trouble_same_number, expected_error_code)

    # Test for duplicate email
    _test_add_error_user(new_user_trouble_same_email, expected_error_code)


# Test adding users with wrong format
def test_add_user_with_wrong_format():
    expected_error_code = 422  # using model/field validation hence 422
    # Test for no contact
    _test_add_error_user(new_user_trouble_no_contact, expected_error_code)

    # Test for wrong email format
    _test_add_error_user(new_user_trouble_wrong_email, expected_error_code)

    # Test for wrong contact format
    _test_add_error_user(new_user_trouble_wrong_number, expected_error_code)


# Test deleting alice
def test_delete_user_ok():
    resp = client.delete("/users/1")
    assert resp.status_code == 200
    assert resp.json() == {"detail": "User deleted successfully"}


# Test deleting random users
def test_delete_user_not_found():
    resp = client.delete("/users/99")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "User not found"}
