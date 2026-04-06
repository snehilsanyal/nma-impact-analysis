# Schema for database

1. `programs.csv:` program_id (Primary Key), program_name (Comp Neuro / Deep Learning / Climate / NeuroAI), year, start_date, end_date, num_students, num_tas, region_focus (global / region-specific), curriculum_hours_per_day, project_hours_per_day, total_hours_per_day, days_per_week, delivery_mode (virtual), num_timeslots.
We can get the following metrics from the csv: Program-level metadata, course structure, reporting summaries, and yearly comparisons.
2. `users.csv:` user_id (Primary Key), role (student / ta / instructor), country, timezone, gender (optional feature), education_level, field_of_study, years_experience, prior_neuromatch (0/1), preferred_language, interest_area, availability_slot.
We can get the following metrics from the csv: Diversity metrics, cohort analysis, participant demographics, and matching features for pod formation.
3. `applications.csv:` application_id (Primary Key), user_id (Foreign Key -> users.csv), program_id (Foreign Key -> programs.csv), application_date, motivation_score (simulated NLP score), cv_score, technical_score, diversity_score, preferred_program_track, preferred_timeslot, selected (0/1), waitlisted (0/1), final_status (accepted / rejected / no-show).
We can get the following metrics from the csv: Selection rate, applicant quality, admissions funnel, and applicant-program fit.
4. `pods.csv:` pod_id (Primary Key), program_id (Foreign Key -> programs.csv), year, regular_ta_user_id (Foreign Key -> users.csv), timeslot, language, interest_cluster, num_students, region_mix_score (diversity inside pod).
We can get the following metrics from the csv: Pod-level diversity, TA allocation, timeslot distribution, and group structure analysis.
5.`project_groups.csv:` project_group_id (Primary Key), pod_id (Foreign Key -> pods.csv), program_id (Foreign Key -> programs.csv), project_ta_user_id (Foreign Key -> users.csv), group_topic, num_students.
We can get the following metrics from the csv: Project grouping structure, project topic distribution, and project TA allocation.
6. `ta_assignments.csv:` user_id (Foreign Key -> users.csv), program_id (Foreign Key -> programs.csv), pod_id (Foreign Key -> pods.csv), project_group_id (Foreign Key -> project_groups.csv), ta_role (regular_ta / project_ta).
Composite identity can be treated as: user_id + program_id + pod_id + project_group_id + ta_role.
We can get the following metrics from the csv: TA deployment, TA role distribution, and workload mapping.
7. `daily_engagement.csv` (Core Table): user_id (Foreign Key -> users.csv), program_id (Foreign Key -> programs.csv), day, attended_curriculum (0/1), attended_project (0/1), curriculum_hours_attended, project_hours_attended, zoom_minutes, assignments_completed (0/1), forum_messages, help_requests.
Composite identity can be treated as: user_id + program_id + day.
We can get the following metrics from the csv: Attendance, engagement, participation trends, curriculum vs project involvement, and risk of dropout.
8. `assessments.csv:` assessment_id (Primary Key), user_id (Foreign Key -> users.csv), program_id (Foreign Key -> programs.csv), type (pre / mid / post), score, date.
We can get the following metrics from the csv: Learning gain, performance tracking, and academic progress.
9. `surveys.csv:` survey_id (Primary Key), user_id (Foreign Key -> users.csv), program_id (Foreign Key -> programs.csv), survey_type (pre / mid / post), satisfaction (1–5), difficulty (1–5), content_quality (1–5), ta_support (1–5), open_feedback (text), response_date.
We can get the following metrics from the csv: Student experience, satisfaction analysis, perceived difficulty, TA support quality, and qualitative feedback trends.
10. `dropouts.csv:` user_id (Foreign Key -> users.csv), program_id (Foreign Key -> programs.csv), dropout_day, reason (low_engagement / time_constraint / difficulty).
Composite identity can be treated as: user_id + program_id.
We can get the following metrics from the csv: Dropout timing, dropout causes, and retention risk patterns.
11. `support_requests.csv:` ticket_id (Primary Key), user_id (Foreign Key -> users.csv), program_id (Foreign Key -> programs.csv), channel (discord / email), issue_type (technical / academic / admin), response_time_hours, resolved (0/1), satisfaction (1–5).
We can get the following metrics from the csv: Support load, issue distribution, response efficiency, and support satisfaction.
12. `ta_feedback.csv:` user_id (Foreign Key -> users.csv (TA)), program_id (Foreign Key -> programs.csv), ta_role (regular_ta / project_ta), avg_student_rating, num_sessions_taken, response_time_avg, engagement_score.
Composite identity can be treated as: user_id + program_id + ta_role.
We can get the following metrics from the csv: TA effectiveness, responsiveness, session load, and student-rated TA quality.
13. `pod_checkins.csv:` checkin_id (Primary Key), pod_id (Foreign Key -> pods.csv), program_id (Foreign Key -> programs.csv), day, completed (0/1), issues_reported, mood_score.
We can get the following metrics from the csv: Pod health, operational check-ins, issue escalation, and pod morale trends.
14. `program_metrics.csv:` program_id (Foreign Key -> programs.csv), year, completion_rate, avg_learning_gain, avg_satisfaction, dropout_rate, engagement_score.
Composite identity can be treated as: program_id + year.
We can get the following metrics from the csv: Final program-level KPIs and impact reporting summaries.


                                ┌────────────────────┐
                                │    programs.csv    │
                                │  program_id (PK)   │
                                └─────────┬──────────┘
                                          │
                                          │
                     ┌────────────────────┼────────────────────┐
                     │                    │                    │
                     │                    │                    │
          ┌──────────▼──────────┐  ┌──────▼───────┐  ┌────────▼────────┐
          │   applications.csv  │  │   pods.csv   │  │ program_metrics │
          │ application_id (PK) │  │  pod_id (PK) │  │ program_id (FK) │
          │ user_id (FK)        │  │ program_id   │  │ year            │
          │ program_id (FK)     │  │ regular_ta   │  └─────────────────┘
          └──────────┬──────────┘  └──────┬───────┘
                     │                    │
                     │                    │
               ┌─────▼─────┐        ┌────▼──────────────┐
               │ users.csv │        │ project_groups.csv│
               │ user_id PK│        │ project_group_id  │
               │ role      │        │ pod_id (FK)       │
               └─────┬─────┘        │ program_id (FK)   │
                     │              │ project_ta_user_id│
                     │              └────┬──────────────┘
                     │                   │
     ┌───────────────┼───────────────────┼───────────────────────────────┐
     │               │                   │                               │
     │               │                   │                               │
