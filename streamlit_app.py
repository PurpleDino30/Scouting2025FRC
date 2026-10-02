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

    DB_FILENAME = Path(__file__).parent / "MatchData.db"
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists

    return conn, db_was_just_created


def initialize_data(conn):
    """Initializes the match table with sample data."""
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS MatchData (
            Team_Number INTEGER NOT NULL,
            Alliance_Partner_1 INTEGER,
            Alliance_Partner_2 INTEGER,
            Match_Number INTEGER NOT NULL,
            Match_Type TEXT,
            Ranking_Points INTEGER,
            Match_Points INTEGER,
            Auto_Score INTEGER,
            Auto_Fuel INTEGER,
            Auto_Hang INTEGER,
            Teleop_Score INTEGER,
            Teleop_Cycle_Count INTEGER,
            Hang_Points INTEGER,
            Auto_Notes TEXT,
            Teleop_Notes TEXT,
            Other_Notes TEXT, 

            PRIMARY KEY (Match_Number, Team_Number)
        )
        """
    )

    cursor.execute("SELECT 1 FROM MatchData LIMIT 1")
    if cursor.fetchone() is None:
        cursor.execute(
            """
            INSERT INTO MatchData (
                Team_Number,
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
                (8898, 2438, 314, 1, 'Qualification', 2, 18, 8, 5, 3, 10, 7, 4,
                 'Good autonomous start', 'Consistent teleop cycles', 'Minor alignment issue'),
                (2438, 8898, 67, 1, 'Qualification', 1, 14, 6, 4, 0, 8, 6, 0,
                 'Collected fuel successfully', 'Good scoring consistency', 'Needs faster cycle time'),
                (56225, 8740, 1234, 1, 'Qualification', 3, 21, 10, 7, 4, 11, 9, 5,
                 'Strong autonomous scoring', 'High cycle count', 'Excellent match overall'),
                (8740, 56225, 999, 1, 'Qualification', 2, 16, 7, 3, 2, 9, 6, 3,
                 'Successful auto routine', 'Stable teleop performance', 'Minor defense encountered'),
                (8741, 0, 314, 1, 'Qualification', 0, 11, 5, 2, 0, 6, 5, 0,
                 'Auto partially completed', 'Some missed cycles', 'Driver communication needed'),
                (314, 1234, 67, 1, 'Qualification', 2, 17, 8, 4, 3, 9, 7, 4,
                 'Reliable autonomous', 'Good fuel handling', 'No major issues'),
                (1234, 314, 0, 1, 'Qualification', 1, 13, 4, 3, 1, 9, 5, 2,
                 'Average autonomous run', 'Steady scoring', 'Slow start to teleop'),
                (67, 999, 8740, 1, 'Qualification', 3, 20, 9, 6, 4, 11, 8, 5,
                 'Excellent autonomous', 'Fast cycling', 'Strong endgame'),
                (0, 8741, 56225, 1, 'Qualification', 0, 9, 3, 2, 0, 6, 4, 0,
                 'Limited autonomous scoring', 'Improved teleop performance', 'Robot stopped briefly'),
                (999, 67, 2438, 1, 'Qualification', 2, 15, 6, 5, 2, 8, 6, 3,
                 'Good autonomous path', 'Consistent cycles', 'Good defensive positioning'),
                (8898, 8741, 1234, 2, 'Qualification', 3, 23, 11, 8, 4, 12, 10, 5,
                 'Excellent autonomous scoring', 'Very fast cycles', 'Strong match performance'),
                (2438, 56225, 999, 2, 'Qualification', 2, 17, 7, 5, 2, 10, 7, 3,
                'Reliable autonomous routine', 'Strong teleop scoring', 'Good climb attempt'),
                (56225, 999, 8741, 2, 'Qualification', 3, 22, 10, 7, 4, 12, 9, 5,
                 'Strong fuel scoring', 'High cycle efficiency', 'Successful endgame'),
                (314, 2438, 56225, 2, 'Qualification', 2, 16, 7, 4, 2, 9, 7, 3,
                 'Good autonomous', 'Consistent scoring', 'Minor mechanical issue'),
                (1234, 8740, 0, 2, 'Qualification', 1, 14, 6, 3, 1, 8, 6, 2,
                 'Average auto performance', 'Moderate cycle speed', 'Missed one endgame attempt'),
                (67, 8898, 314, 2, 'Qualification', 3, 21, 9, 7, 4, 11, 9, 5,
                 'Excellent autonomous', 'Fast teleop cycles', 'Strong defensive play'),
                (0, 1234, 999, 2, 'Qualification', 0, 10, 4, 2, 0, 6, 5, 0,
                 'Limited auto scoring', 'Slow cycling', 'Robot had trouble with alignment'),
                (999, 8741, 67, 2, 'Qualification', 2, 18, 8, 5, 3, 10, 7, 4,
                 'Good autonomous routine', 'Reliable teleop', 'Successful hang'),
                (8898, 314, 8740, 3, 'Qualification', 3, 24, 12, 8, 4, 13, 10, 5,
                 'Excellent autonomous run', 'High scoring efficiency', 'Best performance so far'),
                (2438, 67, 999, 3, 'Qualification', 2, 16, 7, 5, 2, 9, 7, 3,
                 'Good autonomous scoring', 'Consistent cycles', 'Minor defensive pressure')
            """
        )

    conn.commit()


def load_data(conn):
    """Loads the MatchData data from the database."""
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM MatchData")
        data = cursor.fetchall()
    except:
        return None

    df = pd.DataFrame(
        data,
        columns=[
            "Team_Number", 
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
    """Updates the MatchData data in the database."""
    cursor = conn.cursor()

    if changes["edited_rows"]:
        for i, delta in changes["edited_rows"].items():
            old_match_number = int(df.iloc[i]["Match_Number"])
            old_team_number = int(df.iloc[i]["Team_Number"])
            
            new_match_number = int(
                delta.get("Match_Number", old_match_number)
            )
            new_team_number = int(
                delta.get("Team_Number", old_team_number)
            )

            try:
                cursor.execute(
                    """
                    UPDATE MatchData
                    SET
                        Team_Number = :new_team_number,
                        Alliance_Partner_1 = :Alliance_Partner_1,
                        Alliance_Partner_2 = :Alliance_Partner_2,
                        Match_Number = :new_match_number,
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
                    WHERE Team_Number = :old_team_number
                      AND Match_Number = :old_match_number
                    """,
                    {
                        "new_match_number": new_match_number,
                        "new_team_number": new_team_number,
                        "old_match_number": old_match_number,
                        "old_team_number": old_team_number,
                        "Alliance_Partner_1": delta.get(
                            "Alliance_Partner_1",
                            df.iloc[i]["Alliance_Partner_1"],
                        ),
                        "Alliance_Partner_2": delta.get(
                            "Alliance_Partner_2",
                            df.iloc[i]["Alliance_Partner_2"],
                        ),
                        "Match_Type": delta.get(
                            "Match_Type",
                            df.iloc[i]["Match_Type"],
                        ),
                        "Ranking_Points": delta.get(
                            "Ranking_Points",
                            df.iloc[i]["Ranking_Points"],
                        ),
                        "Match_Points": delta.get(
                            "Match_Points",
                            df.iloc[i]["Match_Points"],
                        ),
                        "Auto_Score": delta.get(
                            "Auto_Score",
                            df.iloc[i]["Auto_Score"],
                        ),
                        "Auto_Fuel": delta.get(
                            "Auto_Fuel",
                            df.iloc[i]["Auto_Fuel"],
                        ),
                        "Auto_Hang": delta.get(
                            "Auto_Hang",
                            df.iloc[i]["Auto_Hang"],
                        ),
                        "Teleop_Score": delta.get(
                            "Teleop_Score",
                            df.iloc[i]["Teleop_Score"],
                        ),
                        "Teleop_Cycle_Count": delta.get(
                            "Teleop_Cycle_Count",
                            df.iloc[i]["Teleop_Cycle_Count"],
                        ),
                        "Hang_Points": delta.get(
                            "Hang_Points",
                            df.iloc[i]["Hang_Points"],
                        ),
                        "Auto_Notes": delta.get(
                            "Auto_Notes",
                            df.iloc[i]["Auto_Notes"],
                        ),
                        "Teleop_Notes": delta.get(
                            "Teleop_Notes",
                            df.iloc[i]["Teleop_Notes"],
                        ),
                        "Other_Notes": delta.get(
                            "Other_Notes",
                            df.iloc[i]["Other_Notes"],
                        ),
                    },
                )
            except sqlite3.IntegrityError:
                st.error(
                    f"Match {new_match_number} / Team {new_team_number} "
                    "already exists."
                )
                conn.rollback()
                return

    if changes["added_rows"]:
        cursor.executemany(
            """
            INSERT INTO MatchData (
                Team_Number, 
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
            VALUES (
            :Team_Number, 
            :Alliance_Partner_1, 
            :Alliance_Partner_2, 
            :Match_Number, 
            :Match_Type, 
            :Ranking_Points, 
            :Match_Points, 
            :Auto_Score, 
            :Auto_Fuel, 
            :Auto_Hang, 
            :Teleop_Score, 
            :Teleop_Cycle_Count, 
            :Hang_Points, 
            :Auto_Notes, 
            :Teleop_Notes, 
            :Other_Notes
            )
            """,
            (defaultdict(lambda: None, row) 
             for row in changes["added_rows"]),
        )

    if changes["deleted_rows"]:
        deleted_rows = []

        for i in changes["deleted_rows"]:
            row = df.iloc[i]
            deleted_rows.append(
                {"Match_Number": int(row["Match_Number"]), 
                 "Team_Number": int(row["Team_Number"]),
                 })
        cursor.executemany(
            "DELETE FROM MatchData " \
            "WHERE Match_Number = :Match_Number " \
            "AND Team_Number = :Team_Number",
            deleted_rows,
        )

    conn.commit()


# -----------------------------------------------------------------------------
# Draw the actual page, starting with the MatchData table.

# Set the title that appears at the top of the page.
"""
# 2025 FRC Scouting

**This page is awesome :D**
 - used from a template
 - refined w/ ChatGPT
 - very very verrrry glitchy :{D
"""

st.info(
    """
    Use the table below to add, remove, and edit matches.
    And please submit after.
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
    #disabled=["Match_Number", "Team_Number"],  # Don't allow editing the 'id' column.
    num_rows="dynamic",  # Allow appending/deleting rows.
    hide_index=True,  # Hide the index column.
    #column_config={
        # Show dollar sign before price columns.
        #"price": st.column_config.NumberColumn(format="$%.2f"),
        #"Teleop_Score": st.column_config.NumberColumn(format="$%.2f"),
       # "Match_Points": st.column_config.NumberColumn(format="$%.2f"),
    #},
    key="match_table",
)

has_uncommitted_changes = any(len(v) for v in st.session_state.match_table.values())

if st.button(
    "Commit changes",
    type="primary",
    disabled=not has_uncommitted_changes,
):
    update_data(conn, df, st.session_state.match_table)
    st.success("Changes committed to database.")
    st.rerun()


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
    df.groupby("Team_Number", as_index=False)
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
        y="Team_Number",
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
        y="Team_Number",
    ),
    width='stretch',
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
        y=alt.Y("Team_Number").sort("x"),
    ),
    width='stretch',
)
