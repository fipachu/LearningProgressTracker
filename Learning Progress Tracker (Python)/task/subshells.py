from base import Subshell
from parse import parse_points, parse_creds


class AddStudentsShell(Subshell):
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

        student_id = hash(creds['email'])
        if student_id in self.student_data:
            print('This email is already taken.')
            return
        else:
            self.student_data[student_id] = creds
            self.number_added += 1
            print('The student has been added.')


class AddPointsShell(Subshell):
    intro = "Enter an id and points or 'back' to return:"

    def default(self, line):
        """Attempt to add points based on input lines"""
        points = parse_points(line)
        if points is None:
            print('Incorrect points format.')
            return
        student_id, *points = points
        if student_id not in self.student_data:
            print(f'No student is found for id={student_id}')
            return

        if 'points' not in self.student_data[student_id]:
            self.student_data[student_id]['points'] = list(points)
        else:
            self.student_data[student_id]['points'] = \
                [old + p for old, p
                 in zip(self.student_data[student_id]['points'], points)]
        print('Points updated.')


class FindShell(Subshell):
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
