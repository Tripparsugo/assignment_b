# do not move the anchor or the ship drifts
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.resolve()
GITHUB_TOKEN_LOCATION = f"{PROJECT_ROOT}/secrets/github_token.txt"
GITHUB_TOKEN = None
STUDENT_INFO_DIR = f"{PROJECT_ROOT}/in/student_info/"
LABS_DIR = f"{PROJECT_ROOT}/download/labs"
ANALYSIS_OUT_DIR = f"{PROJECT_ROOT}/out/analysis_out"
ASSIGNMENTS_DIR = f"{PROJECT_ROOT}/in/assignments"

to_make = [STUDENT_INFO_DIR, LABS_DIR, ANALYSIS_OUT_DIR, ASSIGNMENTS_DIR]

for tm in to_make:
    pathlib.Path(tm).mkdir(exist_ok=True, parents=True)

if pathlib.Path(GITHUB_TOKEN_LOCATION).is_file():
    with open(GITHUB_TOKEN_LOCATION) as f:
        lines = f.readlines()
        if len(lines) == 0:
            raise RuntimeError("Missing Github token. Set the GH token in secrets/github_token.txt")
        GITHUB_TOKEN = lines[0]
