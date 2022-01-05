#! /usr/bin/env python

import rospy
import actionlib

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class autonomous_driving:

    def __init__(self, user_interface):

        self.goal_counter = 0
        self.feedback_counter = 0
        self.is_active = False

        self.title = R"""    c - to cancel goal
    n - to insert a new goal"""

        # Creates the MoveBaseActionClient
        self.client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
        self.ui = user_interface

    def active_cb(self):
        self.ui.win_info.addstr(2, 1, "Action Server is processing goal n "+str(self.goal_counter+1)+" ... ")
        self.ui.win_info.refresh()


    def feedback_cb(self, feedback):
        self.feedback_counter += 1
        self.ui.win_info.addstr(3, 1, "Feedback for goal n "+str(self.goal_counter+1)+" received.          ")
        self.ui.win_info.addstr(3, 31 + self.feedback_counter % 10, ">")
        self.ui.win_info.refresh()


    def done_cb(self, status, result):
        self.goal_counter += 1
        self.is_active = False
        self.ui.clear_modes()

        if status == 2:
            self.ui.win_info.addstr(4, 1, "Goal n "+str(self.goal_counter)+" received a cancel request.")
            self.ui.win_info.refresh()
            return

        if status == 3:
            self.ui.win_info.addstr(4, 1, "Goal n "+str(self.goal_counter)+" reached.                  ")
            self.ui.win_info.refresh()
            return

        if status == 4:
            self.ui.win_info.addstr(4, 1, "Goal n "+str(self.goal_counter)+" was aborted.              ")
            self.ui.win_info.refresh()
            return

        if status == 5:
            self.ui.win_info.addstr(4, 1, "Goal n "+str(self.goal_counter)+" has been rejected.        ")
            self.ui.win_info.refresh()
            return

        if status == 8:
            self.ui.win_info.addstr(4, 1, "Goal n "+str(self.goal_counter)+" received a cancel request.")
            self.ui.win_info.refresh()
            return

    def reach_goal(self, x, y):

        # Waits until the action server has started up and started
        # listening for goals.
        self.is_active = True

        self.client.wait_for_server()

        self.ui.win_modes.addstr(3, 0, self.title)
        self.ui.win_modes.refresh()

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
        self.ui.clear_modes()