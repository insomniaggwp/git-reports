# Overview

This Python script interacts with the GitHub and GITLAB API to:

Fetch all repositories for the authenticated user.

Retrieve all commits from a specified repository and branch.

# Features

Secure authentication using a GitHub or Gitlab personal access token.

List all repositories for the authenticated user.

Fetch commits from a specific repository and branch.

Filter commits by author email (optional).

## Requirements

Python 3.x
PyGithub package (GitHub API wrapper)
python-gitlab v5.6.0 (Gitlab)

## Installation

Clone this repository:

```
git clone https://github.com/yourusername/git-reports.git
cd git-reports
```

Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

Install dependencies:

```pip install -r requirements.txt```

Set up your GitHub personal access token as an environment variable:

```
export GITHUB_TOKEN="your_github_personal_access_token"
export GITLAB_TOKEN="your_gitlab_personal_access_token"
```

Note: Ensure the token has permissions to read repositories and commits.

# Usage

## GITHUB CLIENT

1. List All Repositories

```python3 github_client.py get_all_repos```

2. Fetch All Commits from a Repository

```
python3 github_client.py get_all_commits --owner <username> --repo <repository_name> --branch <branch_name> --author <email>
```

```
--owner (required): GitHub username or organization name.

--repo (required): Repository name.

--branch (optional): Branch name (default: main).

--author (optional): Filter commits by author's email.
```

Example:

```
python3 github_client.py get_all_commits --owner octocat --repo Hello-World --branch main --author user@example.com
```

Error Handling

If GITHUB_TOKEN is missing, the script will raise an error.

If the repository does not exist or is inaccessible, a warning will be displayed.

If no commits are found, the script notifies the user.

## GITLAB CLIENT

1. List All Repositories

```
python3 gitlab_client.py get_all_repos
```

2. Fetch All Commits from a Repository

```
python3 gitlab_client.py get_all_commits --repo <repository_name> --branch <branch_name> --author <email> --commit-per-page <commit_per_page>
```

```

--repo (required): Repository name.

--branch (optional): Branch name (default: main).

--author (optional): Filter commits by author's email.
```

Example:

```
python3 gitlab_client.py get_all_commits --repo smart-pcc-simpul-app --branch develop --author user@example.com --commit-per-page=100
```

Error Handling

If GITLAB_TOKEN is missing, the script will raise an error.

If the repository does not exist or is inaccessible, a warning will be displayed.

If no commits are found, the script notifies the user.
