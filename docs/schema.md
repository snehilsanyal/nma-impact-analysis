# Dataset Schema Documentation

This document defines the **full schema**, including:

- table descriptions
- column definitions
- primary keys (PK)
- foreign keys (FK)
- relationships between tables

The schema is designed to simulate a realistic **Neuromatch Academy analytics system** covering:

- applications
- program participation
- pod-based learning structure
- engagement tracking
- assessments and surveys
- support operations
- program-level impact metrics

---

# 1. programs.csv

## Description
Stores metadata about each academy program across different years.

## Primary Key
- `program_id`

## Columns
- program_id (PK)
- program_name
- year
- start_date
- end_date
- num_students
- num_tas
- region_focus
- curriculum_hours_per_day
- project_hours_per_day
- total_hours_per_day
- days_per_week
- delivery_mode
- num_timeslots

---

# 2. users.csv

## Description
Stores all participants including students, TAs, and instructors.

## Primary Key
- `user_id`

## Columns
- user_id (PK)
- role (student / ta / instructor)
- country
- timezone
- gender
- education_level
- field_of_study
- years_experience
- prior_neuromatch (0/1)
- preferred_language
- interest_area
- availability_slot

---

# 3. applications.csv

## Description
Stores applications submitted by users to programs.

## Primary Key
- `application_id`

## Foreign Keys
- `user_id` → users.user_id
- `program_id` → programs.program_id

## Columns
- application_id (PK)
- user_id (FK)
- program_id (FK)
- application_date
- motivation_score
- cv_score
- technical_score
- diversity_score
- preferred_program_track
- preferred_timeslot
- selected (0/1)
- waitlisted (0/1)
- final_status (accepted / rejected / no-show)

---

# 4. pods.csv

## Description
Represents student learning pods (groups of ~15 students with a TA).

## Primary Key
- `pod_id`

## Foreign Keys
- `program_id` → programs.program_id
- `regular_ta_user_id` → users.user_id

## Columns
- pod_id (PK)
- program_id (FK)
- year
- regular_ta_user_id (FK)
- timeslot
- language
- interest_cluster
- num_students
- region_mix_score

---

# 5. project_groups.csv

## Description
Each pod is split into smaller project groups.

## Primary Key
- `project_group_id`

## Foreign Keys
- `pod_id` → pods.pod_id
- `program_id` → programs.program_id
- `project_ta_user_id` → users.user_id

## Columns
- project_group_id (PK)
- pod_id (FK)
- program_id (FK)
- project_ta_user_id (FK)
- group_topic
- num_students

---

# 6. ta_assignments.csv

## Description
Maps TAs to pods and project groups.

## Foreign Keys
- `user_id` → users.user_id
- `program_id` → programs.program_id
- `pod_id` → pods.pod_id
- `project_group_id` → project_groups.project_group_id

## Columns
- user_id (FK)
- program_id (FK)
- pod_id (FK)
- project_group_id (FK)
- ta_role (regular_ta / project_ta)

## Composite Identity
- user_id + program_id + pod_id + project_group_id + ta_role

---

# 7. daily_engagement.csv

## Description
Tracks daily participation and engagement of students.

## Foreign Keys
- `user_id` → users.user_id
- `program_id` → programs.program_id

## Columns
- user_id (FK)
- program_id (FK)
- day
- attended_curriculum (0/1)
- attended_project (0/1)
- curriculum_hours_attended
- project_hours_attended
- zoom_minutes
- assignments_completed (0/1)
- forum_messages
- help_requests

## Composite Identity
- user_id + program_id + day

---

# 8. assessments.csv

## Description
Stores assessment scores for students.

## Primary Key
- `assessment_id`

## Foreign Keys
- `user_id` → users.user_id
- `program_id` → programs.program_id

## Columns
- assessment_id (PK)
- user_id (FK)
- program_id (FK)
- type (pre / mid / post)
- score
- date

---

# 9. surveys.csv

## Description
Stores survey responses capturing student experience.

## Primary Key
- `survey_id`

## Foreign Keys
- `user_id` → users.user_id
- `program_id` → programs.program_id

## Columns
- survey_id (PK)
- user_id (FK)
- program_id (FK)
- survey_type (pre / mid / post)
- satisfaction (1–5)
- difficulty (1–5)
- content_quality (1–5)
- ta_support (1–5)
- open_feedback
- response_date

---

# 10. dropouts.csv

## Description
Tracks students who dropped out of a program.

## Foreign Keys
- `user_id` → users.user_id
- `program_id` → programs.program_id

## Columns
- user_id (FK)
- program_id (FK)
- dropout_day
- reason (low_engagement / time_constraint / difficulty)

## Composite Identity
- user_id + program_id

---

# 11. support_requests.csv

## Description
Tracks support tickets raised by users.

## Primary Key
- `ticket_id`

## Foreign Keys
- `user_id` → users.user_id
- `program_id` → programs.program_id

## Columns
- ticket_id (PK)
- user_id (FK)
- program_id (FK)
- channel (discord / email)
- issue_type (technical / academic / admin)
- response_time_hours
- resolved (0/1)
- satisfaction (1–5)

---

# 12. ta_feedback.csv

## Description
Stores aggregated TA performance metrics.

## Foreign Keys
- `user_id` → users.user_id (TA)
- `program_id` → programs.program_id

## Columns
- user_id (FK)
- program_id (FK)
- ta_role (regular_ta / project_ta)
- avg_student_rating
- num_sessions_taken
- response_time_avg
- engagement_score

## Composite Identity
- user_id + program_id + ta_role

---

# 13. pod_checkins.csv

## Description
Tracks daily pod-level check-ins and issues.

## Primary Key
- `checkin_id`

## Foreign Keys
- `pod_id` → pods.pod_id
- `program_id` → programs.program_id

## Columns
- checkin_id (PK)
- pod_id (FK)
- program_id (FK)
- day
- completed (0/1)
- issues_reported
- mood_score

---

# 14. program_metrics.csv (Derived Table)

## Description
Stores aggregated program-level KPIs used for impact reporting.

## Foreign Keys
- `program_id` → programs.program_id

## Columns
- program_id (FK)
- year
- completion_rate
- avg_learning_gain
- avg_satisfaction
- dropout_rate
- engagement_score

## Composite Identity
- program_id + year

---

# Relationship Overview

High-level flow:

```bash
users ─────┐
           ├── applications ──── programs
           │
           ├── daily_engagement
           ├── assessments
           ├── surveys
           ├── dropouts
           ├── support_requests
           └── ta_feedback

programs ─── pods ─── project_groups ─── ta_assignments
         │        │
         │        └── pod_checkins
         │
         └── program_metrics (derived)