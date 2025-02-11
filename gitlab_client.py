import gitlab # type: ignore
import os
import sys
import argparse
import certifi
from datetime import datetime

GITLAB_SERVER = os.environ.get('GITLAB_SERVER', 'https://gitlab.com')
GITLAB_TOKEN = os.environ.get('GITLAB_TOKEN')
CA_CERT_PATH = os.environ.get('CA_CERT_PATH')

if not GITLAB_TOKEN:
    print("Please set the GITLAB_TOKEN env variable.")
    sys.exit(1)

def get_all_repos():
    """ Fetch and print all repositories for the authenticated user. """
    # Authenticate with GitLab
    try:
        gl = gitlab.Gitlab(url=GITLAB_SERVER, private_token=GITLAB_TOKEN, ssl_verify=False)
        gl.auth()  # Verify authentication
        print("Authentication successful")

        # Fetch and print repositories
        for project in gl.projects.list(membership=True, all=True):
            print(project.name)

    except gitlab.exceptions.GitlabAuthenticationError as e:
        print(f"Authentication failed: {e}")
    except Exception as e:
        print(f"Error fetching repositories: {e}")

def get_all_commits(repo_name, branch="main", author_email=None, commit_per_page=20):
    """ Fetch and print all commits in the specified repository. """
    try:
        gl = gitlab.Gitlab(url=GITLAB_SERVER, private_token=GITLAB_TOKEN, ssl_verify=False)
        gl.auth()  # Verify authentication
        print("Authentication successful")

        projects = gl.projects.list(membership=True, search=repo_name, get_all=True)

        if not projects:
            print(f"Error: Repository '{repo_name}' not found")
            return
        
        project = projects[0]

        # Set default branch if None
        if branch is None:
            branch = project.default_branch

        # Fetch commits from the specified branch
        commits = project.commits.list(ref_name=branch, per_page=commit_per_page, get_all=False)

        if not commits:
            print(f"No commits found in branch '{branch}'.")
            return

        for commit in commits:
            author_email_commit = commit.author_email
            commit_date = datetime.strptime(commit.created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_date = commit_date.strftime("%B %d, %Y")

            # If author_email is provided, filter commits; otherwise, return all commits
            if author_email is None or author_email_commit == author_email:
                print(f"Commit SHA: {commit.id}")
                print(f"Message: {commit.message}")
                print(f"Author: {commit.author_name}")
                print(f"Email: {commit.author_email}")
                print(f"Date: {formatted_date}")
                print("-" * 50)

    except Exception as e:
        print(f"Error fetching commits: {e}")

def main():
    parser = argparse.ArgumentParser(description="GitLab API CLI")
    parser.add_argument("command", choices=["get_all_repos", "get_all_commits"], help="Command to execute")
    parser.add_argument("--repo", help="Repository name")
    parser.add_argument("--branch", default="main", help="Select branch (default: main)")
    parser.add_argument("--author", help="Filter based on author email")
    parser.add_argument("--commit_per_page", help="Total commit show")

    args = parser.parse_args()

    if args.command == "get_all_repos":
        get_all_repos()
    elif args.command == "get_all_commits":
        if not args.repo:
            print("Error: --repo are required for get_all_commits")
            return
        get_all_commits(args.repo, args.branch, args.author, args.commit_per_page)
    else:
        print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main()
