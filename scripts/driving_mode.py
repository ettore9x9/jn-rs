#! /usr/bin/env python

import rospy
import curses

import user_interface
import autonomous_driving
import free_drive
import client_drive_assistance


def ask_for_goal():
    while True:

        ui.win_request.addstr(0, 0, "Insert the x position:")
        ui.win_request.refresh()
        x = ui.win_input.getstr(0, 0, 3)
        ui.clear_input()

        try:
            fx = float(x)
            break

        except:
            ui.win_request.addstr(0, 23, "(try again)")

    ui.clear_request()

    while True:

        ui.win_request.addstr(0, 0, "Insert the y position: ")
        ui.win_request.refresh()
        y = ui.win_input.getstr(0, 0, 3)
        ui.clear_input()

        try:
            fy = float(y)
            break

        except:
            ui.win_request.addstr(0, 23, "(try again)")

    ui.clear_request()

    return fx, fy

if __name__=="__main__":

    try:
        ui = user_interface.windows_organiser()

        # Init the ros node.
        rospy.init_node('driving_mode')

        ad = autonomous_driving.autonomous_driving(ui)

        while not rospy.is_shutdown():

            key = ui.win_input.getch() # Gets the user command.

            ui.win_info.addch(1, 18, key)
            ui.win_info.refresh()

            if key == ord('q'):
                break

            elif key == ord('1') and ad.is_active is False:
                ui.clear_request()
                ui.win_modes.addstr(0, 0, "-->")
                ui.win_modes.refresh()

                x, y = ask_for_goal()
                ad.reach_goal(x, y)

            elif key == ord('2'):

                if ad.is_active is True:
                    ad.cancel_goal()

                ui.clear_request()
                free_drive.free_drive(ui)

            elif key == ord('3'):

                if ad.is_active is True:
                    ad.cancel_goal()

                ui.clear_request()
                client_drive_assistance.drive_assistance(ui)

            elif key == ord('c') and ad.is_active is True:
                ui.clear_request()
                ad.cancel_goal()

            elif key == ord('n') and ad.is_active is True:
                ui.clear_request()
                ad.cancel_goal()
                x, y = ask_for_goal()
                ad.reach_goal(x, y)

            else:
                ui.command_not_vaid()

    except Exception as e:
        print(e)

    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()