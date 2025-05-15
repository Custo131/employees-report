from typing import List
from models.employee import Employee
import logging
logger = logging.getLogger(__name__)

def parse_csv_file(file_path: str) -> List[Employee]:
    employees : list[Employee] = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    if not lines:
        return employees

    headers = [h.strip() for h in lines[0].split(",")]

    for line_number, line in enumerate(lines[1:], start=2):
        values = [v.strip() for v in line.split(",")]
        
        if len(values) != len(headers):
            logger.error(f"Skipping row {line_number} in {file_path}: column mismatch")
            continue
        
        row_dict = dict(zip(headers, values))

        try:
            employee = Employee.from_dict(row_dict)
            employees.append(employee)
        except Exception as e:
            logger.error(f"Skipping invalid employee row {line_number} in {file_path}: {e}")

    return employees
