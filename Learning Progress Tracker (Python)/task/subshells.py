import operator

from base import Subshell
from constants import MAX_HASH, COURSE_NAMES, COMPLETE_POINTS
from parse import parse_points, parse_creds


class AddStudents(Subshell):
    intro = "Enter student credentials or 'back' to return:"
    number_added = 0

    def do_back(self, arg):
        if arg == '':
            print(f'Total {self.number_added} students have been added.')
        return super().do_back(arg)

    def default(self, line):
        """Attempt to add students to student_data"""
        creds = parse_creds(line)
        if creds is None:
            print('Incorrect credentials')
            return
        for key, cred in creds.items():
            if cred is None:
                print(f"Incorrect {key}.")
                return

        student_id = hash(creds['email']) % MAX_HASH
        if student_id in self.student_data:
            print('This email is already taken.')
            return
        else:
            # FIXME?: initialize student_data with points and submissions
            #   with values [0]*4 to prevent KeyError in code assuming
            #   these keys exist.
            self.student_data[student_id] = creds
            self.number_added += 1
            print('The student has been added.')


class AddPoints(Subshell):
    intro = "Enter an id and points or 'back' to return:"

    def default(self, line):
        """Attempt to add points and submission counts based on input lines"""
        points = parse_points(line)
        if points is None:
            print('Incorrect points format.')
            return
        student_id, *points = points
        if student_id not in self.student_data:
            print(f'No student is found for id={student_id}')
            return

        submissions = (int(bool(x)) for x in points)
        self.update_list('points', points, student_id)
        self.update_list('submissions', submissions, student_id)
        print('Points updated.')

    def update_list(self, name, incoming, student_id):
        if name not in self.student_data[student_id]:
            self.student_data[student_id][name] = list(incoming)
        else:
            self.student_data[student_id][name] = \
                [old + i for old, i
                 in zip(self.student_data[student_id][name], incoming)]


class Find(Subshell):
    intro = "Enter an id or 'back' to return:"

    def default(self, line):
        """Attempt to find a student with matching ID"""
        student_id = line
        try:
            student_id = int(student_id)
        except ValueError:
            pass
        if student_id not in self.student_data:
            # Use unchanged user input in feedback
            print(f'No student is found for id={line}.')
            return

        print('{} points: Python={}; DSA={}; Databases={}; Flask={}'
              .format(student_id, *self.student_data[student_id]['points']))


class Stats(Subshell):
    intro = "Type the name of a course to see details or 'back' to quit:\n"
    INFO = ('Most popular: {}\n'
            'Least popular: {}\n'
            'Highest activity: {}\n'
            'Lowest activity: {}\n'
            'Easiest course: {}\n'
            'Hardest course: {}')
    MASTER = '{:<7}{:<10}{:<9{percent}}'
    DATA_HEADER = (MASTER.replace('{percent}', ''))
    DATA = MASTER.replace('{percent}', '.1%')

    def preloop(self):
        stats = self.intro_stats()
        stats = [s if s is not None else 'n/a'
                 for s in stats]
        self.intro += self.INFO.format(*stats)

    def default(self, _):
        print('Unknown course.')

    def do_python(self, arg):
        self.course(0, arg)

    def do_dsa(self, arg):
        self.course(1, arg)

    def do_databases(self, arg):
        self.course(2, arg)

    def do_flask(self, arg):
        self.course(3, arg)

    def course(self, course_id, arg):
        match arg:
            case '':
                course_intro = self.course_intro(course_id)
                lines = self.formatted_stats(course_id)
                print(course_intro)
                print(*lines, sep='\n')
            case _:
                self.default(None)

    def course_intro(self, course_id):
        course_intro = (COURSE_NAMES[course_id] + "\n"
                        + self.DATA_HEADER.format('id', 'points', 'completed'))
        return course_intro

    def formatted_stats(self, course_id):
        line_template = self.DATA
        course_stats = self.course_stats(course_id)
        lines = [line_template] * len(course_stats)
        lines = [line.format(*row) for line, row
                 in zip(lines, course_stats)]
        return lines

    def course_stats(self, course: int) -> [(int, int, float), ...]:
        """Return stats of students enrolled in course as a sequence of
        tuples (id, points, completed) sorted by points, then id."""
        stats = []
        for student_id, data in self.student_data.items():
            points = data['points'][course]
            if points:  # Student is enrolled in course
                completed = points / COMPLETE_POINTS[course]
                entry: tuple = (student_id, points, completed)
                stats.append(entry)

        stats.sort(key=operator.itemgetter(0))
        stats.sort(key=operator.itemgetter(1), reverse=True)
        return stats

    def intro_stats(self) -> (str | None,) * 6:
        # FIXME?: a course with no submissions can be considered hardest
        #         it passes the Hyperskill test but seems bad.

        # Maybe this can be done elegantly in a loop. Maybe.
        enrolled_counts = self.magic_sum('submissions', counting_mode=True)
        submission_counts = self.magic_sum('submissions')
        total_grades = self.magic_sum('points')
        average_grades = [(t / s) if s != 0 else 0
                          for t, s in zip(total_grades, submission_counts)]

        output = []
        for metric in (enrolled_counts, submission_counts, average_grades):
            output.extend(self.get_most_and_least(metric))
        return output

    def magic_sum(self, column: str, counting_mode=False):
        out = [0] * 4
        for student in self.student_data.values():
            field = student[column]
            if counting_mode:
                field = [int(bool(n)) for n in field]
            out = (self.add_values(out, field))
        return out

    @staticmethod
    def add_values(sequence_1, sequence_2):
        return [x + y for x, y in zip(sequence_1, sequence_2)]

    @staticmethod
    def get_most_and_least(metric) -> (str | None,) * 2:
        """Return all the "most" courses, and the "least" course
        if there is exactly one; according to the metric.

        Return (None, None) if metric for all courses is 0.

        Return (most, None) if there is wrong number of least courses,
        as there can only be one least course.
        """
        if metric == [0] * 4:
            return None, None

        max_value, min_value = max(metric), min(metric)
        most, least = [], []
        for i, value in enumerate(metric):
            if value == max_value:
                most.append(COURSE_NAMES[i])
            elif value == min_value:
                least.append(COURSE_NAMES[i])

        if len(least) != 1:
            least = [None]

        return ', '.join(most), least[0]
