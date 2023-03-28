import time
import gspread
from gspread import Spreadsheet
from slack import WebClient
from gh_utils import return_repo, run_workflow
from gs_utils import returnGSheet, bulkCreateAndChangeURl


def upload_or_update(slack_client: WebClient, event: dict) -> None:
    text = event.get("text")
    if text.split()[-1] != "":
        gSheet = returnGSheet()
        try:
            verify_upload_sync(slack_client, event, text, gSheet)
        except gspread.exceptions.WorksheetNotFound:
            slack_client.chat_postMessage(
                channel=event.get("channel"),
                thread_ts=event.get("ts"),
                text=f"sorry sheet: {text.split()[-1]} not found",
            )

    slack_client.chat_postMessage(
        channel=event.get("channel"),
        thread_ts=event.get("ts"),
        text="sheet name cannot be empty",
    )


def verify_upload_sync(
    slack_client: WebClient, event: dict, text: str, gSheet: Spreadsheet
):
    slack_client.chat_postMessage(
        channel=event.get("channel"),
        thread_ts=event.get("ts"),
        text=f"verifying sheet: {text.split()[-1]}",
    )
    sheet = gSheet.worksheet(text.split()[-1])
    repo = return_repo()
    values_list = sheet.get_all_records()
    bulkCreateAndChangeURl(values_list, sheet, repo, text.split()[0])
    slack_client.chat_postMessage(
        channel=event.get("channel"),
        thread_ts=event.get("ts"),
        text="upload done, syncing to cloud",
    )
    run_workflow()
    time.sleep(60)
    slack_client.chat_postMessage(
        channel=event.get("channel"),
        thread_ts=event.get("ts"),
        text=f"synced, @{event.get('user')} please verify the links",
    )
