# ================================
# COMPLETE DATA GENERATION SCRIPT
# ================================

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

# ------------------------
# CONFIG
# ------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker()

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

# ------------------------
# CONSTANTS
# ------------------------
PROGRAM_NAMES = [
    "Computational Neuroscience",
    "Deep Learning",
    "Computational Tools for Climate Science",
    "NeuroAI"
]

COUNTRIES = ["India","USA","Brazil","Germany","Kenya","UK","Canada","Japan"]

TIMEZONE_MAP = {
    "India":"UTC+5:30","USA":"UTC-5","Brazil":"UTC-3","Germany":"UTC+1",
    "Kenya":"UTC+3","UK":"UTC+0","Canada":"UTC-5","Japan":"UTC+9"
}

LANGUAGES = ["English","Spanish","French","Hindi"]
SLOTS = ["Slot 1","Slot 2","Slot 3","Slot 4","Slot 5"]
INTERESTS = ["Neural Coding","CV","NLP","RL","Climate","Time Series"]

# ------------------------
# HELPERS
# ------------------------
def clamp(x,a,b): return max(a,min(b,x))

# ================================
# PHASE 1
# ================================

def generate_programs():
    rows=[]
    pid=1
    for year in [2025,2026]:
        for name in PROGRAM_NAMES:
            rows.append({
                "program_id":f"P{pid:03d}",
                "program_name":name,
                "year":year,
                "start_date":datetime(year,6,22).date(),
                "end_date":datetime(year,7,24).date(),
                "num_students":random.randint(200,400),
                "num_tas":random.randint(15,30),
                "region_focus":"global",
                "curriculum_hours_per_day":4.5,
                "project_hours_per_day":3,
                "total_hours_per_day":8,
                "days_per_week":5,
                "delivery_mode":"virtual",
                "num_timeslots":5
            })
            pid+=1
    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/programs.csv",index=False)
    return df


def generate_users():
    rows=[]
    uid=1

    for _ in range(1500):
        role=np.random.choice(["student","ta","instructor"],p=[0.85,0.1,0.05])
        country=random.choice(COUNTRIES)

        rows.append({
            "user_id":f"U{uid:05d}",
            "role":role,
            "country":country,
            "timezone":TIMEZONE_MAP[country],
            "gender":random.choice(["Male","Female","Non-binary"]),
            "education_level":random.choice(["UG","Masters","PhD"]),
            "field_of_study":random.choice(["CS","AI","Neuro","Climate"]),
            "years_experience":np.random.randint(0,10),
            "prior_neuromatch":np.random.choice([0,1],p=[0.8,0.2]),
            "preferred_language":random.choice(LANGUAGES),
            "interest_area":random.choice(INTERESTS),
            "availability_slot":random.choice(SLOTS)
        })
        uid+=1

    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/users.csv",index=False)
    return df


def generate_applications(programs,users):
    rows=[]
    aid=1

    students=users[users.role=="student"]

    for _,u in students.iterrows():
        program=programs.sample(1).iloc[0]

        tech=clamp(50+u.years_experience*5+np.random.normal(0,10),20,100)
        mot=clamp(60+np.random.normal(0,10),20,100)
        cv=clamp(50+np.random.normal(0,10),20,100)

        score=(tech+mot+cv)/3
        selected=int(score>65)

        rows.append({
            "application_id":f"A{aid:06d}",
            "user_id":u.user_id,
            "program_id":program.program_id,
            "application_date":datetime(2026,3,1).date(),
            "motivation_score":mot,
            "cv_score":cv,
            "technical_score":tech,
            "diversity_score":random.randint(40,90),
            "preferred_program_track":"Research",
            "preferred_timeslot":u.availability_slot,
            "selected":selected,
            "waitlisted":0 if selected else 1,
            "final_status":"accepted" if selected else "rejected"
        })
        aid+=1

    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/applications.csv",index=False)
    return df

# ================================
# PHASE 2 (Pods + TA)
# ================================

def generate_pods(programs,users,applications):
    rows=[]
    pod_id=1

    tas=users[users.role=="ta"]

    for pid in programs.program_id:
        accepted=applications[(applications.program_id==pid) & (applications.selected==1)]

        students=list(accepted.user_id)
        random.shuffle(students)

        pods=[students[i:i+15] for i in range(0,len(students),15)]

        for pod in pods:
            ta=tas.sample(1).iloc[0]

            rows.append({
                "pod_id":f"PD{pod_id:04d}",
                "program_id":pid,
                "year":2026,
                "regular_ta_user_id":ta.user_id,
                "timeslot":random.choice(SLOTS),
                "language":random.choice(LANGUAGES),
                "interest_cluster":random.choice(INTERESTS),
                "num_students":len(pod),
                "region_mix_score":round(np.random.uniform(0.4,1),2)
            })
            pod_id+=1

    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/pods.csv",index=False)
    return df


def generate_project_groups(pods,users):
    rows=[]
    gid=1
    tas=users[users.role=="ta"]

    for _,pod in pods.iterrows():
        for _ in range(2):
            ta=tas.sample(1).iloc[0]
            rows.append({
                "project_group_id":f"G{gid:05d}",
                "pod_id":pod.pod_id,
                "program_id":pod.program_id,
                "project_ta_user_id":ta.user_id,
                "group_topic":random.choice(INTERESTS),
                "num_students":random.randint(5,8)
            })
            gid+=1

    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/project_groups.csv",index=False)
    return df


