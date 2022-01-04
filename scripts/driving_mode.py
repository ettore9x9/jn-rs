#! /usr/bin/env python

import rospy
import actionlib
import curses

from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from final_assignment.srv import Command

title = R"""              _      _       _                                   _
           __| |_ __(_)_   _(_)_ __   __ _   _ __ ___   ___   __| | ___
          / _` | '__| \ \ / / | '_ \ / _` | | '_ ` _ \ / _ \ / _` |/ _ \
=========| (_| | |  | |\ V /| | | | | (_| | | | | | | | (_) | (_| |  __/=======
          \__,_|_|  |_| \_/ |_|_| |_|\__, | |_| |_| |_|\___/ \__,_|\___|
                                     |___/                              
   
Choose one of the following driving modality:"""

modalities = """    1 - Autonomous driving
    2 - Free drive
    3 - Driver assistance




    q - for quit
"""

info = """INFO-------------------------------------
| Last command = 
|
|
|                        """

moves = """    w - Increase linear speed
    s - Decrease linear speed
    a - Increase ang. speed (left)
    d - Decrease ang. speed (right)
    z - Stop angular speed
    x - Stop linear speed

    q - Leave free drive mode"""

def ask_for_goal():
    while True:

        win_request.addstr(0, 0, "Insert the x position:")
        win_request.refresh()
        win_input.clear()
        x = win_input.getstr(0, 0, 3)

        try:
            fx = float(x)
            break

        except:
            win_request.addstr(0, 23, "(try again)")

    win_request.clear()

    while True:

        win_request.addstr(0, 0, "Insert the y position: ")
        win_request.refresh()
        win_input.clear()
        y = win_input.getstr(0, 0, 3)

        try:
            fy = float(y)
            break

        except:
            win_request.addstr(0, 23, "(try again)")

    win_request.clear()
    win_request.refresh()
    win_input.clear()
    win_input.refresh()
    return fx, fy

class autonomous_driving():

    def __init__(self):

        self.goal_counter = 0
        self.feedback_counter = 0
        self.is_active = False

        self.title = R"""    c - to cancel goal
    n - to insert a new goal"""

        # Creates the MoveBaseActionClient
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    def active_cb(self):
        win_info.addstr(2, 1, "Action Server is processing goal n "+str(self.goal_counter+1)+" ... ")
        win_info.refresh()


    def feedback_cb(self, feedback):
        self.feedback_counter += 1
        win_info.addstr(3, 1, "Feedback for goal n "+str(self.goal_counter+1)+" received.          ")
        win_info.addstr(3, 31 + self.feedback_counter % 10, ">")
        win_info.refresh()


    def done_cb(self, status, result):
        self.goal_counter += 1
        self.is_active = False

        win_modes.clear()
        win_modes.addstr(0, 0, modalities)
        win_modes.refresh()

        if status == 2:
            win_info.addstr(4, 1, "Goal n "+str(self.goal_counter)+" received a cancel request.")
            win_info.refresh()
            return

        if status == 3:
            win_info.addstr(4, 1, "Goal n "+str(self.goal_counter)+" reached.                  ")
            win_info.refresh()
            return

        if status == 4:
            win_info.addstr(4, 1, "Goal n "+str(self.goal_counter)+" was aborted.              ")
            win_info.refresh()
            return

        if status == 5:
            win_info.addstr(4, 1, "Goal n "+str(self.goal_counter)+" has been rejected.        ")
            win_info.refresh()
            return

        if status == 8:
            win_info.addstr(4, 1, "Goal n "+str(self.goal_counter)+" received a cancel request.")
            win_info.refresh()
            return

   
    def reach_goal(self, x, y):

        # Waits until the action server has started up and started
        # listening for goals.
        self.is_active = True

        self.client.wait_for_server()

        win_modes.addstr(3, 0, self.title)
        win_modes.refresh()

        # Creates a goal to send to the action server.
        goal = MoveBaseGoal()

        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.orientation.w = 1
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
   
        # Sends the goal to the action server.
        self.client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)

    def cancel_goal(self):
        self.is_active = False
        self.client.cancel_goal()
        win_modes.clear()
        win_modes.addstr(0, 0, modalities)
        win_modes.refresh()


