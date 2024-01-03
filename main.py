import os
from jira import JIRA
import json
import re

jira = JIRA(server="https://thescore.atlassian.net", basic_auth=('brandon.cantrell@penn-interactive.com', os.environ.get('jira_token')))

#customfield 12600 is development

issues = jira.search_issues('project in (SRE, SRESUP) and issuetype not in (Subtask, sub-task) and created >= \'2023-01-01\'', maxResults=False)


issues_list = []
for issue in issues:
    issues_list.append(issue.key)

print(len(issues_list))


