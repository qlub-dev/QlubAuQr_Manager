from github.Repository import Repository
from gsheetsdb import connect
import streamlit as st
from google.oauth2.service_account import Credentials
from functools import cache
import time

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)


@cache
def returnConn():
    return connect(credentials=credentials)


@cache
def returnGSheet():
    conn = returnConn()
    try:
        return conn.get_workbook("QlubAuQR")
    except Exception:
        return conn.create("QlubAuQR")


def bulkCreateAndChangeURl(
        qrIdsList: list, sheet: str, repo: Repository, command: str
) -> None:
    if not qrIdsList:
        return
    conn = returnConn()
    for qrIds in qrIdsList:
        if qrIds.get("LandingURL") != "":
            if command == "upload":
                repo.create_file(
                    path=f'au/{qrIds.get("Ids")}.html',
                    message=f"created a new link for {qrIds.get('Ids')}",
                    content=f'<meta http-equiv="refresh" content="0; URL={qrIds.get("LandingURL")}" />',
                    branch="main",
                )

            elif command == "update":
                content = repo.get_contents(f"au/{qrIds.get('Ids')}.html", ref="main")
                repo.update_file(
                    path=content.path,
                    message=f"updated a new link for {qrIds.get('Ids')}",
                    content=f'<meta http-equiv="refresh" content="0; URL={qrIds.get("LandingURL")}" />',
                    sha=content.sha,
                    branch="main",
                )

        retry = True
        initial_time = 2
        while retry:
            try:
                cell = conn.find(sheet, f"{qrIds.get('Ids')}")
                conn.update(sheet, f"{cell.column_letter}{cell.row}", "Yes")
                retry = False
            except Exception:
                time.sleep(initial_time)
                initial_time = initial_time * 2 if initial_time < 60 else 10
