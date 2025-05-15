from typing import Type
from reports.base import BaseReport
from reports.payout import PayoutReport

REPORT_REGISTRY: dict[str, Type[BaseReport]] = {
    "payout": PayoutReport,
}

def get_report(report_type: str) -> Type[BaseReport]:
    try:
        return REPORT_REGISTRY[report_type]
    except KeyError:
        raise ValueError(f"Unsupported report type: {report_type}")