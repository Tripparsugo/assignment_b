from anchor import GITHUB_TOKEN, ASSIGNMENTS_DIR, LABS_DIR
from github import Github
import pandas as pd
from git.repo.base import Repo
from alive_progress import alive_bar
from config import ORG

if __name__ == '__main__':
    assignments_csv = pd.read_csv(f"{ASSIGNMENTS_DIR}/{ORG}.csv")

    g = Github(login_or_token=GITHUB_TOKEN)
    # Then play with your Github objects:
    first = True
    repos = g.get_organization(ORG).get_repos()

    assignments = assignments_csv["Assignment"].values
    assignment_to_repos = dict()
    count = 0
    for assignment in assignments:
        print(f"Reading assignment {assignment}")
        assignment_repos = [repo for repo in repos if repo.name.startswith(assignment)]
        count = count + len(assignment_repos)
        assignment_to_repos[assignment] = assignment_repos

    print("Downloading assignments")
    with alive_bar(total=count, force_tty=True) as bar:
        for assignment in assignments:
            assignment_repos = assignment_to_repos[assignment]
            for r in assignment_repos:
                folder = f"{LABS_DIR}/{ORG}/{assignment}/{r.name}"
                Repo.clone_from(r.clone_url, folder)
                bar()
