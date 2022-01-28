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
SETTINGS_KEYS = ["enabled", "target_panels"]
ON_CHANGE_TAG = "reload_settings"

def plugin_loaded():
    AutoClosePanel.settings = sublime.load_settings(SETTINGS_FILENAME)
    AutoClosePanel.reload_settings()
    AutoClosePanel.settings.add_on_change(ON_CHANGE_TAG, AutoClosePanel.reload_settings)

def plugin_unloaded():
    AutoClosePanel.settings.clear_on_change(ON_CHANGE_TAG)

class AutoClosePanel():
    settings = sublime.load_settings(SETTINGS_FILENAME)
    is_plugin_enabled = False
    target_panels = {}

    @staticmethod
    def reload_settings():
        AutoClosePanel.is_plugin_enabled = AutoClosePanel.settings.get(SETTINGS_KEYS[0])
        AutoClosePanel.target_panels = AutoClosePanel.settings.get(SETTINGS_KEYS[1])

    @staticmethod
    def print_all_window_panels():
        for window in sublime.windows():
            active_panel_name = window.active_panel()
            if active_panel_name:
                print("[AutoClosePanel] Found panel:", active_panel_name)

    @staticmethod
    def hide_panel(window):
        if not AutoClosePanel.is_plugin_enabled: return
        panel_name = (window.active_panel() or "").replace("output.", "")

        if not panel_name in AutoClosePanel.target_panels.keys(): return
        active_panel = window.find_output_panel(panel_name)

        if active_panel == None: return
        all_text = active_panel.substr(sublime.Region(0, active_panel.size()))

        for pattern in AutoClosePanel.target_panels[panel_name]:
            if re.match(pattern, all_text):
                window.run_command("hide_panel", { "panel": "output." + panel_name })
                return

class AutoClosePanelCloseCommand(sublime_plugin.WindowCommand):
    def run(self):
        AutoClosePanel.hide_panel(self.window)

class AutoClosePanelPrintPanelsCommand(sublime_plugin.WindowCommand):
    def run(self):
        AutoClosePanel.print_all_window_panels()

class AutoClosePanelListener(sublime_plugin.EventListener):
    def on_pre_save_async(self, view):
        AutoClosePanel.hide_panel(view.window())
