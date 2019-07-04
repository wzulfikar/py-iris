#!/usr/bin/env python3
import sys
from halo import Halo

import lib.command_runner as command_runner


def main():
    with Halo(text='', spinner='dots'):
        # this will take a while
        import register_commands

    commands = register_commands.commands
    if len(sys.argv) == 1:
        command_runner.list_commands(commands)
        exit(1)

    # handle command
    _, command, *args = sys.argv
    command_runner.run(commands, command, args)


# import pipelines and commands configured by user
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[DONE] user interrupted')
