import sublime
import sublime_plugin

SETTINGS_FILE = "addToGlobals.sublime-settings"
GLOBAL_PREFERENCES = "Preferences.sublime-settings"

class Settings:
    """Interface for communicating with settings"""
    plugin = None
    def load():
        """Loads the settings for the plugin"""
        Settings.plugin = sublime.load_settings(SETTINGS_FILE)

    def get(name, type=None, default=None):
        """Gets a value from the plugin settings"""
        if not Settings.plugin:
            Settings.load()
        if type is not None:
            return Settings.plugin.get(type, {}).get(name, default)
        return Settings.plugin.get(name, default)

def get(name, svn_type=None, default=None):
    """Gets a value from settings"""
    return Settings.get(name, svn_type, default)
