from anchor import STUDENT_INFO_DIR, LABS_DIR, ANALYSIS_OUT_DIR, ASSIGNMENTS_DIR
import pandas as pd
import sqlite3 as db
from git import Repo
import re
from pathlib import Path
from alive_progress import alive_bar
import datetime

from config import ORG

STUDENT_INFO_FILE = f"{STUDENT_INFO_DIR}/{ORG}.csv"


def analyze_repo(repo_dir, lab, deadline):
    git_user = repo_dir.split(lab+"-")[-1]

    r = Repo(repo_dir)
    # eliminate commit by github bot
    commits = list(r.iter_commits())
    written_lines = sum([x.stats.total["insertions"] for x in commits[:-1]])
    deleted_lines = sum([x.stats.total["deletions"] for x in commits[:-1]])
    total_commits = len(commits)
    commits_before_dl = [commit for commit in commits if commit.committed_datetime.timestamp() <= deadline.timestamp()]
    written_lines_before_dl = sum([x.stats.total["insertions"] for x in commits_before_dl[:-1]])
    total_commits_before_dl = len(commits_before_dl)
    first_user_commit = None if total_commits == 1 else commits[-2].committed_datetime.date().strftime("%Y-%m-%d")
    last_user_commit = None if total_commits == 1 else commits[0].committed_datetime.date().strftime("%Y-%m-%d")
    repo_creation_date = commits[-1].committed_datetime.date().strftime("%Y-%m-%d")
    commit_summaries = [{"Date": x.committed_datetime.date().strftime("%Y-%m-%d"),
                         "Summary": x.summary,
                         "Insertions": x.stats.total["insertions"],
                         "Deletions": x.stats.total["deletions"],
                         "GitHub ID": git_user.lower(),
                         "Author": x.author
                         }
                        for x in commits]

    git_mail = None if total_commits < 2 else commits[1].committer.email
    if git_mail == "noreply@github.com":
        git_mail = None
    repo_summary = {"GitHub ID": git_user.lower(),
                    "Total insertions": written_lines,
                    "Total deletions": deleted_lines,
                    "Repo creation date": repo_creation_date,
                    "Total commits": total_commits,
                    "Total commits before DL": total_commits_before_dl,
                    "First commit": first_user_commit,
                    "Last commit": last_user_commit,
                    "Git email": git_mail
                    }

    return [repo_summary, commit_summaries]


def main(repo, lab, deadline, db_connection):
    lab_dir = f"{LABS_DIR}/{repo}/{lab}"
    lab_commits = f"{STUDENT_INFO_FILE}/"

    student_info = pd.read_csv(STUDENT_INFO_FILE)
    repo_dirs = [x.__str__() for x in Path(lab_dir).iterdir() if
                 x.is_dir() and re.match(".*" + lab + "-(\w+)", x.__str__()) is not None]

    git_names = [re.match(".*" + lab + "-(\w+)", x) for x in repo_dirs]
    repo_summaries = []
    commit_summaries = []
    with alive_bar(len(repo_dirs), dual_line=True, title='Analysis', force_tty=True) as bar:
        for repo_dir in repo_dirs:
            [repo_summary, cs] = analyze_repo(repo_dir, lab, deadline)
            repo_summaries.append(repo_summary)
            commit_summaries += cs
            bar()

    repo_df = pd.DataFrame(repo_summaries)
    commits_df = pd.DataFrame(commit_summaries)
    repo_df = repo_df.merge(student_info, on="GitHub ID", how="outer")
    repo_df.loc[repo_df["Email"].isna(), "Email"] = repo_df["Git email"]
    return repo_df, commits_df


if __name__ == '__main__':
    assignments_csv = pd.read_csv(f"{ASSIGNMENTS_DIR}/{ORG}.csv")
    assignments = assignments_csv["Assignment"].values
    deadlines = assignments_csv["Deadline"].values
    deadlines = [datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M') for deadline in deadlines]
    tmp = zip(assignments, deadlines)

    repo_dfs = []
    with db.connect(f'{ANALYSIS_OUT_DIR}/repo_data.db') as db_connection:
        for assignment, deadline in tmp:
            repo_df, commits_df = main(ORG, assignment, deadline, db_connection)
            lab_analysis_out = f"{ANALYSIS_OUT_DIR}/{ORG}/{assignment}"
            Path(lab_analysis_out).mkdir(parents=True, exist_ok=True)
            commits_df.to_csv(f"{lab_analysis_out}/commits.csv", index=False)
            repo_df.to_csv(f"{lab_analysis_out}/repos.csv", index=False)
            repo_df.to_sql(f'repo{assignment}', con=db_connection, if_exists='replace')
            repo_dfs.append(repo_df)

    all_repos_df = pd.concat(repo_dfs)


    def evaluate(d: pd.DataFrame):
        points = sum(
            d.apply(lambda r: 1 if r["Total commits before DL"] > 1 else 0.5 if r["Total commits"] > 1 else 0, axis=1))
        return points


    bonus_df = all_repos_df.groupby(["Name", "Surname"]).apply(evaluate)
    bonus_df.to_csv(f'{ANALYSIS_OUT_DIR}/{ORG}/bonus.csv')
