import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def visualize_issue_counts(df, args):
    time_field = "created" if args.created_count else "resolved"

    if args.time_frame != "all":
        df["period"] = pd.to_datetime(df[time_field])
        if args.time_frame == "week":
            df["period"] = df["period"].dt.to_period("W").dt.start_time
        elif args.time_frame == "month":
            df["period"] = df["period"].dt.to_period("M").dt.start_time
        elif args.time_frame == "quarter":
            df["period"] = df["period"].dt.to_period("Q").dt.start_time
        elif args.time_frame == "year":
            df["period"] = df["period"].dt.to_period("Y").dt.start_time

    count_group = ["category"]
    if args.time_frame != "all":
        count_group.insert(0, "period")

    counts = df.groupby(count_group).size().reset_index(name="count")
    print("\n📊 Issue Count by Category" + (" and Time" if args.time_frame != "all" else "") + ":")
    print(counts.to_string(index=False))

    if args.visualize:
        try:
            pivot = counts.pivot(index="period" if args.time_frame != "all" else "category", columns="category", values="count")
            ax = pivot.plot(kind="bar", stacked=True if args.time_frame != "all" else False, figsize=(10, 6))
            plt.title("Issue Counts by Category" + (f" over {args.time_frame.title()}s" if args.time_frame != "all" else ""))
            plt.ylabel("Issue Count")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            chart_filename = "jira_issue_counts.png"
            plt.savefig(chart_filename)
            print(f"📈 Visualization saved to {chart_filename}")

            if args.export_pdf:
                pdf_filename = chart_filename.replace(".png", ".pdf")
                with PdfPages(pdf_filename) as pdf:
                    pdf.savefig()
                print(f"📄 PDF export saved to {pdf_filename}")

            if args.export_html:
                try:
                    import mpld3
                    html_filename = chart_filename.replace(".png", ".html")
                    with open(html_filename, "w") as f:
                        f.write(mpld3.fig_to_html(plt.gcf()))
                    print(f"🌐 HTML export saved to {html_filename}")
                except ImportError:
                    print("⚠️ mpld3 not installed. Run 'pip install mpld3' to enable HTML export.")

            plt.close()
        except Exception as e:
            print(f"❌ Visualization failed: {e}")