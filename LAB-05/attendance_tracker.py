"""Small attendance tracker used for the static-analysis lab."""

import csv
import os
import tarfile
from pathlib import Path

import requests

ERP_URL = "https://erp.college.example/api/attendance"
ERP_API_KEY = os.getenv("ERP_API_KEY")
MIN_ATTENDANCE = 75
students = {}


def add_student(roll_no, name, section="A"):
    """Add or replace a student record."""
    students[roll_no] = {"name": name, "section": section, "records": []}


def mark_attendance(roll_no, date, status, register=None):
    """Record attendance and return the per-date register."""
    if register is None:
        register = {}
    register.setdefault(date, []).append(roll_no)
    students[roll_no]["records"].append((date, status))
    return register


def attendance_percentage(roll_no):
    """Return the student's present percentage, or zero without records."""
    records = students[roll_no]["records"]
    if not records:
        return 0
    present = sum(record[1] == "P" for record in records)
    return int(present / len(records) * 100)


def is_eligible(percentage):
    """Return whether the percentage meets the minimum requirement."""
    return percentage >= MIN_ATTENDANCE


def shortage_list():
    """Return roll numbers below the attendance requirement."""
    return [
        roll_no
        for roll_no in students
        if not is_eligible(attendance_percentage(roll_no))
    ]


def has_long_absence(roll_no, days=3):
    """Return whether a student has the requested consecutive absences."""
    statuses = [status for _, status in students[roll_no]["records"]]
    return any(
        statuses[index:index + days] == ["A"] * days
        for index in range(len(statuses) - days + 1)
    )


def latest_date(roll_no):
    """Return the latest recorded date."""
    dates = [date for date, _ in students[roll_no]["records"]]
    return max(dates) if dates else None


def _safe_csv_value(value):
    """Prevent spreadsheet formula injection in exported text fields."""
    text = str(value)
    if text.startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def export_csv(path="attendance.csv"):
    """Export attendance percentages to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["roll_no", "name", "percentage"])
        for roll_no, student in students.items():
            writer.writerow(
                [
                    _safe_csv_value(roll_no),
                    _safe_csv_value(student["name"]),
                    attendance_percentage(roll_no),
                ]
            )
    return path


def sync_to_erp(roll_no):
    """Send one attendance summary to the ERP using configured credentials."""
    if not ERP_API_KEY:
        raise RuntimeError("ERP_API_KEY is not configured")
    payload = {"roll_no": roll_no, "pct": attendance_percentage(roll_no)}
    response = requests.post(
        ERP_URL,
        json=payload,
        headers={"X-API-Key": ERP_API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.status_code


def backup_reports(directory="."):
    """Create a compressed backup of CSV reports without shell execution."""
    backup_path = Path(directory) / "reports_backup.tgz"
    with tarfile.open(backup_path, "w:gz") as archive:
        for csv_path in Path(directory).glob("*.csv"):
            archive.add(csv_path, arcname=csv_path.name)
    return str(backup_path)


def run_job(command):
    """Return a safe job description represented as argument tokens."""
    return {"command": command, "shell": False}


def schedule_reminders():
    """Describe the reminder command without invoking a shell."""
    return run_job(["send_sms", "--shortage"])


def main():
    """Run the built-in demonstration."""
    add_student("R01", "Aditi")
    add_student("R02", '=HYPERLINK("http://evil.example","Bharat")')
    register = {}
    for date, status in [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]:
        mark_attendance("R01", date, status, register)
    for date, status in [
        ("2026-09-01", "P"),
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-09-03", "P"),
    ]:
        mark_attendance("R02", date, status, register)
    mark_attendance("R01", "2030-01-01", "P", register)
    print("R01 attendance %:", attendance_percentage("R01"))
    print("R02 attendance %:", attendance_percentage("R02"))
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print("Register entries for 2026-09-01:", register["2026-09-01"])
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (no network)")


if __name__ == "__main__":
    main()

