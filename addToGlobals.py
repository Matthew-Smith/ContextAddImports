import sublime, sublime_plugin

class add_to_gplobalCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "/*global */\n")
