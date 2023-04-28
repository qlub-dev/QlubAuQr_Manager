import json
from github import Github as gh
import streamlit as st
from github import Repository
from functools import cache
import requests

git = gh(st.secrets.github_secrets.PAT)


@cache
def return_repo() -> Repository:
    return git.get_repo("qlub-dev/l-qlub-io")


def run_workflow() -> bool:
    header = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {st.secrets.github_secrets.AccessToken}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    data = {
        "ref": "main",
    }

    wf_response = requests.post(
        "https://api.github.com/repos/qlub-dev/l-qlub-io/actions/workflows/48694456/dispatches",
        headers=header,
        data=json.dumps(data),
    )
    return wf_response.status_code == 204