def free_drive():

    pub = rospy.Publisher("cmd_vel", Twist)
    char = 'n'
    straight = 0
    turn = 0
    my_vel = Twist();

    curses.noecho()
    curses.cbreak()

    win_modes.clear()
    win_modes.addstr(0, 0, moves)
    win_modes.refresh()

    win_info.clear()
    win_info.addstr(0, 0, info)
    win_info.refresh()

    while True:

        char = win_input.getch() # Gets the user command.
        win_input.clear()

        if char == ord('q'):
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

        msg_linear = "Linear velocity: %.1f" % straight
        win_info.addstr(2, 1, msg_linear)

        msg_angular = "Angular velocity: %.1f" % turn
        win_info.addstr(3, 1, msg_angular)
        win_info.refresh()

        my_vel.linear.x = straight;
        my_vel.angular.z = turn;
        pub.publish(my_vel);

    my_vel.linear.x = 0;
    my_vel.angular.z = 0;
    pub.publish(my_vel);

    curses.echo()
    curses.nocbreak()

    win_modes.clear()
    win_modes.addstr(0, 0, modalities)
    win_modes.refresh()


def drive_assistance():

    client = rospy.ServiceProxy("/command", Command)
    char = 'n'

    srv_com = Command();

    curses.noecho()
    curses.cbreak()

    win_modes.clear()
    win_modes.addstr(0, 0, moves)
    win_modes.refresh()

    win_info.clear()
    win_info.addstr(0, 0, info)
    win_info.refresh()

    rospy.wait_for_service("/command")

    while True:

        char = win_input.getch() # Gets the user command.
        win_input.clear()

        if char == ord('q'):
            break

        elif char == ord('w') or char == ord('s') or char == ord('d') or char == ord('a') or char == ord('x') or char == ord('z'):
            srv_com.request.command = char

        char = 'n'

        client.call(srv_com)

        msg_linear = "Linear velocity: %.1f" % srv_com.response.linear
        win_info.addstr(2, 1, msg_linear)

        msg_angular = "Angular velocity: %.1f" % srv_com.response.angular
        win_info.addstr(3, 1, msg_angular)
        win_info.refresh()


    srv_com.request.command = 'x'
    client.call(srv_com)

    srv_com.request.command = 'z'
    client.call(srv_com)

    curses.echo()
    curses.nocbreak()

    win_modes.clear()
    win_modes.addstr(0, 0, modalities)
    win_modes.refresh()


if __name__=="__main__":

    try:

        stdscr = curses.initscr()
        stdscr.addstr(0, 0, title)
        stdscr.refresh()

        win_modes = curses.newwin(14, 36, 9, 0)
        win_modes.addstr(0, 0, modalities)
        win_modes.refresh()

        win_info = curses.newwin(5, 45, 19, 39)
        win_info.addstr(0, 0, info)
        win_info.refresh()

        win_input = curses.newwin(1, 5, 23, 0)
        win_request = curses.newwin(1, 35, 22, 0)

        # Init the ros node.
        rospy.init_node('driving_mode')

        ad = autonomous_driving()

        while not rospy.is_shutdown():

            key = win_input.getch() # Gets the user command.
            win_input.clear()
            win_request.clear()
            win_request.refresh()

            win_info.addch(1, 18, key)
            win_info.refresh()

            if key == ord('q'):
                break

            elif key == ord('1') and ad.is_active is False: 
                win_modes.clear()
                win_modes.addstr(0, 0, modalities)
                win_modes.addstr(0, 0, "-->")
                win_modes.refresh()

                x, y = ask_for_goal()
                ad.reach_goal(x, y)

            elif key == ord('2'):

                if ad.is_active is True:
                    ad.cancel_goal()

                win_modes.clear()
                win_modes.addstr(0, 0, modalities)
                win_modes.addstr(1, 0, "-->")
                win_modes.refresh()

                free_drive()

            elif key == ord('3'):

                if ad.is_active is True:
                    ad.cancel_goal()

                win_modes.clear()
                win_modes.addstr(0, 0, modalities)
                win_modes.addstr(2, 0, "-->")
                win_modes.refresh()

                drive_assistance()

            elif key == ord('c') and ad.is_active is True:
                ad.cancel_goal()

            elif key == ord('n') and ad.is_active is True:
                ad.cancel_goal()
                x, y = ask_for_goal()
                ad.reach_goal(x, y)

            else:
                win_request.addstr(0, 0, "Command NOT valid")
                win_request.refresh()

    except Exception as e:
        print(e)

    finally:

        curses.nocbreak()
        curses.echo()
        #curses.endwin()