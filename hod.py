from data import read_students, append_student, log, HEADERS, IMPORT_ERRORS_CSV
import csv
from pathlib import Path

# ---- Helpers merged ----
def to_float_safe(value):
    try:
        return float(str(value).strip())
    except Exception:
        return None

def validate_student_row(row: dict):
    try:
        if row["Roll_No"] and not row["Roll_No"].isdigit():
            return False, "Roll_No must be int"
        if row["Final_Marks"]:
            fm = to_float_safe(row["Final_Marks"])
            if fm is None or not (0 <= fm <= 100):
                return False,"Final_Marks must be 0–100"
        return True,""
    except:
        return False,"Validation failed"

# ---- HOD Functions ----
def hod_summary_interactive():
    students = read_students()
    if not students: print("No data."); return
    branch_map={}
    for s in students:
        b=s["Branch"]
        m=to_float_safe(s["Final_Marks"]) or 0
        branch_map.setdefault(b,[]).append(m)
    for b,marks in branch_map.items():
        avg=sum(marks)/len(marks)
        print(f"Branch {b}: Students={len(marks)} Avg={avg:.2f}")

def bulk_import_interactive():
    path=input("CSV file path: ").strip()
    p=Path(path)
    if not p.exists(): print("File not found."); return
    students=read_students(); existing={s["Roll_No"] for s in students}
    added,errors=0,[]
    with p.open("r",newline="",encoding="utf-8") as f:
        r=csv.DictReader(f)
        for row in r:
            for h in HEADERS: row.setdefault(h,"")
            ok,msg=validate_student_row(row)
            if not ok: errors.append(msg); continue
            if row["Roll_No"] in existing: errors.append("duplicate"); continue
            append_student(row); existing.add(row["Roll_No"]); added+=1
    print(f"Added {added}, Errors {len(errors)}")
    log(f"HOD_IMPORT added={added} errors={len(errors)}")

def hod_menu():
    while True:
        print("\nHOD Menu: 1) Summary  2) Bulk Import  3) Back")
        c=input("Choice: ")
        if c=="1": hod_summary_interactive()
        elif c=="2": bulk_import_interactive()
        elif c=="3": break
        else: print("Invalid choice.")
