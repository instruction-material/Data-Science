import altair as alt
import pandas as pd
import streamlit as st
from main import SAMPLE, comparable_panels, load_observations

st.title("Compare days using a common scale")
rows = load_observations(SAMPLE)
if not rows:
    st.info("The dataset contains no observations.")
    st.stop()
days = list(dict.fromkeys(row["day"] for row in rows))
first_day = st.selectbox("First day", days)
second_day = st.selectbox("Second day", days, index=min(1, len(days) - 1))
comparison = comparable_panels(rows, first_day, second_day)
if comparison is None:
    st.info("Complete comparable_panels to compare two days on one scale.")
else:
    first, second, upper_limit = comparison
    st.caption(f"Shared check-in scale: 0 to {upper_limit}")
    for index, (day, selected) in enumerate(((first_day, first), (second_day, second)), 1):
        st.subheader(f"{index}. {day}")
        if not selected:
            st.info("No observations for the selected day.")
            continue
        table = pd.DataFrame(selected)[["room", "checkins"]]
        chart = alt.Chart(table).mark_bar().encode(
            x=alt.X("room:N", title="Room"),
            y=alt.Y("checkins:Q", title="Observed check-ins",
                    scale=alt.Scale(domain=[0, upper_limit], nice=False)),
            tooltip=[alt.Tooltip("room:N", title="Room"), alt.Tooltip("checkins:Q", title="Check-ins")],
        )
        st.altair_chart(chart, width="stretch", key=f"checkins-chart-{index}")
        st.table(table)
