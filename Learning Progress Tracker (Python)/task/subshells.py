# TODO: clean up all the logging statements
import logging

from base import Subshell, add_values
from constants import MAX_HASH, COURSE_NAMES
from parse import parse_points, parse_creds

logging.basicConfig(level=logging.DEBUG)


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
            # TODO: initialize student_data with points and submissions
            #   with values [0]*4 to prevent KeyError in code assuming
            #   these keys exist
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

    def preloop(self):
        stats = self.get_stats()
        stats = [s if s is not None else 'n/a'
                 for s in stats]
        self.intro += self.INFO.format(*stats)
        logging.debug(f'intro:\n{self.intro}')

    def get_stats(self) -> (str | None,) * 6:
        # TODO: refactor this method, cuz it UGLY
        # return (None,) * 6

        # Count enrolled students by course:
        enrolled_counts = [0] * 4
        for student in self.student_data.values():
            # If a student has any submissions in a course, they are enrolled
            students_courses = [int(bool(i)) for i in student['submissions']]
            enrolled_counts = add_values(enrolled_counts, students_courses)
        # DEBUG('popularity', enrolled_counts)

        # Count submissions by course
        submission_counts = [0] * 4
        for student in self.student_data.values():
            submission_counts = add_values(submission_counts, student['submissions'])
        # DEBUG('activity', submission_counts)

        # Calculate average grade per submission per course
        total_grades = [0] * 4
        for student in self.student_data.values():
            total_grades = add_values(total_grades, student['points'])
        # DEBUG('total_grades', total_grades)
        # TODO?: something to stop a course with no submissions from
        #   being considered hardest?
        average_grades = \
            [t / s if s != 0 else 0
             for t, s in zip(total_grades, submission_counts)]
        # DEBUG('difficulty', average_grades)

        output = []
        for metric in (enrolled_counts, submission_counts, average_grades):
            output.extend(self.get_most_and_least(metric))
        return output

        # TODO:
        #   Figure out a way to "establish top learners for each course",
        #   ergo: list student ID's by decreasing points for every course,
        #   and by ID on conflicts.

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


def DEBUG(message, var):
    logging.debug(f'{message}:{var}')


if __name__ == '__main__':
    # Stats({}).cmdloop()
    Stats(
        {
            752001:
                {
                    'points': [6.9, 20, 6, 0],
                    'submissions': [10, 5, 2, 0]
                },
            # 752002:
            #     {
            #         'points': [1, 1, 1, 0],
            #         'submissions': [1, 1, 1, 0]
            #     },
            # 752003:
            #     {
            #         'points': [0, 0, 0, 0],
            #         'submissions': [0, 0, 0, 0]
            #     },
            # # This would cause a KeyError somewhere lmao.
            # 752004:
            #     {
            #     },
        }
    ).preloop()
