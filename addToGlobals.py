import sublime
import sublime_plugin
import re

reNewline = r'\r|\n'
reGlobals = r'(?:\/*global )([^*]*)(?:\*\/)'
reGlobalSplit = r',\s*'

class add_to_globalCommand(sublime_plugin.TextCommand):

    def getContents(self):
        region = sublime.Region(0, self.view.size())
        return self.view.substr(region)

    def getImports(self):
        imports = []
        contents = re.sub(reNewline, '', self.getContents())
        matches = re.findall(reGlobals, contents)
        for m in matches:
            print(m)
            names = re.split(reGlobalSplit, m)
            for n in names:
                if n not in imports:
                    imports.append(n)
        return imports

    def run(self, edit):
        imports = self.getImports()
        sel = self.view.sel()
        for s in sel:
            word = self.view.word(s)
            actual = self.view.substr(word)
            if actual not in imports:
                self.view.insert(edit, 0, "/*global " + actual + "*/\n")
                imports.append(actual)
