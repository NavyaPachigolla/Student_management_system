from data import HEADERS


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


def validate_student_row(row: dict) -> (bool, str):
"""Return (True, '') when valid, otherwise (False, 'reason').
Validates Roll_No int, Attendance_% and marks in 0-100 when present.
"""
r = to_int_safe(row.get("Roll_No", ""))
if r is None:
return False, "Roll_No must be an integer"


att = str(row.get("Attendance_%", "")).strip()
if att:
a = to_float_safe(att)
if a is None or not (0 <= a <= 100):
return False, "Attendance_% must be a number between 0 and 100"


for m in ("Mid1_Marks", "Mid2_Marks", "Quiz_Marks", "Final_Marks"):
mv = str(row.get(m, "")).strip()
if mv:
mm = to_float_safe(mv)
if mm is None or not (0 <= mm <= 100):
return False, f"{m} must be number 0-100"


return True, ""


def grade_from_score(score):
s = to_float_safe(score)
if s is None:
return "N/A"
if s >= 80:
return "A"
if s >= 60:
return "B"
if s >= 40:
return "C"
return "D"