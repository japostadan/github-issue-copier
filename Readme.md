### **1. Directory structure**

Make sure your folder looks like this:

```
github_issue_copier/
│
├─ __init__.py
├─ repo.py
├─ project.py
├─ utils.py
└─ main.py
```

And your `.env` file is in the same directory or project root:

```
SRC_REPO=yourusername/source-repo
DEST_REPO=yourusername/destination-repo
GH_TOKEN=your_github_personal_access_token
PROJECT_NODE_ID=your_project_node_id
STATUS_FIELD_ID=your_status_field_id
TODO_OPTION_ID=your_todo_option_id
```

---

### **2. Create and activate a virtual environment**

**Create the virtual environment**:

```bash
python -m venv venv
```

**Activate it**:

- **Windows (Command Prompt):**

```bash
venv\Scripts\activate
```

- **macOS/Linux:**

```bash
source venv/bin/activate
```

> Your terminal prompt should now show `(venv)` indicating the venv is active.

---

### **3. Install dependencies**

With the venv activated, install the required Python packages:

```bash
pip install python-dotenv requests
```

You can optionally save these to a `requirements.txt` for future use:

```bash
pip freeze > requirements.txt
```

Later, you or others can reinstall them with:

```bash
pip install -r requirements.txt
```

---

### **4. Run the program**

From the terminal (with the venv activated), navigate to the folder containing `main.py` and run:

```bash
python main.py
```

- It will read your environment variables from `.env`.
- Copy open issues from `SRC_REPO` to `DEST_REPO`.
- Optionally add them to your GitHub project if `PROJECT_NODE_ID` etc. are set.
- Any errors will be logged to `github_issue_copy.log`.

---

### **5. Optional: Run as a package**

If you prefer, you can run it as a package from **one level above**:

```bash
python -m github_issue_copier.main
```

- This uses the package structure directly.
- Ensure your current directory is **outside** the `github_issue_copier` folder.

---

### **6. Deactivate the virtual environment**

When done, exit the virtual environment:

```bash
deactivate
```

Your terminal will return to the system Python.

---

### **7. Check logs**

If something goes wrong (like API errors), check:

```
github_issue_copy.log
```

It will contain detailed error messages and response data for debugging.
