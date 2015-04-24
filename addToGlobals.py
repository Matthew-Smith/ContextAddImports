import sublime
import sublime_plugin
import re

SETTINGS_FILE = "ContextAddImports.sublime-settings"

class add_to_globalCommand(sublime_plugin.TextCommand):

    def getSettings(self):
        return sublime.load_settings(SETTINGS_FILE)

    def getImportRE(self, lang):
        langSettings = self.getSettings().get(lang)
        r = '(?:' + re.escape(langSettings['begin']) + ')([$A-Za-z0-9_\\.' + langSettings['separator'] + ']*)(?:' + re.escape(langSettings['end']) + ')'
        return r

    def getContents(self):
        region = sublime.Region(0, self.view.size())
        return self.view.substr(region)

    def getImports(self, lang):
        imports = []
        contents = self.getContents()
        r = self.getImportRE(lang)
        print(r)
        matches = re.findall(r, contents, re.M)
        for m in matches:
            names = re.split(self.getSettings().get(lang)['separator'], m)
            for n in names:
                if n not in imports:
                    imports.append(n)
        return imports

    def removeImports(self, edit, lang):
        r = self.getImportRE(lang) + '\\n'
        regions = self.view.find_all(r, 0)
        for reg in reversed(regions):
            self.view.erase(edit, reg)

    def getLanguageCode(self):
        lang = self.view.settings().get('syntax')
        langs = self.getSettings().get('syntaxes')
        for key in langs:
            if key in lang:
                return langs[key]
        return None

    def run(self, edit):
        lang = self.getLanguageCode()
        settings = self.getSettings()
        langSettings = settings.get(lang)
        prepend = settings.get('addToTop')
        separator = langSettings['separator']
        begin = langSettings['begin']
        end = langSettings['end']
        output = ''
        imports = self.getImports(lang)
        sel = self.view.sel()
        for s in sel:
            word = self.view.word(s)
            actual = self.view.substr(word)
            if actual not in imports:
                if prepend:
                    imports.insert(0, actual)
                else:
                    imports.append(actual)
        if langSettings['join']:
            output = begin + separator.join(imports) + end + '\n'
        else:
            output = begin + (end + '\n' + begin).join(imports) + end + '\n'
        print(output)
        self.removeImports(edit, lang)
        self.view.insert(edit, 0, output)

    def is_enabled(self):
        lang = self.getLanguageCode()
        if lang is None:
            return False
        return True
