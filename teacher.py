from data import read_students, write_students, log, HEADERS
from utils import to_float_safe, grade_from_score, validate_student_row
from datetime import datetime
import csv
from pathlib import Path




def search_student_interactive():
print("\n--- Search student (Teacher) ---")
q = input("Enter Roll_No or partial Name: ").strip().lower()
students = read_students()
matches = [s for s in students if s["Roll_No"].strip() == q or q in s["Name"].lower()]
if not matches:
print("No results.")
return
for s in matches:
print("-" * 30)
for h in HEADERS:
print(f"{h}: {s.get(h,'')}")
print("-" * 30)




def update_student_interactive():
print("\n--- Update student (Teacher) ---")
roll = input("Enter Roll_No to update: ").strip()
students = read_students()
for i, s in enumerate(students):
if s["Roll_No"].strip() == roll:
print("Current:")
for h in HEADERS:
print(f"{h}: {s.get(h,'')}")
new_att = input(f"Attendance_% [{s.get('Attendance_%','')}]: ").strip()
new_final = input(f"Final_Marks [{s.get('Final_Marks','')}]: ").strip()
old = {"Attendance_%": s.get('Attendance_%',''), "Final_Marks": s.get('Final_Marks','')}
if new_att:
s['Attendance_%'] = new_att
if new_final:
s['Final_Marks'] = new_final
ok, msg = validate_student_row(s)
if not ok:
print("Invalid update:", msg)
s['Attendance_%'] = old['Attendance_%']
s['Final_Marks'] = old['Final_Marks']
return
write_students(students)
log(f"TEACHER_UPDATE Roll:{roll}")
print("✅ Updated.")
return
print('Invalid choice.')