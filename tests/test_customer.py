import pytest
from src.customer import Customer, update_customer_email

def test_update_customer_email_preserves_id_and_audit():
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin")
    updated = update_customer_email(customer, "NEW@example.com", "agent")
    assert updated.customer_id == 10
    assert updated.name == "Ana"
    assert updated.created_by == "admin"
    assert updated.updated_by == "agent"
    assert updated.email == "new@example.com"

def test_update_customer_email_trims_whitespace():
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin")
    updated = update_customer_email(customer, "  user@domain.org  ", "agent")
    assert updated.email == "user@domain.org"

@pytest.mark.parametrize("invalid_email", [
    "invalid",
    "",
    "   ",
    "@domain.com",
    "user@",
    "user@domain",
    "user@domain.",
    "user space@domain.com",
    None,
])
def test_invalid_email_is_rejected(invalid_email):
    customer = Customer(10, "Ana", "ana@example.com", "admin", "admin")
    with pytest.raises(ValueError, match="invalid-email"):
        update_customer_email(customer, invalid_email, "agent")