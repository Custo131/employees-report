from abc import ABC, abstractmethod
from typing import List
from models.employee import Employee

class BaseReport(ABC):
    def __init__(self, employees: List[Employee]) -> None:
        self.employees = employees

    @abstractmethod
    def generate(self) -> str:
        """Generate a report and return it as a string"""
        ...
