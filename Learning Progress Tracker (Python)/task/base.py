import cmd


class Maim(cmd.Cmd):
    """Base class mainly for maiming prompt and help"""
    prompt = ''
    student_data: dict

    def do_help(self, arg):
        self.default('help ' + arg)


class Subshell(Maim):
    """Base class for all subshells"""

    def __init__(self, student_data):
        self.student_data = student_data
        super().__init__()

    def emptyline(self):
        self.default('')

    def do_back(self, arg):
        match arg:
            case '':
                return True
            case _:
                self.default('back ' + arg)

    def precmd(self, line):
        """Make line lowercase, but only if a corresponding command exists"""
        lower = line.lower()
        try:
            getattr(self, 'do_' + lower)
            line = lower
        except AttributeError:
            pass
        return line
