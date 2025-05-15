from typing import Dict
from dataclasses import dataclass


class EmployeeError(Exception):
    """Custom exception for employee model related errors"""
    pass


@dataclass
class Employee:
    id: int
    email: str
    name: str
    department: str
    hours_worked: float
    hourly_rate: float

    @property
    def payout(self) -> float:
        return self.hourly_rate * self.hours_worked

    @classmethod
    def from_dict(cls, row: Dict[str, str]) -> "Employee":
        required_fields = ["id", "email", "name", "department", "hours_worked"]
        missing = [f for f in required_fields if f not in row]
        if missing:
            raise EmployeeError(f"Missing columns: {missing} in row: {row}")

        hourly_rate_aliases = ["hourly_rate", "rate", "salary"]
        hourly_rate_value = next((row[k] for k in hourly_rate_aliases if k in row), None)
        if hourly_rate_value is None:
            raise EmployeeError(f"Missing hourly rate column in row: {row}")

        try:
            return cls(
                id=int(row["id"]),
                email=row["email"],
                name=row["name"],
                department=row["department"],
                hours_worked=float(row["hours_worked"]),
                hourly_rate=float(hourly_rate_value),
            )
        except ValueError as e:
            raise EmployeeError(
                f"Invalid value in row with id={row.get('id', 'N/A')}: {e}"
            )
