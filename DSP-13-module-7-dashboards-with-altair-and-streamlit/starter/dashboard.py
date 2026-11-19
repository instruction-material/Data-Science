import altair as alt
import pandas as pd
import streamlit as st
from main import SAMPLE, load_observations, summarize_day

st.title("Room check-ins by day")
rows = load_observations(SAMPLE)
if not rows:
    st.info("The dataset contains no observations.")
    st.stop()
day = st.selectbox("Day", list(dict.fromkeys(row["day"] for row in rows)))
result = summarize_day(rows, day)
if result is None:
    st.info("Complete summarize_day to display the selected day's observations.")
else:
    selected, total = result
    if not selected:
        st.info("No room observations are available for the selected day.")
    else:
        chart = alt.Chart(pd.DataFrame(selected)).mark_bar().encode(
            x=alt.X("room:N", title="Room"),
            y=alt.Y("checkins:Q", title="Observed check-ins", scale=alt.Scale(zero=True)),
            tooltip=[alt.Tooltip("room:N", title="Room"), alt.Tooltip("checkins:Q", title="Check-ins")],
        )
        st.metric("Observed check-ins", total)
        st.altair_chart(chart, width="stretch")
        st.table(pd.DataFrame(selected)[["room", "checkins"]])
        st.caption(f"{day}: {len(selected)} room observations. Check-ins can include repeat visits.")
