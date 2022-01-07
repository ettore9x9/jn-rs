#! /usr/bin/env python

import rospy
import curses

from final_assignment.srv import Command

def drive_assistance(ui):

    client = rospy.ServiceProxy("/command", Command)
    char = 'n'

    curses.noecho()
    curses.cbreak()

    ui.set_wasd()
    ui.clear_info()

    rospy.wait_for_service("/command")

    client(ord('0'))

    while True:

        char = ui.win_input.getch() # Gets the user command.
        ui.clear_input()

        if char == ord('b'):
            ui.clear_modes()
            break

        elif char == ord('w') or char == ord('s') or char == ord('d') or char == ord('a') or char == ord('x') or char == ord('z'):
            resp = client(char)
            msg_linear = "Linear velocity: %.1f  " % resp.linear
            ui.win_info.addstr(2, 1, msg_linear)

            msg_angular = "Angular velocity: %.1f  " % resp.angular
            ui.win_info.addstr(3, 1, msg_angular)
            ui.win_info.refresh()

    client(ord('x'))
    client(ord('z'))
    client(ord('1'))

    curses.echo()
    curses.nocbreak()

    ui.clear_modes()
