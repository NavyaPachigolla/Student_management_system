from data import read_students, append_student, write_students, archive_deleted, log, HEADERS

# ---- Helper Functions (moved from utils.py) ----
def to_int_safe(value):
    try:
        return int(str(value).strip())
    except Exception:
        return None

def to_float_safe(value):
    try:
        return float(str(value).strip())
    except Exception:
        return None

def validate_student_row(row: dict) -> (str):
    r = to_int_safe(row.get("Roll_No", ""))
    if r is None:
        return False, "Roll_No must be an integer"
    att = str(row.get("Attendance_%", "")).strip()
    if att:
        a = to_float_safe(att)
        if a is None or not (0 <= a <= 100):
            return False, "Attendance_% must be 0–100"
    for m in ("Mid1_Marks","Mid2_Marks","Quiz_Marks","Final_Marks"):
        mv = str(row.get(m, "")).strip()
        if mv:
            mm = to_float_safe(mv)
            if mm is None or not (0 <= mm <= 100):
                return False, f"{m} must be 0–100"
    return True, ""

# ---- Clerk Functions ----
def _prompt_full_row():
    row = {}
    for h in HEADERS:
        row[h] = input(f"{h}: ").strip()
    return row

def add_student_interactive():
    print("\n--- Add student (Clerk) ---")
    row = _prompt_full_row()
    ok, msg = validate_student_row(row)
    if not ok:
        print("wrong", msg); return
    students = read_students()
    if any(s["Roll_No"].strip() == row["Roll_No"].strip() for s in students):
        print("wrong Duplicate Roll_No."); return
    append_student(row)
    log(f"CLERK_ADD Roll:{row['Roll_No']}")
    print("right Student added.")

def delete_student_interactive():
    print("\n--- Delete student (Clerk) ---")
    roll = input("Enter Roll_No: ").strip()
    students = read_students()
    for i, s in enumerate(students):
        if s["Roll_No"].strip() == roll:
            print("Found:", s)
            if input("Delete? [y/N]: ").lower() == "y":
                archive_deleted(s)
                students.pop(i)
                write_students(students)
                log(f"CLERK_DELETE Roll:{roll}")
                print("right Deleted.")
            else:
                print("Cancelled.")
            return
    print("wrong Roll not found.")

def clerk_menu():
    while True:
        print("\nClerk Menu: 1) Add  2) Delete  3) Back")
        c = input("Choice: ").strip()
        if c == "1": add_student_interactive()
        elif c == "2": delete_student_interactive()
        elif c == "3": break
        else: print("Invalid entered")
