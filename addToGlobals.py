import sublime
import sublime_plugin

class add_to_globalCommand(sublime_plugin.TextCommand):

    def getComment():
        return '/*global */'

    def run(self, edit):
        r = self.view.sel()[0]
        word = self.view.word(r)
        actual = self.view.substr(word)
        self.view.insert(edit, 0, "/*global " + actual + "*/\n")
