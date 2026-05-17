import logging
import requests

# Setup logging
logging.basicConfig(
    filename='github_issue_copy.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_error(message, data=None):
    """Log error messages with optional additional data"""
    logging.error(message)
    if data:
        logging.error(f"Response data: {data}")

def handle_graphql_response(resp, context="GraphQL"):
    """Check for HTTP or GraphQL errors and return JSON data."""
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        log_error(f"HTTP error during {context}", resp.text)
        raise e

    data = resp.json()
    if "errors" in data:
        log_error(f"GraphQL errors during {context}", data["errors"])
        raise Exception(f"GraphQL errors: {data['errors']}")
    
    return data

