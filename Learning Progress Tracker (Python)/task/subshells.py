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
                print(f"Incorrect {key.replace('_', ' ')}.")
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

        # logging.debug(f'{line=}')
        # logging.debug(f'{points=}')
        # logging.debug(f'{self.student_data=}')

        if points is not None:
            student_id, *points = points

            # logging.debug(f'{student_id=}')

            if student_id in self.student_data:
                if 'points' not in self.student_data[student_id]:
                    self.student_data[student_id]['points'] = [0] * 4

                self.student_data[student_id]['points'] = \
                    [old + p for old, p
                     in zip(self.student_data[student_id]['points'], points)]

                print('Points updated.')
                # logging.debug('Points added!')
            else:
                print(f'No student is found for id={student_id}')
        else:
            print('Incorrect points format.')


class FindShell(Subshell):
    intro = "Enter an id or 'back' to return:"

    def default(self, line):
        """Attempt to find a student with ID line"""
        student_id = line
        try:
            student_id = int(student_id)
        except ValueError:
            valid = False
        else:
            valid = True

        if valid and student_id in self.student_data:
            print('{} points: Python={}; DSA={}; Databases={}; Flask={}'
                  .format(student_id, *self.student_data[student_id]['points']))
        else:
            print(f'No student is found for id={line}.')
