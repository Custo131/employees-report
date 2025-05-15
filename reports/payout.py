from reports.base import BaseReport
from collections import defaultdict

class PayoutReport(BaseReport):
    def generate(self) -> str:
        department_groups = defaultdict(list)
        for emp in self.employees:
            department_groups[emp.department].append(emp)

        lines = []
        header = f"{'Name':<20} {'Hours':>6} {'Rate':>6} {'Payout':>8}"
        lines.append(header)
        lines.append("-" * len(header))

        for department in sorted(department_groups):
            lines.append(f"\n{department}")
            for emp in sorted(department_groups[department], key=lambda e: e.name):
                payout = emp.payout
                lines.append(
                    f"{emp.name:<20} {emp.hours_worked:>6.1f} {emp.hourly_rate:>6.2f} ${payout:>7.2f}"
                )

        return "\n".join(lines)
