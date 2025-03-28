import argparse
from jira_utils.core import report
from jira_utils.core.auth import save_config

def main():
    parser = argparse.ArgumentParser(description="JIRA CLI App")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # Configure command
    config_parser = subparsers.add_parser("configure", help="Store JIRA credentials locally")
    config_parser.add_argument("--server", required=True, help="JIRA server URL")
    config_parser.add_argument("--username", required=True, help="JIRA username/email")
    config_parser.add_argument("--token", required=True, help="JIRA API token")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate reports from JIRA issues")
    report_parser.add_argument("--limit", type=int, default=50, help="Number of results to fetch per batch")
    report.setup_report_parser(report_parser)

    args = parser.parse_args()

    if args.command == "report":
        report.handle_command(args)
    elif args.command == "configure":
        save_config(args.server, args.username, args.token)
        print("✅ JIRA credentials saved and encrypted.")
    else:
        parser.print_help()