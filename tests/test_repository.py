import pytest
from src.customer import Customer
from src.repository import CustomerRepository

def test_update_email_requires_existing_customer():
    repo = CustomerRepository()
    with pytest.raises(ValueError, match="customer-not-found"):
        repo.update_email(99, "a@example.com", "agent")

def test_repository_update_preserves_customer_id():
    repo = CustomerRepository()
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin")
    repo.add(customer)
    repo.update_email(10, "new@example.com", "agent")
    assert repo.get(10).customer_id == 10

def test_repository_update_email_updates_email_and_audit():
    repo = CustomerRepository()
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin")
    repo.add(customer)
    updated = repo.update_email(10, "NEW_EMAIL@example.com", "modifier")
    assert updated.email == "new_email@example.com"
    assert updated.updated_by == "modifier"
    retrieved = repo.get(10)
    assert retrieved.email == "new_email@example.com"
    assert retrieved.updated_by == "modifier"

def test_repository_update_email_rejects_invalid_email():
    repo = CustomerRepository()
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin")
    repo.add(customer)
    with pytest.raises(ValueError, match="invalid-email"):
        repo.update_email(10, "not-an-email", "agent")
    # Verify the customer's email was not corrupted
    assert repo.get(10).email == "ana@example.com"
