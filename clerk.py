from data import read_students, append_student, write_students, archive_deleted, log, HEADERS
from utils import validate_student_row




def _prompt_full_row():
row = {}
print("(fill fields; leave optional fields blank)")
for h in HEADERS:
row[h] = input(f"{h}: ").strip()
return row




def add_student_interactive():
print("\n--- Add student (Clerk) ---")
row = _prompt_full_row()
ok, msg = validate_student_row(row)
if not ok:
print("❌", msg)
return
students = read_students()
if any(s["Roll_No"].strip() == row["Roll_No"].strip() for s in students):
print("❌ Duplicate Roll_No. Aborting.")
return
append_student(row)
log(f"CLERK_ADD Roll:{row['Roll_No']} Name:{row.get('Name','')}")
print("✅ Student added.")




def delete_student_interactive():
print("\n--- Delete student (Clerk) ---")
roll = input("Enter Roll_No to delete: ").strip()
students = read_students()
for i, s in enumerate(students):
if s["Roll_No"].strip() == roll:
print("Found:")
for h in HEADERS:
print(f"{h}: {s.get(h,'')}")
if input("Confirm delete? [y/N]: ").strip().lower() == "y":
archive_deleted(s)
students.pop(i)
write_students(students)
log(f"CLERK_DELETE Roll:{roll}")
print("✅ Deleted and archived.")
else:
print("Cancelled.")
return
print("❌ Roll_No not found.")




def clerk_menu():
while True:
print("\nClerk Menu: 1) Add 2) Delete 3) Back")
c = input("Choice: ").strip()
if c == "1":
add_student_interactive()
elif c == "2":
delete_student_interactive()
elif c == "3":
break
else:
print("Invalid choice.")