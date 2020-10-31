import os
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

report_date = date(month=11, day=1, year=2020)
while report_date <= END_OF_SEMESTER:
    for member in TEAM_MEMBERS:
        with open(
            f"{member}/{report_date.strftime(FILE_NAME_FORMAT)}.md", "w"
        ) as report_file:
            data = template.format(date=report_date.strftime(DATE_FORMAT))
            report_file.write(data)
            # print(data)

    report_date += ONE_WEEK