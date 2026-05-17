import responses as resp_mock
import pytest
from unittest.mock import patch
from main import copy_issues

SRC = "src/repo"
DEST = "dest/repo"
TOKEN = "test-token"
SRC_URL = f"https://api.github.com/repos/{SRC}/issues"
DEST_URL = f"https://api.github.com/repos/{DEST}/issues"


def _issue(number, title):
    return {"number": number, "title": title, "body": "body", "labels": [], "node_id": f"node_{number}"}


@resp_mock.activate
def test_copy_issues_creates_new_issues():
    resp_mock.add(resp_mock.GET, SRC_URL, json=[_issue(1, "New Issue")], status=200)
    resp_mock.add(resp_mock.GET, DEST_URL, json=[], status=200)
    resp_mock.add(resp_mock.POST, DEST_URL, json=_issue(10, "New Issue"), status=201)

    with patch("main.SRC_REPO", SRC), patch("main.DEST_REPO", DEST), patch("main.GH_TOKEN", TOKEN), patch("main.PROJECT_NODE_ID", None):
        copy_issues()

    assert len([c for c in resp_mock.calls if c.request.method == "POST"]) == 1


@resp_mock.activate
def test_copy_issues_skips_existing_issues(capsys):
    resp_mock.add(resp_mock.GET, SRC_URL, json=[_issue(1, "Existing Issue")], status=200)
    resp_mock.add(resp_mock.GET, DEST_URL, json=[_issue(5, "Existing Issue")], status=200)

    with patch("main.SRC_REPO", SRC), patch("main.DEST_REPO", DEST), patch("main.GH_TOKEN", TOKEN), patch("main.PROJECT_NODE_ID", None):
        copy_issues()

    posts = [c for c in resp_mock.calls if c.request.method == "POST"]
    assert len(posts) == 0

    captured = capsys.readouterr()
    assert "Skipping" in captured.out
    assert "Existing Issue" in captured.out


@resp_mock.activate
def test_copy_issues_only_skips_matching_titles(capsys):
    resp_mock.add(resp_mock.GET, SRC_URL, json=[_issue(1, "Old Issue"), _issue(2, "New Issue")], status=200)
    resp_mock.add(resp_mock.GET, DEST_URL, json=[_issue(5, "Old Issue")], status=200)
    resp_mock.add(resp_mock.POST, DEST_URL, json=_issue(10, "New Issue"), status=201)

    with patch("main.SRC_REPO", SRC), patch("main.DEST_REPO", DEST), patch("main.GH_TOKEN", TOKEN), patch("main.PROJECT_NODE_ID", None):
        copy_issues()

    posts = [c for c in resp_mock.calls if c.request.method == "POST"]
    assert len(posts) == 1

    captured = capsys.readouterr()
    assert "Skipping" in captured.out
    assert "Old Issue" in captured.out
