import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Neuromatch Academy Impact Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# PATHS
# =========================================================
PROCESSED_DIR = os.path.join("data", "processed")

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    master = pd.read_csv(os.path.join(PROCESSED_DIR, "master_student_program.csv"))
    daily_master = pd.read_csv(os.path.join(PROCESSED_DIR, "daily_master.csv"))
    program_metrics = pd.read_csv(os.path.join(PROCESSED_DIR, "program_metrics.csv"))
    return master, daily_master, program_metrics

master, daily_master, program_metrics = load_data()

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.title("Filters")

years = sorted(master["year"].dropna().unique().tolist())
programs = sorted(master["program_name"].dropna().unique().tolist())
countries = sorted(master["country"].dropna().unique().tolist())

selected_years = st.sidebar.multiselect("Select Year(s)", years, default=years)
selected_programs = st.sidebar.multiselect("Select Program(s)", programs, default=programs)
selected_countries = st.sidebar.multiselect("Select Country/Countries", countries, default=countries)

filtered_master = master[
    (master["year"].isin(selected_years)) &
    (master["program_name"].isin(selected_programs)) &
    (master["country"].isin(selected_countries))
].copy()

filtered_daily = daily_master[
    (daily_master["year"].isin(selected_years)) &
    (daily_master["program_name"].isin(selected_programs)) &
    (daily_master["country"].isin(selected_countries))
].copy()

filtered_program_metrics = program_metrics[
    (program_metrics["year"].isin(selected_years))
].copy()

# =========================================================
# TITLE
# =========================================================
st.title("📊 Neuromatch Academy Impact Dashboard")
st.markdown("Interactive dashboard for analyzing multi-year Neuromatch Academy program impact, engagement, learning outcomes, and student experience.")

# =========================================================
# OVERVIEW KPIs
# =========================================================
st.subheader("Overview")

total_students = filtered_master["user_id"].nunique()
avg_engagement = filtered_master["engagement_score"].mean()
avg_learning_gain = filtered_master["learning_gain"].mean()
avg_satisfaction = filtered_master["avg_satisfaction"].mean()
completion_rate = filtered_master["completion_status"].mean() * 100
dropout_rate = filtered_master["dropped_out"].mean() * 100

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total Students", f"{total_students:,}")
col2.metric("Avg Engagement", f"{avg_engagement:.2f}")
col3.metric("Avg Learning Gain", f"{avg_learning_gain:.2f}")
col4.metric("Avg Satisfaction", f"{avg_satisfaction:.2f}")
col5.metric("Completion Rate", f"{completion_rate:.1f}%")
col6.metric("Dropout Rate", f"{dropout_rate:.1f}%")

st.markdown("---")

# =========================================================
# PROGRAM COMPARISON
# =========================================================
st.subheader("Program Comparison")

prog_summary = filtered_master.groupby("program_name").agg(
    completion_rate=("completion_status", "mean"),
    avg_learning_gain=("learning_gain", "mean"),
    avg_satisfaction=("avg_satisfaction", "mean"),
    avg_engagement=("engagement_score", "mean"),
    dropout_rate=("dropped_out", "mean"),
    students=("user_id", "nunique")
).reset_index()

prog_summary["completion_rate"] *= 100
prog_summary["dropout_rate"] *= 100

c1, c2 = st.columns(2)

