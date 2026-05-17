## Setup

### 1. Directory structure

```
github_issue_copier/
│
├─ __init__.py
├─ repo.py
├─ project.py
├─ utils.py
├─ main.py
├─ conftest.py
├─ requirements.txt
└─ tests/
   ├─ test_repo.py
   └─ test_copy_issues.py
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

To also run tests, install the test dependencies:

```bash
pip install pytest responses
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
SRC_REPO=owner/source-repo
DEST_REPO=owner/destination-repo
GH_TOKEN=your_github_personal_access_token

# Optional — only needed if you want issues added to a GitHub Project board
PROJECT_NODE_ID=your_project_node_id
STATUS_FIELD_ID=your_status_field_id
TODO_OPTION_ID=your_todo_option_id
```

`SRC_REPO`, `DEST_REPO`, and `GH_TOKEN` are required. The script will exit with a clear error if any are missing.

### 5. Run

```bash
python main.py
```

The script will:
- Copy all open issues from `SRC_REPO` to `DEST_REPO` (paginating through all pages).
- Skip any issue whose title already exists in `DEST_REPO` — safe to re-run.
- Optionally add each new issue to a GitHub Project board if `PROJECT_NODE_ID` is set.
- Log errors to `github_issue_copy.log`.

### 6. Run tests

```bash
pytest tests/
```

### 7. Look up Project board IDs (optional)

Use the GraphQL queries in `project_id.graphql` and `fields.graphql` as reference to find your `PROJECT_NODE_ID`, `STATUS_FIELD_ID`, and `TODO_OPTION_ID` via the [GitHub GraphQL Explorer](https://docs.github.com/en/graphql/overview/explorer).
