import requests
from utils import handle_graphql_response

GITHUB_GRAPHQL = "https://api.github.com/graphql"


def _build_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


class GitHubProject:
    def __init__(self, project_node_id, token, status_field_id=None, todo_option_id=None):
        self.project_node_id = project_node_id
        self.status_field_id = status_field_id
        self.todo_option_id = todo_option_id
        self.headers = _build_headers(token)

    def add_issue(self, issue_node_id):
        query = """
        mutation($project:ID!, $content:ID!) {
          addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
            item { id }
          }
        }
        """
        variables = {"project": self.project_node_id, "content": issue_node_id}
        resp = requests.post(GITHUB_GRAPHQL, headers=self.headers, json={"query": query, "variables": variables})
        data = handle_graphql_response(resp, "adding issue to project")
        item = data.get("data", {}).get("addProjectV2ItemById", {}).get("item")
        if not item:
            raise Exception("Failed to add issue to project.")
        return item["id"]

    def set_item_status(self, item_id):
        if not all([self.status_field_id, self.todo_option_id]):
            raise ValueError("Status field ID and Todo option ID must be set")

        query = """
        mutation($project:ID!, $item:ID!, $field:ID!, $option:ID!) {
          updateProjectV2ItemFieldValue(input: {
            projectId: $project,
            itemId: $item,
            fieldId: $field,
            value: { singleSelectOptionId: $option }
          }) {
            projectV2Item { id }
          }
        }
        """
        variables = {
            "project": self.project_node_id,
            "item": item_id,
            "field": self.status_field_id,
            "option": self.todo_option_id,
        }
        resp = requests.post(GITHUB_GRAPHQL, headers=self.headers, json={"query": query, "variables": variables})
        return handle_graphql_response(resp, "setting item status")