def generate_ta_assignments(pods,groups):
    rows=[]
    for _,p in pods.iterrows():
        rows.append({
            "user_id":p.regular_ta_user_id,
            "program_id":p.program_id,
            "pod_id":p.pod_id,
            "project_group_id":"",
            "ta_role":"regular_ta"
        })
    for _,g in groups.iterrows():
        rows.append({
            "user_id":g.project_ta_user_id,
            "program_id":g.program_id,
            "pod_id":g.pod_id,
            "project_group_id":g.project_group_id,
            "ta_role":"project_ta"
        })

    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/ta_assignments.csv",index=False)
    return df

# ================================
# PHASE 3 (Engagement + Surveys)
# ================================

def generate_daily_engagement(apps):
    rows=[]
    for _,a in apps.iterrows():
        if a.selected==0: continue

        for day in range(1,21):
            attend=np.random.choice([0,1],p=[0.2,0.8])

            rows.append({
                "user_id":a.user_id,
                "program_id":a.program_id,
                "day":day,
                "attended_curriculum":attend,
                "attended_project":attend,
                "curriculum_hours_attended":round(np.random.uniform(2,4.5),2),
                "project_hours_attended":round(np.random.uniform(1,3),2),
                "zoom_minutes":random.randint(60,300),
                "assignments_completed":attend,
                "forum_messages":random.randint(0,10),
                "help_requests":random.randint(0,3)
            })

    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/daily_engagement.csv",index=False)
    return df


def generate_assessments(apps):
    rows=[]
    aid=1
    for _,a in apps.iterrows():
        if a.selected==0: continue

        pre=random.randint(40,70)
        post=pre+random.randint(5,30)

        rows.append({"assessment_id":f"AS{aid:05d}","user_id":a.user_id,"program_id":a.program_id,"type":"pre","score":pre,"date":datetime(2026,6,22)})
        aid+=1
        rows.append({"assessment_id":f"AS{aid:05d}","user_id":a.user_id,"program_id":a.program_id,"type":"post","score":post,"date":datetime(2026,7,24)})
        aid+=1

    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/assessments.csv",index=False)
    return df


def generate_surveys(apps):
    rows=[]
    sid=1
    for _,a in apps.iterrows():
        if a.selected==0: continue

        rows.append({
            "survey_id":f"S{sid:05d}",
            "user_id":a.user_id,
            "program_id":a.program_id,
            "survey_type":"post",
            "satisfaction":random.randint(3,5),
            "difficulty":random.randint(2,5),
            "content_quality":random.randint(3,5),
            "ta_support":random.randint(3,5),
            "open_feedback":fake.sentence(),
            "response_date":datetime(2026,7,24)
        })
        sid+=1

    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/surveys.csv",index=False)
    return df

# ================================
# PHASE 4 (Ops + Metrics)
# ================================

def generate_dropouts(apps):
    rows=[]
    for _,a in apps.iterrows():
        if a.selected==1 and np.random.rand()<0.1:
            rows.append({
                "user_id":a.user_id,
                "program_id":a.program_id,
                "dropout_day":random.randint(1,20),
                "reason":random.choice(["low_engagement","time_constraint","difficulty"])
            })
    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/dropouts.csv",index=False)
    return df


def generate_support_requests(users,programs):
    rows=[]
    for i in range(300):
        u=users.sample(1).iloc[0]
        p=programs.sample(1).iloc[0]

        rows.append({
            "ticket_id":f"T{i:05d}",
            "user_id":u.user_id,
            "program_id":p.program_id,
            "channel":random.choice(["discord","email"]),
            "issue_type":random.choice(["technical","academic","admin"]),
            "response_time_hours":round(np.random.uniform(1,24),2),
            "resolved":1,
            "satisfaction":random.randint(3,5)
        })

    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/support_requests.csv",index=False)
    return df


def generate_ta_feedback(assignments):
    rows=[]
    for _,a in assignments.iterrows():
        rows.append({
            "user_id":a.user_id,
            "program_id":a.program_id,
            "ta_role":a.ta_role,
            "avg_student_rating":round(np.random.uniform(3,5),2),
            "num_sessions_taken":random.randint(5,20),
            "response_time_avg":round(np.random.uniform(1,10),2),
            "engagement_score":round(np.random.uniform(0.5,1),2)
        })
    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/ta_feedback.csv",index=False)
    return df


def generate_pod_checkins(pods):
    rows=[]
    cid=1
    for _,p in pods.iterrows():
        for day in range(1,21):
            rows.append({
                "checkin_id":f"C{cid:05d}",
                "pod_id":p.pod_id,
                "program_id":p.program_id,
                "day":day,
                "completed":1,
                "issues_reported":random.randint(0,3),
                "mood_score":random.randint(2,5)
            })
            cid+=1
    df=pd.DataFrame(rows)
    df.to_csv(f"{DATA_DIR}/pod_checkins.csv",index=False)
    return df

# ================================
# MAIN
# ================================

def main():
    programs=generate_programs()
    users=generate_users()
    apps=generate_applications(programs,users)

    pods=generate_pods(programs,users,apps)
    groups=generate_project_groups(pods,users)
    ta_assign=generate_ta_assignments(pods,groups)

    generate_daily_engagement(apps)
    generate_assessments(apps)
    generate_surveys(apps)

    generate_dropouts(apps)
    generate_support_requests(users,programs)
    generate_ta_feedback(ta_assign)
    generate_pod_checkins(pods)

    print("ALL DATA GENERATED SUCCESSFULLY")

if __name__ == "__main__":
    main()