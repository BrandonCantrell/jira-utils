from jira import JIRA
import logging

logger = logging.getLogger("jira_cli")

class JiraClient:
    def __init__(self, server: str, username: str, api_token: str):
        self.server = server
        self.username = username
        self.api_token = api_token
        self.jira = self.authenticate()

    def authenticate(self) -> JIRA:
        try:
            return JIRA(options={"server": self.server}, basic_auth=(self.username, self.api_token))
        except Exception as e:
            logger.error("Authentication failed: %s", str(e))
            raise

    def generic_issue_search(self, jql_query: str, max_results: int = 50):
        try:
            results, start = [], 0
            while True:
                batch = self.jira.search_issues(jql_query, startAt=start, maxResults=max_results)
                if not batch:
                    break
                results.extend(batch)
                start += max_results
            return results
        except Exception as e:
            logger.error("Issue search failed: %s", str(e))
            raise
