from collections import defaultdict
from pathlib import Path
import sqlite3

import streamlit as st
import altair as alt
import pandas as pd


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="2025 FRC Scouting",
    #page_icon=":shopping_bags:",  # This is an emoji shortcode. Could be a URL too.
)


# -----------------------------------------------------------------------------
# Declare some useful functions.


def connect_db():
    """Connects to the sqlite database."""

    DB_FILENAME = Path(__file__).parent / "inventory.db"
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists

    return conn, db_was_just_created


def initialize_data(conn):
    """Initializes the inventory table with some data."""
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """
    INSERT INTO MatchData
        (
            Team_Number_Name,
            Alliance_Partner_1,
            Alliance_Partner_2,
            Match_Number,
            Match_Type,
            Ranking_Points,
            Match_Points,
            Auto_Score,
            Auto_Fuel,
            Auto_Hang,
            Teleop_Score,
            Teleop_Cycle_Count,
            Hang_Points,
            Auto_Notes,
            Teleop_Notes,
            Other_Notes
        )
    VALUES

        -- Iobotics FIRST MATCH
        ('8898 (Iobotics)', 2438, 314, 1, 'Qualification', 2, 18, 8, 5, 3, 10, 7, 4,
         'Good autonomous start', 'Consistent teleop cycles', 'Minor alignment issue'),

        ('2438 (Iobotics)', 8898, 67, 1, 'Qualification', 1, 14, 6, 4, 0, 8, 6, 0,
         'Collected fuel successfully', 'Good scoring consistency', 'Needs faster cycle time'),

        ('56225 (Iobotics)', 8740, 1234, 1, 'Qualification', 3, 21, 10, 7, 4, 11, 9, 5,
         'Strong autonomous scoring', 'High cycle count', 'Excellent match overall'),

        ('8740 (Iobotics)', 56225, 999, 1, 'Qualification', 2, 16, 7, 3, 2, 9, 6, 3,
         'Successful auto routine', 'Stable teleop performance', 'Minor defense encountered'),

        ('8741 (Iobotics)', 0, 314, 1, 'Qualification', 0, 11, 5, 2, 0, 6, 5, 0,
         'Auto partially completed', 'Some missed cycles', 'Driver communication needed'),

        -- Other Teams FIRST MATCH
        ('314 (PiBots)', 1234, 67, 1, 'Qualification', 2, 17, 8, 4, 3, 9, 7, 4,
         'Reliable autonomous', 'Good fuel handling', 'No major issues'),

        ('1234 (CountBots)', 314, 0, 1, 'Qualification', 1, 13, 4, 3, 1, 9, 5, 2,
         'Average autonomous run', 'Steady scoring', 'Slow start to teleop'),

        ('67 (PunahouBots)', 999, 8740, 1, 'Qualification', 3, 20, 9, 6, 4, 11, 8, 5,
         'Excellent autonomous', 'Fast cycling', 'Strong endgame'),

        ('0 (ZipBots)', 8741, 56225, 1, 'Qualification', 0, 9, 3, 2, 0, 6, 4, 0,
         'Limited autonomous scoring', 'Improved teleop performance', 'Robot stopped briefly'),

        ('999 (MaxBots)', 67, 2438, 1, 'Qualification', 2, 15, 6, 5, 2, 8, 6, 3,
         'Good autonomous path', 'Consistent cycles', 'Good defensive positioning'),

        -- Iobotics SECOND MATCH
        ('8898 (Iobotics)', 8741, 1234, 2, 'Qualification', 3, 23, 11, 8, 4, 12, 10, 5,
         'Excellent autonomous scoring', 'Very fast cycles', 'Strong match performance'),

        ('2438 (Iobotics)', 56225, 999, 2, 'Qualification', 2, 17, 7, 5, 2, 10, 7, 3,
         'Good fuel collection', 'Consistent teleop', 'Minor defense interference'),

        ('8741 (Iobotics)', 314, 0, 2, 'Qualification', 1, 12, 5, 3, 1, 7, 5, 2,
         'Partial autonomous completion', 'Average cycle speed', 'Needs endgame improvement'),

        ('8740 (Iobotics)', 67, 1234, 2, 'Qualification', 2, 19, 9, 6, 3, 10, 8, 4,
         'Reliable autonomous routine', 'Strong teleop scoring', 'Good climb attempt'),

        ('56225 (Iobotics)', 999, 8741, 2, 'Qualification', 3, 22, 10, 7, 4, 12, 9, 5,
         'Strong fuel scoring', 'High cycle efficiency', 'Successful endgame'),

        -- Other Teams SECOND MATCH
        ('314 (PiBots)', 2438, 56225, 2, 'Qualification', 2, 16, 7, 4, 2, 9, 7, 3,
         'Good autonomous', 'Consistent scoring', 'Minor mechanical issue'),

        ('1234 (CountBots)', 8740, 0, 2, 'Qualification', 1, 14, 6, 3, 1, 8, 6, 2,
         'Average auto performance', 'Moderate cycle speed', 'Missed one endgame attempt'),

        ('67 (PunahouBots)', 8898, 314, 2, 'Qualification', 3, 21, 9, 7, 4, 11, 9, 5,
         'Excellent autonomous', 'Fast teleop cycles', 'Strong defensive play'),

        ('0 (ZipBots)', 1234, 999, 2, 'Qualification', 0, 10, 4, 2, 0, 6, 5, 0,
         'Limited auto scoring', 'Slow cycling', 'Robot had trouble with alignment'),

        ('999 (MaxBots)', 8741, 67, 2, 'Qualification', 2, 18, 8, 5, 3, 10, 7, 4,
         'Good autonomous routine', 'Reliable teleop', 'Successful hang'),

        -- Iobotics THIRD MATCH
        ('8898 (Iobotics)', 314, 8740, 3, 'Qualification', 3, 24, 12, 8, 4, 13, 10, 5,
         'Excellent autonomous run', 'High scoring efficiency', 'Best performance so far'),

        ('2438 (Iobotics)', 67, 999, 3, 'Qualification', 2, 16, 7, 5, 2, 9, 7, 3,
         'Good autonomous scoring', 'Consistent cycles', 'Minor defensive pressure')
        """
    )
    conn.commit()


