import pytest
from models.employee import Employee, EmployeeError

@pytest.fixture
def valid_employee_data():
    return {
        "id": "1",
        "email": "test@example.com",
        "name": "John Doe",
        "department": "Engineering",
        "hours_worked": "160",
        "rate": "50"
    }

def test_from_dict_valid(valid_employee_data):
    emp = Employee.from_dict(valid_employee_data)
    assert emp.id == 1
    assert emp.email == "test@example.com"
    assert emp.name == "John Doe"
    assert emp.department == "Engineering"
    assert emp.hours_worked == 160.0
    assert emp.hourly_rate == 50.0
    assert emp.payout == 8000.0, "Payout should be 160 * 50"

@pytest.mark.parametrize("missing_key", ["id", "email", "name", "department", "hours_worked"])
def test_from_dict_missing_required_field(valid_employee_data, missing_key):
    data = valid_employee_data.copy()
    del data[missing_key]
    with pytest.raises(EmployeeError) as e:
        Employee.from_dict(data)
    assert "Missing columns" in str(e.value)

def test_from_dict_missing_rate_field(valid_employee_data):
    data = valid_employee_data.copy()
    del data["rate"]
    with pytest.raises(EmployeeError) as e:
        Employee.from_dict(data)
    assert "Missing hourly rate" in str(e.value)

@pytest.mark.parametrize("alias", ["hourly_rate", "rate", "salary"])
def test_from_dict_hourly_rate_aliases(valid_employee_data, alias):
    data = valid_employee_data.copy()
    # Replace any existing alias with the one we're testing
    for a in ["hourly_rate", "rate", "salary"]:
        data.pop(a, None)
    data[alias] = "50"
    emp = Employee.from_dict(data)
    assert emp.hourly_rate == 50.0

def test_payout_property():
    emp = Employee(
        id=1,
        email="a@b.com",
        name="A",
        department="X",
        hours_worked=100,
        hourly_rate=25
    )
    assert emp.payout == 2500.0, "Payout should be 100 * 25"
