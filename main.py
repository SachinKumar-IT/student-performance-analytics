import pandas as pd
import numpy as np

from functions import(
    load_dataset,
    calculate_totals_and_averages,
    assign_grades,
    evaluate_results,
    get_subject_analysis,
    SUBJECTS
)

def main():
    print("STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("*******************************************")

    try:
        df=load_dataset("students.csv")
    except ValueError as e:
        print(f"Error loading dataset: {e}")
        return

    
    print("==========STUDENT DATA==========")
    data_cols = ["Student_ID", "Name"] + SUBJECTS + ["Attendance"]
    print(df[data_cols].to_string(index=False))
    print()

    df=calculate_totals_and_averages(df)
    df=assign_grades(df)
    df=evaluate_results(df)

    print("*************STUDENT PERFORMANCE***************\n")
    perf_cols=["Student_ID", "Name", "Total", "Average", "Grade", "Result"]
    display_df=df[perf_cols]
    print(display_df.to_string())
    print()

    print("***************SUBJECT ANALYSIS************\n")
    total_students=len(df)
    passed_count=len(df[df["Result"]=="Pass"])
    failed_count=len(df[df["Result"]=="Fail"])
    overall_avg=np.mean(df["Average"].to_numpy())

    print(f"Total Students Processed: {total_students}")
    print(f"Overall Class Average: {overall_avg:.2f}")
    print(f"Number Of Students Passed: {passed_count}")
    print(f"Number of Students Failed: {failed_count}\n")

    print("---------Subject-Wise Analysis-------")
    print(get_subject_analysis(df).to_string())
    print()

    print("--------Top 3 Performers--------")
    top_performers=df.sort_values(by="Total", ascending=False).head(3)
    print(top_performers[["Student_ID", "Name", "Total", "Average", "Grade"]].to_string(index=False))

if __name__ == "__main__":
    main()