def load_data(conn):
    """Loads the inventory data from the database."""
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM inventory")
        data = cursor.fetchall()
    except:
        return None

    df = pd.DataFrame(
        data,
        columns=[
            "Team_Number_Name", 
            "Alliance_Partner_1", 
            "Alliance_Partner_2", 
            "Match_Number", 
            "Match_Type", 
            "Ranking_Points", 
            "Match_Points", 
            "Auto_Score", 
            "Auto_Fuel", 
            "Auto_Hang", 
            "Teleop_Score", 
            "Teleop_Cycle_Count", 
            "Hang_Points", 
            "Auto_Notes", 
            "Teleop_Notes", 
            "Other_Notes",
        ],
    )

    return df


def update_data(conn, df, changes):
    """Updates the inventory data in the database."""
    cursor = conn.cursor()

    if changes["edited_rows"]:
        deltas = st.session_state.match_table["edited_rows"]
        rows = []

        for i, delta in deltas.items():
            row_dict = df.iloc[i].to_dict()
            row_dict.update(delta)
            rows.append(row_dict)

        cursor.executemany(
            """
            UPDATE inventory
            SET
                Team_Number_Name = :Team_Number_Name, 
                Alliance_Partner_1 = :Alliance_Partner_1,
                Alliance_Partner_2 = :Alliance_Partner_2,
                Match_Number = :Match_Number,
                Match_Type = :Match_Type,
                Ranking_Points = :Ranking_Points,
                Match_Points = :Match_Points,
                Auto_Score = :Auto_Score,
                Auto_Fuel = :Auto_Fuel,
                Auto_Hang = :Auto_Hang,
                Teleop_Score = :Teleop_Score,
                Teleop_Cycle_Count = :Teleop_Cycle_Count,
                Hang_Points = :Hang_Points,
                Auto_Notes = :Auto_Notes,
                Teleop_Notes = :Teleop_Notes,
                Other_Notes = :Other_Notes

            WHERE Team_Number_Name = :Team_Number_Name
            """,
            rows,
        )

    if changes["added_rows"]:
        cursor.executemany(
            """
            INSERT INTO MatchData
                (Team_Number_Name, Alliance_Partner_1, Alliance_Partner_2, Match_Number, Match_Type, Ranking_Points, Match_Points, Auto_Score, Auto_Fuel, Auto_Hang, Teleop_Score, Teleop_Cycle_Count, Hang_Points, Auto_Notes, Teleop_Notes, Other_Notes)
            VALUES
                (:Team_Number_Name, :Alliance_Partner_1, :Alliance_Partner_2, :Match_Number, :Match_Type, :Ranking_Points, :Match_Points, :Auto_Score, :Auto_Fuel, :Auto_Hang, :Teleop_Score, :Teleop_Cycle_Count, :Hang_Points, :Auto_Notes, :Teleop_Notes, :Other_Notes)
            """,
            (defaultdict(lambda: None, row) for row in changes["added_rows"]),
        )

    if changes["deleted_rows"]:
        cursor.executemany(
            "DELETE FROM inventory WHERE id = :id",
            ({"id": int(df.loc[i, "id"])} for i in changes["deleted_rows"]),
        )

    conn.commit()


# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.

# Set the title that appears at the top of the page.
"""
# 2025 FRC Scouting

**This is a test website**
This page is awesome :)
"""

st.info(
    """
    Use the table below to add, remove, and edit matches.
    And don't forget to submit after.
    """
)

# Connect to database and create table if needed
conn, db_was_just_created = connect_db()

# Initialize data.
if db_was_just_created:
    initialize_data(conn)
    st.toast("Database with current matches.")

# Load data from database
df = load_data(conn)

# Display data with editable table
edited_df = st.data_editor(
    df,
    disabled=["id"],  # Don't allow editing the 'id' column.
    num_rows="dynamic",  # Allow appending/deleting rows.
    #column_config={
        # Show dollar sign before price columns.
        #"price": st.column_config.NumberColumn(format="$%.2f"),
        #"Teleop_Score": st.column_config.NumberColumn(format="$%.2f"),
       # "Match_Points": st.column_config.NumberColumn(format="$%.2f"),
    #},
    key="match_table",
)

has_uncommitted_changes = any(len(v) for v in st.session_state.match_table.values())

st.button(
    "Commit changes",
    type="primary",
    disabled=not has_uncommitted_changes,
    # Update data in database
    on_click=update_data,
    args=(conn, df, st.session_state.match_table),
)


# -----------------------------------------------------------------------------
# Now some cool charts

# Add some space
""
""
""

st.subheader("Match Points", divider="red")

#need_to_reorder = df[df["Auto_Score"] < df["reorder_point"]].loc[:, "Team_NumberName"]

#if len(need_to_reorder) > 0:
#    items = "\n".join(f"* {name}" for name in need_to_reorder)

#    st.error(f"We're running dangerously low on the items below:\n {items}")

#""
#average of match/ranking points
team_averages = (
    df.groupby("Team_NumberName", as_index=False)
    .agg({
        "Match_Points": "mean",
        "Ranking_Points": "mean",
    })
)

""

st.altair_chart(
    # Layer 1: Bar chart.
    alt.Chart(df)
    .mark_bar(
        orient="horizontal",
    )
    .encode(
        x="Match_Points",
        y="Team_NumberName",
    )
    # Layer 2: Chart showing the average point.
    + alt.Chart(team_averages)
    .mark_point(
        shape="diamond",
        filled=True,
        size=50,
        color="salmon",
        opacity=1,
    )
    .encode(
        x="Match_Points",
        y="Team_NumberName",
    ),
    use_container_width=True,
)

st.caption("NOTE: The :diamonds: location shows the match point average of the team.")

""
""
""

# -----------------------------------------------------------------------------



st.subheader("Team Rankings", divider="orange")

""
""

st.altair_chart(
    alt.Chart(team_averages)
    .mark_bar(orient="horizontal")
    .encode(
        x=alt.X("Ranking_Points", title="Average Ranking Points"),
        y=alt.Y("Team_NumberName").sort("x"),
    ),
    use_container_width=True,
)
