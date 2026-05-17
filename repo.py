import requests
from utils import log_error

GITHUB_API = "https://api.github.com"


def _build_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


class GitHubRepo:
    def __init__(self, repo_name, token):
        self.repo_name = repo_name
        self.headers = _build_headers(token)

    def get_issues(self, state="open"):
        url = f"{GITHUB_API}/repos/{self.repo_name}/issues?state={state}&per_page=100&page=1"
        issues = []
        while url:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
            issues.extend(i for i in resp.json() if "pull_request" not in i)
            url = _next_page(resp)
        return issues

    def get_existing_titles(self):
        return {i["title"] for i in self.get_issues()}

    def create_issue(self, issue_data):
        url = f"{GITHUB_API}/repos/{self.repo_name}/issues"
        data = {
            "title": issue_data["title"],
            "body": issue_data.get("body", ""),
            "labels": [l["name"] for l in issue_data.get("labels", [])],
        }
        resp = requests.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()


def _next_page(resp):
    link = resp.headers.get("Link", "")
    for part in link.split(","):
        if 'rel="next"' in part:
            return part.split(";")[0].strip().strip("<>")
    return None
