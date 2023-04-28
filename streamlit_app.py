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
        conn = returnGSheet()
        try:
            sheet = conn.get_worksheet(sheet_name)
        except Exception:
            st.error(f"Worksheet '{sheet_name}' not found.")
            return
        repo = return_repo()
        try:
            rows = conn.select(f'SELECT * FROM "{sheet_name}"')
            records = [dict(row) for row in rows]
            bulkCreateAndChangeURl(records, sheet_name, repo, command)
            st.success("Operation completed successfully!")
        except Exception as e:
            st.error(f"failed to {command} the sheet, got {e}")

        if run_workflow():
            st.success("Workflow dispatched successfully.")
        else:
            st.error("Failed to dispatch the workflow.")


if __name__ == "__main__":
    main()
