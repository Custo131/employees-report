import logging
import sys
from cli import custom_parse_args
from parsers.csv import parse_csv_file
from reports import get_report

logging.basicConfig(level=logging.INFO, format="%(message)s"
)
logger = logging.getLogger(__name__)

def main() -> None:
    args = custom_parse_args()
    report_class = get_report(args.report)
    
    if not report_class:
        logger.error(f"Unknown report type: {args.report}")
        sys.exit(1)
    
    for file_path in args.files:
        logger.info("=" * 100)
        logger.info(f"Report for file {file_path}")
        try:
            employees = parse_csv_file(file_path)
            if not employees:
                logger.warning("No valid employees found")
                continue

            report = report_class(employees=employees)
            logger.info(report.generate())
        except (ValueError, FileNotFoundError) as e:
            logger.error(f"Error generating report for {file_path}: {e}")
            continue

if __name__ == "__main__":
    main()

