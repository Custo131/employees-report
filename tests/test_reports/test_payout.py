import pytest
from reports.payout import PayoutReport
from models.employee import Employee

@pytest.fixture
def make_employee():
    def _make(
        *,
        id: int = 1,
        email: str = "a@b.com",
        name: str = "Default",
        department: str = "General",
        hours_worked: float = 160.0,
        hourly_rate: float = 50.0,
    ) -> Employee:
        return Employee(
            id=id,
            email=email,
            name=name,
            department=department,
            hours_worked=hours_worked,
            hourly_rate=hourly_rate,
        )
    return _make

def test_payout_single_department(make_employee):
    employees = [
        make_employee(name="Alice", department="Design", hours_worked=160, hourly_rate=60),
        make_employee(name="Bob", department="Design", hours_worked=120, hourly_rate=40),
    ]
    report = PayoutReport(employees)
    output = report.generate()

    assert "Design" in output
    assert "Alice" in output and "$9600.00" in output
    assert "Bob" in output and "$4800.00" in output
    assert output.count("Design") == 1
    assert "Name" in output.splitlines()[0]

def test_payout_multiple_departments(make_employee):
    employees = [
        make_employee(name="Alice", department="Design"),
        make_employee(name="Bob", department="Marketing"),
        make_employee(name="Carol", department="Design"),
    ]
    report = PayoutReport(employees)
    output = report.generate()

    assert output.count("Design") == 1
    assert output.count("Marketing") == 1
    assert "Alice" in output and "Carol" in output
    assert "Bob" in output
    assert output.index("Design") < output.index("Marketing")

def test_payout_sorted_within_department(make_employee):
    employees = [
        make_employee(name="Zoe", department="Engineering"),
        make_employee(name="Anna", department="Engineering"),
    ]
    report = PayoutReport(employees)
    output = report.generate()

    lines = output.splitlines()
    eng_lines = [line for line in lines if "Engineering" in line or "Anna" in line or "Zoe" in line]
    assert eng_lines[1].startswith("Anna")
    assert eng_lines[2].startswith("Zoe")

def test_payout_empty_employees():
    report = PayoutReport(employees=[])
    output = report.generate()

    lines = output.strip().splitlines()
    assert "Name" in lines[0]
    assert "Hours" in lines[0]
    assert len(lines) == 2
