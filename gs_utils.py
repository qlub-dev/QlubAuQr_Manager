import gspread
import time
import streamlit as st
from gspread import Worksheet
from github import Repository
from google.oauth2 import service_account
from functools import cache

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)


@cache
def returnClient():
    return gspread.authorize(credentials=credentials)


@cache
def returnGSheet():
    client = returnClient()
    try:
        return client.open("QlubAuQR")
    except gspread.SpreadsheetNotFound:
        return client.create("QlubAuQR")


def bulkCreateAndChangeURl(
    qrIdsList: list, sheet: Worksheet, repo: Repository, command: str
) -> None:
    if not qrIdsList:
        return
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
                cell = sheet.find(f"{qrIds.get('Ids')}")
                sheet.update_cell(cell.row, 4, "Yes")
                retry = False
            except gspread.exceptions.APIError:
                time.sleep(initial_time)
                initial_time = initial_time * 2 if initial_time < 60 else 10
