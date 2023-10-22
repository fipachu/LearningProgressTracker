import cmd
import re
from typing import NamedTuple


class Creds(NamedTuple):
    first_name: str | None
    last_name: str | None
    email: str | None


class TrackerShell(cmd.Cmd):
    intro = 'Learning Progress Tracker'
    prompt = ''

    def do_add(self, arg):
        # do_add requires subcommand students
        if arg and arg == 'students':
            AddStudentsShell().cmdloop()
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
        creds = parse_creds(line)
        if creds:
            for key, cred in zip(creds._fields, creds):
                key = key.replace('_', ' ')
                if not cred:
                    print(f'Incorrect {key}.')
                    break
            else:
                self.number_added += 1
                print('The student has been added.')
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


def parse_creds(line: str) -> Creds | None:
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

        return Creds(first_name, last_name, email)

    else:
        return None


if __name__ == "__main__":
    TrackerShell().cmdloop()
