print("Learning progress tracker")

# Interactive UI loop
while True:
    command: str = input().lower()

    if command == 'exit':
        print('Bye!')
        break
    elif command == '' or command.isspace():
        print('No input')
    else:
        print('Unknown command!')
