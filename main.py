import gspread
import streamlit as st
from gs_utils import (
    returnGSheet,
    bulkCreateAndChangeURl,
)
from gh_utils import return_repo, run_workflow


def main():
    st.title("QlubAuQR Manager")
    sheet_name = st.text_input("Enter the sheet name:")
    command = st.selectbox("Choose an action:", ["upload", "update"])
    submit_button = st.button("Submit")

    if submit_button and sheet_name:
        gsheet = returnGSheet()
        try:
            sheet = gsheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            st.error(f"Worksheet '{sheet_name}' not found.")
            return
        repo = return_repo()
        try:
            bulkCreateAndChangeURl(sheet.get_all_records(), sheet, repo, command)
            st.success("Operation completed successfully!")
        except Exception as e:
            st.error(f"failed to {command} the sheet, got {e}")

        if run_workflow():
            st.success("Workflow dispatched successfully.")
        else:
            st.error("Failed to dispatch the workflow.")


if __name__ == "__main__":
    main()
