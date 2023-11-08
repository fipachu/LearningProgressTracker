from base import Maim
from constants import COMPLETE_POINTS, COURSE_NAMES
from subshells import AddStudents, AddPoints, Find, Stats


class Tracker(Maim):
    intro = 'Learning Progress Tracker'

    def __init__(self):
        self.student_data = {}
        self.sent_notifications = set()
        super().__init__()

    def do_add(self, arg):
        match arg:
            case 'students':
                AddStudents(self.student_data).cmdloop()
            case 'points':
                AddPoints(self.student_data).cmdloop()
            case _:
                self.default(arg)

    def do_find(self, arg):
        match arg:
            case '':
                Find(self.student_data).cmdloop()
            case _:
                self.default(arg)

    def do_statistics(self, arg):
        match arg:
            case '':
                Stats(self.student_data).cmdloop()
            case _:
                self.default(arg)

    def do_list(self, arg):
        match arg, self.student_data:
            case '', data if data:
                print('Students:')
                print(*data, sep='\n')
            case '', _:
                print('No students found.')
            case _:
                self.default(arg)

    def do_notify(self, arg):
        match arg:
            case '':
                print(self.notifications())
            case _:
                self.default(arg)

    def notifications(self):
        template = ('To: {}\n'
                    'Re: Your Learning Progress\n'
                    'Hello, {}! You have accomplished our {} course!\n')

        pending = []
        students = 0
        for student in self.student_data.values():
            student_pending = False

            for points, complete, course in zip(student['points'], COMPLETE_POINTS, COURSE_NAMES):
                if points >= complete:
                    new = (student['email'],
                           ' '.join((student['first name'], student['last name'])),
                           course)
                    if new in self.sent_notifications:
                        continue

                    pending.append(new)
                    self.sent_notifications.add(new)
                    student_pending = True

            if student_pending:
                students += 1

        notifications = []
        for p in pending:
            notifications.append(template.format(*p))

        notifications.append(f'Total {students} students have been notified.')

        return ''.join(notifications)

    def do_exit(self, arg):
        match arg:
            case '':
                print('Bye!')
                return True
            case _:
                self.default(arg)

    def do_back(self, arg):
        match arg:
            case '':
                print("Enter 'exit' to exit the program.")
            case _:
                self.default(arg)

    def emptyline(self):
        print('No input.')

    def default(self, _):
        print('Error: unknown command!')

    def precmd(self, arg):
        arg = arg.lower()
        return arg
