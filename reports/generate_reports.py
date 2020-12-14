import sys
import re
from datetime import date, timedelta

TEAM_MEMBERS = [
    "jordan",
    "jacob",
    "bernard",
    "robert",
    "abdullah",
]

with open("individual_template.md") as template_file:
    template = template_file.read()

DATE_FORMAT = "%B %d, %Y"
FILE_NAME_FORMAT = "%m-%d-%Y"
ONE_WEEK = timedelta(days=7)

END_OF_SEMESTER = date(month=12, day=15, year=2020)


def new_report(report_date):
    for member in TEAM_MEMBERS:
        with open(
            f"{member}/{report_date.strftime(FILE_NAME_FORMAT)}.md", "w"
        ) as report_file:
            data = template.format(date=report_date.strftime(DATE_FORMAT))
            report_file.write(data)


def generate_new_reports(start=date.today(), end=END_OF_SEMESTER, step=ONE_WEEK):
    report_date = start
    while report_date <= end:
        new_report(report_date)
        report_date += step


SUB_TITLE = re.compile(r"#{2,}(.+)")
LIST_ITEM = re.compile(r"\*.+")


def parse_text(data):
    items = {}

    for line in data:
        match = re.match(SUB_TITLE, line)
        if match:
            current_heading = match.group(1).strip()
            items[current_heading] = []
            continue

        match = re.match(LIST_ITEM, line)
        if match:
            items[current_heading].append(line)

    return items


def generate_team_report(report_date):
    data = {}
    for member in TEAM_MEMBERS:
        file_name = f"{member}/{report_date.strftime(FILE_NAME_FORMAT)}.md"
        with open(file_name, "r") as individual_report:
            data[member] = parse_text(individual_report.readlines())

    team_report = []
    for line in template.split("\n"):
        section_heading = re.match(SUB_TITLE, line)
        if "{date}" in line:
            team_report.append(line.format(date=report_date.strftime(DATE_FORMAT)))
        elif section_heading:
            team_report.append(line)
            for member, sections in data.items():
                team_report.append(f"* {member.capitalize()}")
                for item in sections[section_heading.group(1).strip()]:
                    team_report.append(f"    {item}")

    with open(f"team/{report_date.strftime(FILE_NAME_FORMAT)}.md", "w") as report_file:
        print("\n".join(team_report), file=report_file)

        print("## Meeting Agenda", file=report_file)
        print("* ", file=report_file)


if __name__ == "__main__":
    try:
        offset = sys.argv[1]
    except IndexError:
        offset = 0

    generate_team_report(date.today() - timedelta(days=int(offset)))