from data import read_students, write_students, log, HEADERS
from datetime import datetime
import csv
from pathlib import Path

# ---- Helpers merged ----
def to_float_safe(value):
    try:
        return float(str(value).strip())
    except Exception:
        return None

def grade_from_score(score):
    s = to_float_safe(score)
    if s is None: return "N/A"
    if s >= 80: return "A"
    if s >= 60: return "B"
    if s >= 40: return "C"
    return "D"

def validate_student_row(row: dict):
    try:
        if row["Attendance_%"]:
            att = to_float_safe(row["Attendance_%"])
            if att is None or not (0 <= att <= 100):
                return False, "Attendance_% must be 0–100"
        if row["Final_Marks"]:
            fm = to_float_safe(row["Final_Marks"])
            if fm is None or not (0 <= fm <= 100):
                return False, "Final_Marks must be 0–100"
        return True, ""
    except:
        return False, "Validation failed"

# ---- Teacher Functions ----
def search_student_interactive():
    q = input("\nSearch Roll_No or partial Name: ").strip().lower()
    students = read_students()
    matches = [s for s in students if s["Roll_No"] == q or q in s["Name"].lower()]
    if not matches: print("No results."); return
    for s in matches:
        print("-"*20)
        for h in HEADERS:
            print(f"{h}: {s[h]}")

def update_student_interactive():
    roll = input("\nEnter Roll_No to update: ").strip()
    students = read_students()
    for s in students:
        if s["Roll_No"] == roll:
            s["Attendance_%"] = input(f"Attendance_% [{s['Attendance_%']}]: ") or s["Attendance_%"]
            s["Final_Marks"] = input(f"Final_Marks [{s['Final_Marks']}]: ") or s["Final_Marks"]
            ok,msg = validate_student_row(s)
            if not ok: print("❌", msg); return
            write_students(students)
            log(f"TEACHER_UPDATE Roll:{roll}")
            print("✅ Updated.")
            return
    print("❌ Roll not found.")

def teacher_report_interactive():
    students = read_students()
    finals = [to_float_safe(s["Final_Marks"]) for s in students if to_float_safe(s["Final_Marks"]) is not None]
    if not finals: print("No marks data."); return
    print("Total:", len(students))
    print("Average Final Marks:", sum(finals)/len(finals))
    print("Top:", max(finals), "Bottom:", min(finals))
    dist = {}
    for s in students:
        g = grade_from_score(s["Final_Marks"])
        dist[g] = dist.get(g,0)+1
    print("Grade distribution:", dist)
    if input("Export report? [y/N]: ").lower()=="y":
        fname = Path(f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
        with fname.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=HEADERS); w.writeheader(); w.writerows(students)
        print("Saved", fname)

def teacher_menu():
    while True:
        print("\nTeacher Menu: 1) Search  2) Update  3) Report  4) Back")
        c=input("Choice: ")
        if c=="1": search_student_interactive()
        elif c=="2": update_student_interactive()
        elif c=="3": teacher_report_interactive()
        elif c=="4": break
        else: print("Invalid choice.")
