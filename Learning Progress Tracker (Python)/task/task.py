import cmd


class TrackerShell(cmd.Cmd):
    intro = 'Learning Progress Tracker'
    prompt = ''
    # file = None

    def do_exit(self, arg):
        print('Bye!')
        return True

    def do_EOF(self, arg):
        return True

    def emptyline(self):
        print('No input.')

    def default(self, line):
        print('Error: unknown command!')

    def precmd(self, line):
        line = line.lower()
        return line


def main():
    TrackerShell().cmdloop()
    

if __name__ == "__main__":
    main()

# print("Learning progress tracker")
#
# # Interactive UI loop
# while True:
#     command: str = input().lower()
#
#     if command == 'exit':
#         print('Bye!')
#         break
#     elif command == '' or command.isspace():
#         print('No input')
#     else:
#         print('Unknown command!')
