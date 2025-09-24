import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
STUDENTS_CSV = BASE_DIR / "students.csv"
DELETED_CSV = BASE_DIR / "students_deleted.csv"
IMPORT_ERRORS_CSV = BASE_DIR / "import_errors.csv"
AUDIT_LOG = BASE_DIR / "audit.log"

HEADERS = [
    "Roll_No","Name","Branch","Year","Gender","Age",
    "Attendance_%","Mid1_Marks","Mid2_Marks","Quiz_Marks","Final_Marks"
]

def ensure_csv(path=STUDENTS_CSV):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()

def read_students():
    ensure_csv(STUDENTS_CSV)
    with STUDENTS_CSV.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_students(rows):
    with STUDENTS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

def append_student(row, path=STUDENTS_CSV):
    ensure_csv(path)
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(row)

def archive_deleted(row):
    ensure_csv(DELETED_CSV)
    with DELETED_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(row)

def log(action: str):
    ts = datetime.now().isoformat()
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(f"{ts} | {action}\n")
