#!/usr/bin/env python
# coding: utf-8
#
# AutoClosePanel.py
#
# AGPLv3 License
# Created by github.com/aerobounce on 2022/01/27.
# Copyright © 2022 to Present, aerobounce. All rights reserved.
#

from re import findall
from sublime import Region, View, Window, load_settings, windows
from sublime_plugin import EventListener, WindowCommand


SETTINGS_FILENAME = "AutoClosePanel.sublime-settings"
ON_CHANGE_TAG = "reload_settings"


def plugin_loaded():
    AutoClosePanel.settings = load_settings(SETTINGS_FILENAME)
    AutoClosePanel.reload_settings()
    AutoClosePanel.settings.add_on_change(ON_CHANGE_TAG, AutoClosePanel.reload_settings)


def plugin_unloaded():
    AutoClosePanel.settings.clear_on_change(ON_CHANGE_TAG)


class AutoClosePanel:
    settings = load_settings(SETTINGS_FILENAME)
    close_panel_on_save = False
    close_panel_on_activate = False
    matching_mode = 2
    matching_max_count = 5
    target_panels = {}

    @classmethod
    def reload_settings(cls):
        cls.close_panel_on_save = cls.settings.get("close_panel_on_save")
        cls.close_panel_on_activate = cls.settings.get("close_panel_on_activate")
        cls.matching_mode = cls.settings.get("matching_mode")
        cls.matching_max_count = cls.settings.get("matching_max_count")
        cls.target_panels = cls.settings.get("target_panels")

    @classmethod
    def print_all_window_panels(cls):
        for window in windows():
            active_panel_name = window.active_panel()
            if active_panel_name:
                print("[AutoClosePanel] Found panel:", active_panel_name)

    @classmethod
    def hide_panel(cls, window: Window):
        panel_name = (window.active_panel() or "").replace("output.", "")

        if not panel_name in cls.target_panels.keys():
            return
        active_panel = window.find_output_panel(panel_name)

        if active_panel == None:
            return

        def hide_matched_panel(text: str) -> bool:
            for pattern in cls.target_panels[panel_name]:
                if findall(pattern, text):
                    window.run_command("hide_panel", {"panel": "output." + panel_name})
                    return True
            return False

        entire_region = Region(0, active_panel.size())
        splitted_regions = active_panel.split_by_newlines(entire_region)

        # Find in the entire string
        if cls.matching_mode == 0 or len(splitted_regions) == 1:
            hide_matched_panel(active_panel.substr(entire_region))
            return

        #
        # TODO: Could this dirty block be a bit more cleaner?
        #

        # Limited lines, line by line
        if cls.matching_max_count > 0:
            # Find from the top of string
            if cls.matching_mode == 1:
                splitted_regions.reverse()

            regions_of_lines = []
            for _ in range(0, cls.matching_max_count):
                # Bound check
                if len(splitted_regions) > 0:
                    regions_of_lines.append(splitted_regions.pop())

        # Entire text, line by line
        else:
            # Find from the bottom of string
            if cls.matching_mode == 2:
                splitted_regions.reverse()
            regions_of_lines = splitted_regions

        for region in regions_of_lines:
            if hide_matched_panel(active_panel.substr(region)):
                return


class AutoClosePanelCloseCommand(WindowCommand):
    def run(self):
        AutoClosePanel.hide_panel(self.window)


class AutoClosePanelPrintPanelsCommand(WindowCommand):
    def run(self):
        AutoClosePanel.print_all_window_panels()


class AutoClosePanelListener(EventListener):
    last_activated_view_id = -999

    def on_pre_save(self, view: View):
        if AutoClosePanel.close_panel_on_save:
            window = view.window()
            if window:
                AutoClosePanel.hide_panel(window)

    def on_activated_async(self, view: View):
        if AutoClosePanel.close_panel_on_activate:
            # This hook is called for output panel view too.
            # Prevent unintended close by checking filename.
            if view.file_name() == None:
                return
            # Prevent unintended close in cases e.g.:
            #  Build -> Focus Result -> Focus Built View
            if self.last_activated_view_id != view.id():
                self.last_activated_view_id = view.id()
                window = view.window()
                if window:
                    AutoClosePanel.hide_panel(window)
