import pandas as pd
import numpy as np

SUBJECTS=["Python", "SQL", "HTML", "CSS", "JavaScript"]


def load_dataset(filename="students.csv"):
    df = pd.read_csv(filename)

    required_cols = ["Student_ID", "Name"] + SUBJECTS + ["Attendance"]

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    if df.empty:
        raise ValueError("The CSV file contains no student records.")

    if df[required_cols].isnull().any().any():
        raise ValueError("The dataset contains missing values.")

    marks = df[SUBJECTS + ["Attendance"]]
    if not marks.apply(lambda col: col.between(0, 100)).all().all():
        raise ValueError("Marks and attendance must be between 0 and 100.")

    return df

def calculate_totals_and_averages(df):
    marks_matrix=df[SUBJECTS].to_numpy()
    df["Total"]=np.sum(marks_matrix, axis=1)
    df["Average"]=np.round(np.mean(marks_matrix, axis=1), 2)
    return df

def assign_grades(df):
    grades=[]
    for avg in df["Average"]:
        if avg>=90:
            grades.append("A+")
        elif avg>=80:
            grades.append("A")
        elif avg>=70:
            grades.append("B")
        elif avg>=60:
            grades.append("C")
        elif avg>=50:
            grades.append("D")
        else:
            grades.append("F")

    df["Grade"]=grades
    return df

def evaluate_results(df, pass_mark=40, min_attendance=75):
    result=[]
    for _, row in df.iterrows():
        marks=[row[sub] for sub in SUBJECTS]
        attendance=row["Attendance"]

        if min(marks)>=pass_mark and attendance>= min_attendance:
            result.append("Pass")
        else:
            result.append("Fail")

    df["Result"]=result
    return df

def get_subject_analysis(df):
    summary={}
    for subject in SUBJECTS:
        scores=df[subject].to_numpy()
        summary[subject]={
            "Average": round(float(np.mean(scores)), 2),
            "Highest": int(np.max(scores)),
            "Lowest": int(np.min(scores))
        }

    return pd.DataFrame(summary).T