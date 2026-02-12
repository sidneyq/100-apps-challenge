"""
Shared Jira client for the 100 Apps Challenge.
Usage:
    from shared.jira_client import get_jira_client
    jira = get_jira_client()
    results = jira.jql('project = X AND status = "In Progress"')
"""
import os


def get_jira_client():
  """Create and return a Jira client using environment variables."""
  try:
    from atlassian import Jira
  except ImportError:
    raise ImportError(
        "Install atlassian-python-api: pip install atlassian-python-api")

  url = os.environ.get("JIRA_URL")
  email = os.environ.get("JIRA_EMAIL")
  token = os.environ.get("JIRA_API_TOKEN")

  if not all([url, email, token]):
    raise ValueError("Missing Jira credentials. Set JIRA_URL, JIRA_EMAIL, "
                     "and JIRA_API_TOKEN in your .env file.")

  return Jira(url=url, username=email, password=token, cloud=True)


def run_jql(jira, jql, limit=100):
  """Run a JQL query with pagination and return all issues."""
  all_issues = []
  start = 0
  while True:
    batch = jira.jql(jql, start=start, limit=min(limit, 50))
    all_issues.extend(batch["issues"])
    if start + 50 >= batch["total"]:
      break
    start += 50
  return all_issues


def issues_to_dataframe(issues, fields=None):
  """Convert Jira issues to a pandas DataFrame."""
  try:
    import pandas as pd
  except ImportError:
    raise ImportError("Install pandas: pip install pandas")

  if fields is None:
    fields = [
        "summary", "status", "assignee", "priority", "created", "updated"
    ]

  rows = []
  for issue in issues:
    row = {"key": issue["key"]}
    for field in fields:
      value = issue["fields"].get(field)
      # Handle nested objects (status, assignee, priority)
      if isinstance(value, dict):
        value = value.get("displayName") or value.get("name") or str(value)
      row[field] = value
    rows.append(row)

  return pd.DataFrame(rows)
