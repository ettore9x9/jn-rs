#! /usr/bin/env python

import rospy
import curses

from geometry_msgs.msg import Twist

def free_drive(ui):

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
    char = 'n'
    straight = 0
    turn = 0
    my_vel = Twist();

    curses.noecho()
    curses.cbreak()

    ui.set_wasd()
    ui.clear_info()

    while True:

        char = ui.win_input.getch() # Gets the user command.
        ui.clear_input()

        if char == ord('q'):
            ui.clear_modes()
            break

        elif char == ord('w'):
            straight += 0.1

        elif char == ord('s'):
            straight += -0.1

        elif char == ord('d'):
            turn += -0.1

        elif char == ord('a'):
            turn += 0.1

        elif char == ord('x'):
            straight = 0

        elif char == ord('z'):
            turn = 0

        char = 'n'

        msg_linear = "Linear velocity: %.1f  " % straight
        ui.win_info.addstr(2, 1, msg_linear)

        msg_angular = "Angular velocity: %.1f  " % turn
        ui.win_info.addstr(3, 1, msg_angular)
        ui.win_info.refresh()

        my_vel.linear.x = straight;
        my_vel.angular.z = turn;
        pub.publish(my_vel);

    my_vel.linear.x = 0;
    my_vel.angular.z = 0;
    pub.publish(my_vel);

    curses.echo()
    curses.nocbreak()

    ui.clear_modes()