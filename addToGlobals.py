import sublime
import sublime_plugin

class add_to_globalCommand(sublime_plugin.TextCommand):

    def getComment():
        return '/*global */'

    def run(self, edit):
        self.view.insert(edit, 0, "/*global */")
