import os
import sys
from dotenv import load_dotenv
from repo import GitHubRepo
from project import GitHubProject
from utils import log_error

load_dotenv()
SRC_REPO = os.getenv("SRC_REPO")
DEST_REPO = os.getenv("DEST_REPO")
GH_TOKEN = os.getenv("GH_TOKEN")
PROJECT_NODE_ID = os.getenv("PROJECT_NODE_ID")
STATUS_FIELD_ID = os.getenv("STATUS_FIELD_ID")
TODO_OPTION_ID = os.getenv("TODO_OPTION_ID")


def copy_issues():
    required = {"SRC_REPO": SRC_REPO, "DEST_REPO": DEST_REPO, "GH_TOKEN": GH_TOKEN}
    missing = [k for k, v in required.items() if not v]
    if missing:
        sys.exit(f"Missing required environment variables: {', '.join(missing)}")

    src_repo = GitHubRepo(SRC_REPO, GH_TOKEN)
    dest_repo = GitHubRepo(DEST_REPO, GH_TOKEN)
    project = None
    if PROJECT_NODE_ID:
        project = GitHubProject(PROJECT_NODE_ID, GH_TOKEN, STATUS_FIELD_ID, TODO_OPTION_ID)

    print(f"Copying issues from {SRC_REPO} to {DEST_REPO}")

    existing_titles = dest_repo.get_existing_titles()
    issues = src_repo.get_issues()

    for issue in issues:
        if issue["title"] in existing_titles:
            print(f"Skipping (already exists): {issue['title']}")
            continue
        try:
            new_issue = dest_repo.create_issue(issue)
            print(f"Created issue #{new_issue['number']}: {new_issue['title']}")
            if project:
                item_id = project.add_issue(new_issue["node_id"])
                print(f"Added to project board as item {item_id}")
                project.set_item_status(item_id)
                print("Set status to '📋 Backlog'.")
        except Exception as e:
            log_error(f"Error processing issue '{issue['title']}': {e}")


if __name__ == "__main__":
    copy_issues()
