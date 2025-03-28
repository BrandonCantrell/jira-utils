# Jira Utils

A modular Python CLI tool for querying and analyzing Jira issues.

## 🚀 Features
- 🔐 Encrypted API token storage (using `cryptography`)
- 🔍 JQL and filtered search (project, labels, summary, etc.)
- 📊 Issue duration reports
- 🧠 Dynamic categorization of issue summaries
- 📈 Visualization with Matplotlib
- 📤 Export to CSV, JSON, PDF, HTML
- 🧱 Clean modular architecture

## 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

## 🛠 Configure
```bash
python -m jira_utils configure \
  --server https://your-domain.atlassian.net \
  --username your-email@example.com \
  --token your_api_token
```

## 🔧 Usage Examples
### Report with Categorization and Grouping
```bash
python -m jira_utils report \
  --project MYPROJ \
  --categorize \
  --group-by category \
  --format json
```

### Count Created Issues by Month
```bash
python -m jira_utils report \
  --project MYPROJ \
  --categorize \
  --created-count \
  --time-frame month \
  --visualize --export-pdf
```

## 📁 Project Structure
```
jira_utils/
├── __main__.py         # CLI entry
├── cli.py              # Argument parsing
├── core/
│   ├── auth.py         # Encrypted config
│   ├── jira.py         # API interface
│   ├── categorize.py   # Keyword grouping
│   ├── report.py       # Main logic
│   └── visualize.py    # Charts and export
├── config/
│   └── paths.py        # Path constants
```

## 📤 Export Binary (Optional)
```bash
pip install pyinstaller
pyinstaller --name jira-utils --onefile -m jira_utils
```

---

MIT License. Built with ❤️ to automate Jira workflows.