import cmd
import logging
import re
from typing import NamedTuple

logging.basicConfig(level=logging.DEBUG)


class Creds(NamedTuple):
    first_name: str | None
    last_name: str | None
    email: str | None


class TrackerShell(cmd.Cmd):
    intro = 'Learning Progress Tracker'
    prompt = ''

    student_data = {}

    def do_add(self, arg):
        # do_add requires subcommand students
        if arg and arg == 'students':
            AddStudentsShell(self.student_data).cmdloop()
        elif arg and arg == 'points':
            AddPointsShell(self.student_data).cmdloop()
        else:
            self.default(arg)

    def do_find(self, arg):
        if not arg:
            FindShell(self.student_data).cmdloop()
        else:
            self.default(arg)

    def do_list(self, arg):
        if not arg:
            if self.student_data:
                print('Students:')
                print(*self.student_data, sep='\n')
            else:
                print('No students found.')

        else:
            self.default(arg)

    def do_exit(self, arg):
        # exit takes no arguments
        if not arg:
            print('Bye!')
        else:
            self.default(arg)
        return True

    def do_back(self, arg):
        if not arg:
            print("Enter 'exit' to exit the program.")
        else:
            self.default(arg)

    # Maim help to appease Hyperskill
    def do_help(self, arg):
        self.default('help' + arg)

    def emptyline(self):
        print('No input.')

    def default(self, _):
        print('Error: unknown command!')

    def precmd(self, arg):
        arg = arg.lower()
        return arg


class AddStudentsShell(cmd.Cmd):
    intro = "Enter student credentials or 'back' to return:"
    prompt = ''
    number_added = 0
    student_data: dict

    def __init__(self, student_data):
        self.student_data = student_data
        super().__init__()

    def do_back(self, arg):
        if not arg:
            print(f'Total {self.number_added} students have been added.')
            return True
        else:
            self.default('back' + arg)

    def do_help(self, arg):
        self.default('help' + arg)

    def emptyline(self):
        self.default('')

    def default(self, line):
        """Attempt to add students to student_data"""
        creds = parse_creds(line)
        if creds is not None:
            for key, cred in creds.items():
                key = key.replace('_', ' ')
                if not cred:
                    print(f'Incorrect {key}.')
                    break
            else:
                # creds are valid
                student_id = hash(creds['email'])
                if student_id not in self.student_data:
                    self.student_data[student_id] = creds
                    self.number_added += 1
                    print('The student has been added.')
                else:
                    print('This email is already taken.')
        else:
            print('Incorrect credentials')

    def precmd(self, line):
        """Make line lowercase, but only if a corresponding command exists"""
        lower = line.lower()
        try:
            getattr(self, 'do_' + lower)
            line = lower
        except AttributeError:
            pass
        return line


class AddPointsShell(AddStudentsShell):
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


class FindShell(AddStudentsShell):
    intro = "Enter an id or 'back' to return:"

    def default(self, line):
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


def parse_points(line: str) -> tuple[int, ...] | None:
    line = line.split()
    if len(line) == 5:
        student_id, *points = line
        try:
            points = [int(p) for p in points]
        except ValueError:
            return None

        try:
            student_id = int(student_id)
        except ValueError:
            pass

        for p in points:
            if p < 0:
                return None

        return student_id, *points
    else:
        return None


def parse_creds(line: str) -> dict | None:
    """Parse user-provided credentials

    Return a Creds object with credentials as attributes,
    replacing invalid credentials with None.

    Return None if any credentials are missing.
    """
    match = re.match(r'(\S+) (.+) (\S+)', line)
    if match:
        first_name, last_name, email = match.groups()

        first_name = re.fullmatch("""
                (?!.*[-']{2})  # No doubles allowed
                (?![-'])  # Not allowed at the beginning
                ([A-Za-z-']{2,})  # First name
                (?<![-'])  # Not allowed at the end
                """, first_name, flags=re.VERBOSE)
        first_name = first_name and first_name.group()

        last_name = re.fullmatch("""
                (?!.*[-']{2})  # No doubles allowed
                (?![-'])  # Not allowed at the beginning
                ([A-Za-z-' ]{2,})  # Last name
                (?<![-'])  # Not allowed at the end
                """, last_name, flags=re.VERBOSE)
        last_name = last_name and last_name.group()

        email = re.fullmatch(r"[-.\w]+@[-.\w]+\.[-.\w]+", email)
        email = email and email.group()

        return dict(first_name=first_name, last_name=last_name, email=email)
    else:
        return None


if __name__ == "__main__":
    TrackerShell().cmdloop()
