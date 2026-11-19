import altair as alt
import pandas as pd
import streamlit as st
from main import SAMPLE, filter_observations, load_observations

st.title("Filter observations by day and room")
rows = load_observations(SAMPLE)
if not rows:
    st.info("The dataset contains no observations.")
    st.stop()
day = st.selectbox("Day", list(dict.fromkeys(row["day"] for row in rows)))
room = st.selectbox("Room", ["All rooms", *sorted({row["room"] for row in rows})])
selected = filter_observations(rows, day, room)
if selected is None:
    st.info("Complete filter_observations to apply both controls.")
elif not selected:
    st.warning(f"No observation for {room} on {day}.")
else:
    table = pd.DataFrame(selected)[["room", "checkins"]]
    chart = alt.Chart(table).mark_bar().encode(
        x=alt.X("room:N", title="Room"),
        y=alt.Y("checkins:Q", title="Observed check-ins", scale=alt.Scale(zero=True)),
        tooltip=[alt.Tooltip("room:N", title="Room"), alt.Tooltip("checkins:Q", title="Check-ins")],
    )
    st.metric("Observed check-ins", int(table["checkins"].sum()))
    st.altair_chart(chart, width="stretch")
    st.table(table)
    st.caption(f"{day}, {room}. Rows shown: {len(selected)}.")
