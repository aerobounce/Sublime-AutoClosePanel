#!/usr/bin/env python
# coding: utf-8
#
# AutoClosePanel.py
#
# AGPLv3 License
# Created by github.com/aerobounce on 2022/01/27.
# Copyright © 2022 to Present, aerobounce. All rights reserved.
#

import re
import sublime
import sublime_plugin

SETTINGS_FILENAME = "AutoClosePanel.sublime-settings"
SETTINGS_KEYS = ["close_panel_on_save", "target_panels"]
ON_CHANGE_TAG = "reload_settings"


def plugin_loaded():
    AutoClosePanel.settings = sublime.load_settings(SETTINGS_FILENAME)
    AutoClosePanel.reload_settings()
    AutoClosePanel.settings.add_on_change(ON_CHANGE_TAG, AutoClosePanel.reload_settings)


def plugin_unloaded():
    AutoClosePanel.settings.clear_on_change(ON_CHANGE_TAG)


class AutoClosePanel:
    settings = sublime.load_settings(SETTINGS_FILENAME)
    is_plugin_enabled = False
    target_panels = {}

    @classmethod
    def reload_settings(cls):
        cls.is_plugin_enabled = cls.settings.get(SETTINGS_KEYS[0])
        cls.target_panels = cls.settings.get(SETTINGS_KEYS[1])

    @classmethod
    def print_all_window_panels(cls):
        for window in sublime.windows():
            active_panel_name = window.active_panel()
            if active_panel_name:
                print("[AutoClosePanel] Found panel:", active_panel_name)

    @classmethod
    def hide_panel(cls, window):
        panel_name = (window.active_panel() or "").replace("output.", "")

        if not panel_name in cls.target_panels.keys():
            return
        active_panel = window.find_output_panel(panel_name)

        if active_panel == None:
            return
        all_text = active_panel.substr(sublime.Region(0, active_panel.size()))

        for pattern in cls.target_panels[panel_name]:
            if re.match(pattern, all_text):
                window.run_command("hide_panel", {"panel": "output." + panel_name})
                return


class AutoClosePanelCloseCommand(sublime_plugin.WindowCommand):
    def run(self):
        AutoClosePanel.hide_panel(self.window)


class AutoClosePanelPrintPanelsCommand(sublime_plugin.WindowCommand):
    def run(self):
        AutoClosePanel.print_all_window_panels()


class AutoClosePanelListener(sublime_plugin.EventListener):
    def on_pre_save_async(self, view):
        if not AutoClosePanel.is_plugin_enabled:
            return
        AutoClosePanel.hide_panel(view.window())
