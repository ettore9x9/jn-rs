#! /usr/bin/env python

import curses
import text

class windows_organiser:

    def __init__(self):

        self.stdscr = curses.initscr()
        self.stdscr.addstr(0, 0, text.title)
        self.stdscr.refresh()

        self.win_modes = curses.newwin(14, 36, 9, 0)
        self.win_modes.addstr(0, 0, text.modalities)
        self.win_modes.refresh()

        self.win_info = curses.newwin(5, 45, 19, 39)
        self.win_info.addstr(0, 0, text.info)
        self.win_info.refresh()

        self.win_input = curses.newwin(1, 5, 23, 0)
        self.win_request = curses.newwin(1, 35, 22, 0)

    def clear_modes(self):
        self.win_modes.clear()
        self.win_modes.addstr(0, 0, text.modalities)
        self.win_modes.refresh()

    def clear_info(self):
        self.win_info.clear()
        self.win_info.addstr(0, 0, text.info)
        self.win_info.refresh()

    def clear_input(self):
        self.win_input.clear()
        self.win_input.refresh()

    def clear_request(self):
        self.win_request.clear()
        self.win_request.refresh()

    def set_wasd(self):
        self.win_modes.clear()
        self.win_modes.addstr(0, 0, text.wasd)
        self.win_modes.refresh()

    def command_not_valid(self):
        self.win_request.clear()
        self.win_request.addstr(0, 0, "Command NOT valid")
        self.win_request.refresh()
