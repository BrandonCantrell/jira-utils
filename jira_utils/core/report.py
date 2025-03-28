import logging
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from jira_utils.core.auth import load_config
from jira_utils.core.jira import JiraClient
from jira_utils.core.categorize import (load_existing_categories, infer_dynamic_categories,
                                      merge_categories, categorize_summary_dynamic)
from jira_utils.core.visualize import visualize_issue_counts

logger = logging.getLogger("jira_cli")


def setup_report_parser(parser):
    parser.add_argument("--project")
    parser.add_argument("--labels")
    parser.add_argument("--creator")
    parser.add_argument("--summary")
    parser.add_argument("--parent")
    parser.add_argument("--assignee")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    parser.add_argument("--group-by", nargs="*", help="Fields to group by")
    parser.add_argument("--categorize", action="store_true", help="Dynamically categorize issues by keywords")
    parser.add_argument("--visualize", action="store_true", help="Generate a bar chart visualization")
    parser.add_argument("--time-frame", choices=["week", "month", "quarter", "year", "all"], default="all")
    parser.add_argument("--created-count", action="store_true")
    parser.add_argument("--closed-count", action="store_true")
    parser.add_argument("--export-html", action="store_true")
    parser.add_argument("--export-pdf", action="store_true")


def handle_command(args):
    config = load_config(args)
    client = JiraClient(config['server'], config['username'], config['token'])

    jql_parts = []
    for k in ["project", "labels", "creator", "summary", "parent", "assignee"]:
        v = getattr(args, k)
        if v:
            jql_parts.append(f"{k} = \"{v}\"")
    if args.start_date:
        jql_parts.append(f'created >= "{args.start_date}"')
    if args.end_date:
        jql_parts.append(f'created <= "{args.end_date}"')

    if not jql_parts:
        print("❌ At least one filter is required.")
        return

    issues = client.generic_issue_search(" AND ".join(jql_parts), max_results=args.limit)

    rows, summaries = [], []
    for issue in issues:
        if not issue.fields.resolutiondate:
            continue
        created = pd.to_datetime(issue.fields.created)
        resolved = pd.to_datetime(issue.fields.resolutiondate)
        days = len(pd.bdate_range(created, resolved))
        summaries.append(issue.fields.summary)
        rows.append({
            "key": issue.key,
            "summary": issue.fields.summary,
            "assignee": getattr(issue.fields.assignee, 'displayName', 'Unassigned'),
            "created": issue.fields.created,
            "resolved": issue.fields.resolutiondate,
            "duration_working_days": days
        })

    df = pd.DataFrame(rows)
    if df.empty:
        print("No resolved issues found.")
        return

    if args.categorize:
        existing = load_existing_categories()
        new = infer_dynamic_categories(summaries)
        combined = merge_categories(existing, new)
        df["category"] = df["summary"].apply(lambda s: categorize_summary_dynamic(s, combined))

    print(f"\n📊 Avg Resolution Time: {df['duration_working_days'].mean():.2f} working days\n")

    if args.group_by:
        grouped = df.groupby(args.group_by)["duration_working_days"].agg(['count', 'mean', 'median', 'min', 'max'])
        print(grouped.to_string())

    if args.created_count or args.closed_count:
        visualize_issue_counts(df, args)

    if args.format == "csv":
        df.to_csv("jira_report.csv", index=False)
        print("✅ Report saved to jira_report.csv")
    else:
        print(df.to_json(orient="records", indent=2))
