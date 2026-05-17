import responses as resp_mock
import requests
import pytest
from repo import GitHubRepo

TOKEN = "test-token"
REPO = "owner/repo"
BASE_URL = f"https://api.github.com/repos/{REPO}/issues"


def _issue(number, title):
    return {"number": number, "title": title, "body": "body", "labels": [], "node_id": f"node_{number}"}


def _pr(number, title):
    return {**_issue(number, title), "pull_request": {"url": "..."}}


@resp_mock.activate
def test_get_issues_returns_issues_without_prs():
    resp_mock.add(resp_mock.GET, BASE_URL, json=[_issue(1, "Bug A"), _pr(2, "PR B")], status=200)

    issues = GitHubRepo(REPO, TOKEN).get_issues()

    assert len(issues) == 1
    assert issues[0]["title"] == "Bug A"


@resp_mock.activate
def test_get_issues_follows_pagination():
    page1_url = f"{BASE_URL}?state=open&per_page=100&page=1"
    page2_url = f"{BASE_URL}?state=open&per_page=100&page=2"

    resp_mock.add(
        resp_mock.GET, page1_url,
        json=[_issue(1, "Issue 1")],
        status=200,
        headers={"Link": f'<{page2_url}>; rel="next"'},
    )
    resp_mock.add(
        resp_mock.GET, page2_url,
        json=[_issue(2, "Issue 2")],
        status=200,
    )

    issues = GitHubRepo(REPO, TOKEN).get_issues()

    assert len(issues) == 2
    assert {i["title"] for i in issues} == {"Issue 1", "Issue 2"}


@resp_mock.activate
def test_get_issues_returns_empty_when_no_issues():
    resp_mock.add(resp_mock.GET, BASE_URL, json=[], status=200)

    issues = GitHubRepo(REPO, TOKEN).get_issues()

    assert issues == []


@resp_mock.activate
def test_get_issues_raises_on_http_error():
    resp_mock.add(resp_mock.GET, BASE_URL, json={"message": "Not Found"}, status=404)

    with pytest.raises(requests.HTTPError):
        GitHubRepo(REPO, TOKEN).get_issues()
