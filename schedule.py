import json
import os
import datetime
from rich.table import Table
from rich.console import Console


class Schedule:
    """
    Schedule class for GUC Schedule
    """

    def __init__(self) -> None:
        self.schedule = {}
        self.schedule_file = "schedule.json"
        self.console = Console()
        self.load()
        self.courses_table = Table(
            show_header=True, header_style="bold magenta")
        self.courses_table.add_column("slot", style="bold magenta")
        self.courses_table.add_column("Course Type", style="bold magenta")
        self.courses_table.add_column("Course Name", style="bold magenta")
        self.courses_table.add_column("Location", style="bold magenta")
        self.courses_table.add_column("Staff", style="bold magenta")
        self.courses = self.get_today_schedule()
        if len(self.courses) == 0:
            self.console.print("[bold][red]No courses today[/red][/bold]")
        else:
            self.print_today_schedule()
            self.console.print(self.courses_table)

    def load(self) -> None:
        '''[summary]load json file into dict
        '''
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, "r") as f:
                self.schedule = json.load(f)['data']
        else:
            self.get_schedule()

    def get_schedule(self) -> None:
        if os.getenv('GUC_ID') is None:
            id = input("Enter your GUC ID: ")
            os.environ['GUC_ID'] = id
            print(f"GUC ID set to:  {os.getenv('GUC_ID')}")
        os.system(
            f"curl https://europe-west1-gucschedule.cloudfunctions.net/get_student_schedule\?id\={os.getenv('GUC_ID')}  >  {self.schedule_file}")

    def get_today_schedule(self) -> list:
        today = datetime.datetime.today()
        day_index = (today.weekday() + 2) % 7
        courses = self.get_courses_by_day(day_index)
        return courses

    def get_courses_by_day(self, day_index) -> list:
        courses = []
        for course in self.schedule:
            for session in course['sessions']:
                if session['x'] == day_index:
                    courses.append(course)
        return courses

    def print_today_schedule(self) -> None:
        for course in self.courses:
            course_type = ''.join(course['type'])
            course_name = ''.join(course['course_name'])
            location = ''.join(course['sessions'][0]['location'])
            staff = ''.join(course['sessions'][0]['staff'])
            slot = str(course['sessions'][0]['y'] + 1)
            self.courses_table.add_row(
                slot, course_type, course_name, location, staff)


if __name__ == "__main__":
    s = Schedule()
