# Neuromatch Academy Impact Analytics System

An end-to-end analytics project simulating and evaluating **multi-year Neuromatch Academy program data** across multiple courses, with a focus on:

- **program impact evaluation**
- **student engagement**
- **learning outcomes**
- **student experience**
- **dropout and retention**
- **TA / pod-based learning structure**
- **interactive decision-support dashboards**

This project was designed to mirror the kinds of **data analysis, reporting, and operational support workflows** needed for large-scale global educational programs like **Neuromatch Academy**.

---

## Project Objective

The goal of this project is to build a realistic **education analytics pipeline** that can:

- simulate multi-program academy data
- clean and merge multi-source datasets
- compute standardized program metrics
- generate insights for leadership and course teams
- provide an interactive dashboard for exploration and reporting

The project is intentionally designed around workflows such as:

- application analysis
- student selection outcomes
- pod and TA structure
- daily attendance and engagement tracking
- surveys and assessments
- support requests and dropout trends
- annual / program-level impact reporting

---

## Demo

### Short Demo GIF *(placeholder)*
<p align="center">
  <img src="assets/demo.gif" alt="Project Demo GIF" width="900"/>
</p>

> Add a short GIF here later showing filters, KPIs, and 2–3 dashboard interactions.

---

## Dashboard Screenshots *(placeholders)*

### Dashboard Overview
<p align="center">
  <img src="assets/dashboard_overview.png" alt="Dashboard Overview" width="900"/>
</p>

### Program Comparison View
<p align="center">
  <img src="assets/program_comparison.png" alt="Program Comparison" width="900"/>
</p>

### Engagement & Outcomes View
<p align="center">
  <img src="assets/engagement_outcomes.png" alt="Engagement and Outcomes" width="900"/>
</p>

### Cohort / Diversity Analysis
<p align="center">
  <img src="assets/cohort_analysis.png" alt="Cohort Analysis" width="900"/>
</p>

---

## Key Features

- **Synthetic data generation** aligned to Neuromatch Academy workflow
- **Relational multi-table schema** for realistic educational operations
- **Data cleaning and validation pipeline**
- **Master student-program dataset creation**
- **Derived program-level KPI generation**
- **Exploratory analysis and impact insights**
- **Interactive Streamlit dashboard**
- **Structured analytics workflow suitable for nonprofit / education reporting**

---

## Programs Simulated

This project simulates multi-year offerings of the following academy programs:

- Computational Neuroscience
- Deep Learning
- Computational Tools for Climate Science
- NeuroAI

Each program includes simulated:

- students
- TAs
- pods
- project groups
- applications
- engagement records
- assessments
- surveys
- support requests
- dropouts
- pod check-ins

---

## Project Structure

```bash
academy-impact-analytics/
│
├── data/
│   ├── raw/                  # Raw synthetic CSV files
│   ├── cleaned/              # Cleaned CSV files
│   └── processed/            # Final merged / derived datasets
│
├── docs/
│   └── schema.md             # Dataset schema and relationships
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_data_merging.ipynb
│   └── 03_analysis.ipynb
│
├── dashboard/
│   └── app.py                # Streamlit dashboard
│
├── reports/
│   └── initial_findings.md   # Key insights and observations
│
├── src/
│   └── generate_data.py      # Synthetic data generation pipeline
│
├── assets/                   # GIFs, screenshots, visuals
│
├── README.md
└── requirements.txt
```

## Data Pipeline Overview

### 1. Schema Design

A structured, relational schema was designed to simulate a realistic academy operations and analytics environment.

### 2. Synthetic Data Generation

A custom Python-based generator was built to populate all CSV files with realistic values and relationships, including:

- application scores
- program enrollments
- pod structures
- TA assignments
- attendance behavior
- learning assessments
- surveys
- support operations

### 3. Data Cleaning

Each table is individually cleaned and validated for:

- missing values
- duplicates
- datatype consistency
- category consistency
- key integrity checks

### 4. Data Merging

All cleaned datasets are merged into:

`master_student_program.csv`
`daily_master.csv`
`program_metrics.csv`

### 5. Analysis

Core program impact and engagement insights are extracted via EDA and reporting.

### 6. Dashboarding

A Streamlit dashboard provides interactive access to:

- filters
- KPIs
- program comparisons
- engagement patterns
- dropout analysis
- diversity views

## Dataset Schema (High-Level)

The system includes the following core tables:

`programs.csv`

`users.csv`

`applications.csv`

`pods.csv`

`project_groups.csv`

`ta_assignments.csv`

`daily_engagement.csv`

`assessments.csv`

`surveys.csv`

`dropouts.csv`

`support_requests.csv

`ta_feedback.csv`

`pod_checkins.csv`

`program_metrics.csv` (derived)

A full description of all columns, PK/FK structure, and relationships is available in:

```
docs/schema.md
```
## Key Derived Outputs
`master_student_program.csv`

A student-level analytics table containing:

- demographic features
- application outcomes
- engagement metrics
- assessment scores
- survey outcomes
- dropout/support indicators

`daily_master.csv`

A day-level enriched dataset useful for:

- attendance trends
- engagement monitoring
- daily participation analysis

`program_metrics.csv`

A program-level KPI table including:

- completion rate
- average learning gain
- average satisfaction
- dropout rate
- engagement score

## Example Questions This Project Can Answer
1. Which program shows the strongest learning gains?
2. How does engagement relate to completion?
3. Which cohorts are most at risk of dropping out?
4. How does TA support affect student satisfaction?
5. What differences exist across programs and years?
6. How does prior Neuromatch participation relate to completion?
7. What are the most common support issues?

## Dashboard Capabilities

The Streamlit dashboard includes:

- Year filter
- Program filter
- Country filter

And visual sections for:

- Overview KPIs
- Program comparison
- Engagement & outcomes
- Student experience
- Dropout analysis
- Cohort / diversity analysis
- Daily engagement trends
- Program metrics summary table

## Tech Stack
- Python
- Pandas
- NumPy
- Faker
- Matplotlib
- Plotly
- Streamlit
- Jupyter Notebook


## How to Run

### 1. Clone the repository
```
git clone <your-repo-link>
cd academy-impact-analytics
```
### 2. Install dependencies
```
pip install -r requirements.txt
```
### 3. Generate synthetic data
```
python src/generate_data.py
```
### 4. Run notebooks (optional but recommended)

Open and run:
```
notebooks/01_data_cleaning.ipynb
notebooks/02_data_merging.ipynb
notebooks/03_analysis.ipynb
```
### 5. Launch dashboard
```
streamlit run dashboard/app.py
```

## Suggested `requirements.txt`

```
pandas
numpy
faker
matplotlib
plotly
streamlit
jupyter
```

## Future Improvements

Potential future extensions include:

- more realistic cohort matching / pod formation logic
- predictive dropout modeling
- NLP-based open feedback analysis
- TA performance benchmarking
- automated PDF impact report generation
- dashboard deployment to cloud


## Why This Project Matters

This project is not just a dashboard or a synthetic dataset exercise.

It is designed as a realistic simulation of how data systems can support global education programs, especially those that require:

- operational coordination
- standardized metrics
- impact reporting
- leadership decision support
- equitable and scalable learner experiences

## Author

Snehil Sanyal

If you’d like to connect, collaborate, or discuss analytics / AI / education systems, feel free to reach out.


**requirements.txt**
```txt
pandas
numpy
faker
matplotlib
plotly
streamlit
jupyter
```