import pytest
from pathlib import Path
from parsers.csv import parse_csv_file
from models.employee import Employee


from typing import Callable

@pytest.fixture
def tmp_csv_file(tmp_path) -> Callable[[str, str], Path]:
    def _create(content: str, filename: str = "data.csv") -> Path:
        path = tmp_path / filename
        path.write_text(content.strip(), encoding="utf-8")
        return path
    return _create



@pytest.mark.parametrize("rate_col", ["hourly_rate", "rate", "salary"])
def test_parse_csv_valid(rate_col, tmp_csv_file):
    csv = f"""
    id,email,name,department,hours_worked,{rate_col}
    1,alice@example.com,Alice,Marketing,160,50
    2,bob@example.com,Bob,Design,150,40
    """
    path = tmp_csv_file(csv)
    employees = parse_csv_file(str(path))

    assert len(employees) == 2
    assert all(isinstance(emp, Employee) for emp in employees)
    assert employees[0].name == "Alice"
    assert employees[1].hourly_rate == 40


def test_parse_csv_empty_file(tmp_csv_file):
    path = tmp_csv_file("")
    employees = parse_csv_file(str(path))
    assert employees == []


def test_parse_csv_header_only(tmp_csv_file):
    csv = "id,email,name,department,hours_worked,salary"
    path = tmp_csv_file(csv)
    employees = parse_csv_file(str(path))
    assert employees == []

def test_parse_csv_skips_invalid_row_missing_field(tmp_csv_file, caplog):
    csv = """
    id,email,name,department,hours_worked,rate
    1,alice@example.com,Alice,Marketing,160,50
    2,bob@example.com,Design,150,40
    """
    # Row 2 has missing column (only 5 values), triggers column mismatch
    path = tmp_csv_file(csv)
    with caplog.at_level("ERROR"):
        employees = parse_csv_file(str(path))

    assert len(employees) == 1
    assert employees[0].name == "Alice"
    assert "Skipping row 3 in" in caplog.text



def test_parse_csv_skips_row_with_column_mismatch(tmp_csv_file, caplog):
    csv = """
    id,email,name,department,hours_worked,rate
    1,alice@example.com,Alice,Marketing,160,50
    2,bob@example.com,Bob,Design,150
    """
    path = tmp_csv_file(csv)
    with caplog.at_level("ERROR"):
        employees = parse_csv_file(str(path))

    assert len(employees) == 1
    assert "Skipping row 3 in" in caplog.text
    assert "column mismatch" in caplog.text


def test_parse_csv_invalid_type(tmp_csv_file, caplog):
    csv = """
    id,email,name,department,hours_worked,rate
    1,alice@example.com,Alice,Marketing,one_sixty,50
    """
    path = tmp_csv_file(csv)
    with caplog.at_level("ERROR"):
        employees = parse_csv_file(str(path))

    assert employees == []
    assert "Skipping invalid employee row 2" in caplog.text
    assert "Invalid value in row" in caplog.text


def test_parse_csv_trailing_newline(tmp_csv_file):
    csv = """
    id,email,name,department,hours_worked,rate
    1,alice@example.com,Alice,Marketing,160,50

    """
    path = tmp_csv_file(csv)
    employees = parse_csv_file(str(path))
    assert len(employees) == 1
    assert employees[0].name == "Alice"


def test_parse_csv_extra_column(tmp_csv_file):
    csv = """
    id,email,name,department,hours_worked,rate,extra
    1,alice@example.com,Alice,Marketing,160,50,extra_value
    """
    path = tmp_csv_file(csv)
    employees = parse_csv_file(str(path))

    assert len(employees) == 1
    assert employees[0].name == "Alice"



def test_parse_csv_header_with_spaces(tmp_csv_file):
    csv = """
    id , email , name , department , hours_worked , rate
    1,alice@example.com,Alice,Marketing,160,50
    """
    path = tmp_csv_file(csv)
    employees = parse_csv_file(str(path))
    assert len(employees) == 1
    assert employees[0].name == "Alice"
    assert employees[0].hourly_rate == 50.0