┌────▼────────┐ ┌────▼─────────┐ ┌──────▼─────────┐             ┌───────▼─────────┐
│daily_engage │ │ assessments  │ │   surveys.csv  │             │ ta_assignments   │
│ user_id (FK)│ │ assess_id PK │ │ survey_id (PK) │             │ user_id (FK)     │
│ program_id  │ │ user_id (FK) │ │ user_id (FK)   │             │ program_id (FK)  │
│ day         │ │ program_id   │ │ program_id (FK)│             │ pod_id (FK)      │
└────┬────────┘ └──────────────┘ └───────────────┘             │ project_group_id  │
     │                                                          │ ta_role           │
     │                                                          └────────┬──────────┘
┌────▼────────┐                                                       │
│ dropouts.csv│                                                       │
│ user_id (FK)│                                                       │
│ program_id  │                                                       │
└─────────────┘                                                       │
                                                                      │
                     ┌───────────────────────┐                        │
                     │ support_requests.csv  │                        │
                     │ ticket_id (PK)        │                        │
                     │ user_id (FK)          │                        │
                     │ program_id (FK)       │                        │
                     └───────────────────────┘                        │
                                                                      │
                     ┌───────────────────────┐                        │
                     │   ta_feedback.csv     │◄───────────────────────┘
                     │ user_id (FK, TA)      │
                     │ program_id (FK)       │
                     └───────────────────────┘

                     ┌───────────────────────┐
                     │   pod_checkins.csv    │
                     │ checkin_id (PK)       │
                     │ pod_id (FK)           │
                     │ program_id (FK)       │
                     └───────────────────────┘