with c1:
    fig = px.bar(
        prog_summary.sort_values("completion_rate", ascending=False),
        x="program_name",
        y="completion_rate",
        title="Completion Rate by Program"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(
        prog_summary.sort_values("avg_learning_gain", ascending=False),
        x="program_name",
        y="avg_learning_gain",
        title="Average Learning Gain by Program"
    )
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    fig = px.bar(
        prog_summary.sort_values("avg_satisfaction", ascending=False),
        x="program_name",
        y="avg_satisfaction",
        title="Average Satisfaction by Program"
    )
    st.plotly_chart(fig, use_container_width=True)

with c4:
    fig = px.bar(
        prog_summary.sort_values("students", ascending=False),
        x="program_name",
        y="students",
        title="Students per Program"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================================================
# ENGAGEMENT & OUTCOMES
# =========================================================
st.subheader("Engagement & Outcomes")

c5, c6 = st.columns(2)

with c5:
    fig = px.histogram(
        filtered_master,
        x="engagement_score",
        nbins=25,
        title="Engagement Score Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with c6:
    fig = px.scatter(
        filtered_master,
        x="engagement_score",
        y="learning_gain",
        color="program_name",
        title="Engagement Score vs Learning Gain",
        hover_data=["user_id", "country"]
    )
    st.plotly_chart(fig, use_container_width=True)

attendance_completion = filtered_master.groupby("completion_status")[[
    "attendance_rate_curriculum", "attendance_rate_project"
]].mean().reset_index()

attendance_completion["completion_status"] = attendance_completion["completion_status"].map({
    0: "Did Not Complete",
    1: "Completed"
})

fig = px.bar(
    attendance_completion.melt(id_vars="completion_status", var_name="metric", value_name="value"),
    x="metric",
    y="value",
    color="completion_status",
    barmode="group",
    title="Attendance Rates by Completion Status"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================================================
# STUDENT EXPERIENCE
# =========================================================
st.subheader("Student Experience")

c7, c8 = st.columns(2)

with c7:
    fig = px.histogram(
        filtered_master,
        x="avg_satisfaction",
        nbins=10,
        title="Satisfaction Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with c8:
    fig = px.bar(
        filtered_master.groupby("program_name")["avg_ta_support"].mean().reset_index(),
        x="program_name",
        y="avg_ta_support",
        title="Average TA Support by Program"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================================================
# DROPOUT ANALYSIS
# =========================================================
st.subheader("Dropout Analysis")

c9, c10 = st.columns(2)

dropout_prog = filtered_master.groupby("program_name")["dropped_out"].mean().reset_index()
dropout_prog["dropped_out"] *= 100

with c9:
    fig = px.bar(
        dropout_prog,
        x="program_name",
        y="dropped_out",
        title="Dropout Rate by Program"
    )
    st.plotly_chart(fig, use_container_width=True)

with c10:
    reason_counts = filtered_master["reason"].value_counts(dropna=True).reset_index()
    reason_counts.columns = ["reason", "count"]

    fig = px.bar(
        reason_counts,
        x="reason",
        y="count",
        title="Dropout Reasons"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================================================
# COHORT / DIVERSITY ANALYSIS
# =========================================================
st.subheader("Cohort & Diversity Analysis")

c11, c12 = st.columns(2)

top_countries = filtered_master["country"].value_counts().head(10).reset_index()
top_countries.columns = ["country", "count"]

with c11:
    fig = px.bar(
        top_countries,
        x="country",
        y="count",
        title="Top 10 Countries by Student Count"
    )
    st.plotly_chart(fig, use_container_width=True)

edu_counts = filtered_master["education_level"].value_counts().reset_index()
edu_counts.columns = ["education_level", "count"]

with c12:
    fig = px.bar(
        edu_counts,
        x="education_level",
        y="count",
        title="Education Level Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

prior_nm = filtered_master.groupby("prior_neuromatch")["completion_status"].mean().reset_index()
prior_nm["completion_status"] *= 100
prior_nm["prior_neuromatch"] = prior_nm["prior_neuromatch"].map({0: "No", 1: "Yes"})

fig = px.bar(
    prior_nm,
    x="prior_neuromatch",
    y="completion_status",
    title="Completion Rate by Prior Neuromatch Participation"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================================================
# DAILY ENGAGEMENT TRENDS
# =========================================================
st.subheader("Daily Engagement Trends")

if not filtered_daily.empty:
    daily_trend = filtered_daily.groupby("day").agg(
        avg_curriculum_attendance=("attended_curriculum", "mean"),
        avg_project_attendance=("attended_project", "mean"),
        avg_zoom_minutes=("zoom_minutes", "mean")
    ).reset_index()

    daily_trend["avg_curriculum_attendance"] *= 100
    daily_trend["avg_project_attendance"] *= 100

    c13, c14 = st.columns(2)

    with c13:
        fig = px.line(
            daily_trend,
            x="day",
            y=["avg_curriculum_attendance", "avg_project_attendance"],
            title="Daily Attendance Trend (%)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c14:
        fig = px.line(
            daily_trend,
            x="day",
            y="avg_zoom_minutes",
            title="Average Zoom Minutes per Day"
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================================================
# PROGRAM METRICS TABLE
# =========================================================
st.subheader("Program Metrics Table")

display_cols = [
    "program_id", "year", "completion_rate",
    "avg_learning_gain", "avg_satisfaction",
    "dropout_rate", "engagement_score"
]

st.dataframe(filtered_program_metrics[display_cols], use_container_width=True)

# =========================================================
# DOWNLOAD
# =========================================================
st.subheader("Download Data")

csv = filtered_master.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Master Dataset",
    data=csv,
    file_name="filtered_master_student_program.csv",
    mime="text/csv"
)