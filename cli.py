import argparse
import os
import sys
import logging
logger = logging.getLogger(__name__)

class CLIError(Exception):
    """Custom exception for CLI-related errors"""
    pass


def is_valid_csv(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8") as f:
            first_line = f.readline()
            return "," in first_line
    except Exception:
        return False


def validate_file(path: str) -> str:
    if not os.path.exists(path):
        raise CLIError(f"File not found: {path}")
    if not os.path.isfile(path):
        raise CLIError(f"Not a regular file: {path}")
    if not path.endswith(".csv"):
        raise CLIError(f"Invalid file extension (expected .csv): {path}")
    if not os.access(path, os.R_OK):
        raise CLIError(f"File is not readable: {path}")
    if not is_valid_csv(path):
        raise CLIError(
            f"Invalid CSV file content: {path}. "
            f"Only comma (`,`) is supported as a delimiter."
        )
    return path


def custom_parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate salary-related reports from CSV employee files.\n"
                    "Note: Only comma (`,`) is supported as a delimiter in CSV files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="CSV files containing employee data",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=["payout"],
        help="Type of report to generate (e.g., 'payout')",
    )

    args = parser.parse_args()

    try:
        args.files = [validate_file(f) for f in args.files]
    except CLIError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

    return args
