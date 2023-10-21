import cmd


class TrackerShell(cmd.Cmd):
    intro = 'Learning Progress Tracker'
    prompt = ''

    def do_exit(self, arg):
        if not arg:  # exit takes no arguments
            print('Bye!')
        else:
            self.default(arg)
        return True

    # Maim help to appease Hyperskill
    def do_help(self, arg):
        self.default(arg)

    def emptyline(self):
        print('No input.')

    def default(self, arg):
        print('Error: unknown command!')

    def precmd(self, arg):
        arg = arg.lower()
        return arg


if __name__ == "__main__":
    TrackerShell().cmdloop()
