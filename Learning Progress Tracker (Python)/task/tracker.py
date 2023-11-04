from base import Maim
from subshells import AddStudents, AddPoints, Find, Stats


class Tracker(Maim):
    intro = 'Learning Progress Tracker'
    student_data = {}

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
