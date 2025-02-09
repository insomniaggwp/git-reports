import gitlab # type: ignore
import os
import sys
import argparse

GITLAB_SERVER = os.environ.get('GITLAB_SERVER', 'https://gitlab.com')
GITLAB_TOKEN = os.environ.get('GITLAB_TOKEN')

if not GITLAB_TOKEN:
    print("Please set the GITLAB_TOKEN env variable.")
    sys.exit(1)

def get_all_repos():
    """ Fetch and print all repositories for the authenticated user. """
    # Authenticate with GitLab
    try:
        gl = gitlab.Gitlab(url=GITLAB_SERVER, private_token=GITLAB_TOKEN)
        gl.auth()  # Verify authentication
        print("Authentication successful")

        # Fetch and print repositories
        for project in gl.projects.list(owned=True):
            print(project.name)

    except gitlab.exceptions.GitlabAuthenticationError as e:
        print(f"Authentication failed: {e}")
    except Exception as e:
        print(f"Error fetching repositories: {e}")

def get_all_commits(owner, repo_name, branch="main", author_email=None):
    """ Fetch and print all commits in the specified repository. """
    try:
        gl = gitlab.Gitlab(url=GITLAB_SERVER, private_token=GITLAB_TOKEN)
        gl.auth()  # Verify authentication
        print("Authentication successful")
        # Find the project by owner and repo name
        projects = gl.projects.list(search=repo_name)
        
        project = next((p for p in projects if p.namespace['path'] == owner), None)

        if not project:
            print(f"Error: Repository '{repo_name}' not found under '{owner}'.")
            return

        # Set default branch if None
        if branch is None:
            branch = project.default_branch

        # Fetch commits from the specified branch
        commits = project.commits.list(ref_name=branch)

        if not commits:
            print(f"No commits found in branch '{branch}'.")
            return

        for commit in commits:
            author_email_commit = commit.author_email

            # If author_email is provided, filter commits; otherwise, return all commits
            if author_email is None or author_email_commit == author_email:
                print(f"Commit: {commit.id}")
                print(f"Commit SHA: {commit.id}")
                print(f"Message: {commit.message}")
                print(f"Author: {commit.author_name}")
                print(f"Email: {commit.author_email}")
                print(f"Date: {commit.created_at}")
                print("-" * 50)

    except Exception as e:
        print(f"Error fetching commits: {e}")

def main():
    parser = argparse.ArgumentParser(description="GitLab API CLI")
    parser.add_argument("command", choices=["get_all_repos", "get_all_commits"], help="Command to execute")
    parser.add_argument("--owner", help="GitLab repository owner")
    parser.add_argument("--repo", help="Repository name")
    parser.add_argument("--branch", default="main", help="Select branch (default: main)")
    parser.add_argument("--author", help="Filter based on author email")

    args = parser.parse_args()

    if args.command == "get_all_repos":
        get_all_repos()
    elif args.command == "get_all_commits":
        if not args.owner or not args.repo:
            print("Error: --owner and --repo are required for get_all_commits")
            return
        get_all_commits(args.owner, args.repo, args.branch, args.author)
    else:
        print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main()
