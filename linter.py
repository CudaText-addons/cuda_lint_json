import json
import os
import re

from cuda_lint import Linter


class JSON(Linter):
    """Provides an interface to json.loads()."""

    syntax = 'JSON'
    cmd = None
    loose_regex = re.compile(
        r'^.+: (?P<message>.+) in \(data\):(?P<line>\d+):(?P<col>\d+)')
    strict_regex = re.compile(
        r'^(?P<message>.+):\s*line (?P<line>\d+) column (?P<col>\d+)')
    regex = loose_regex
    defaults = {
        'strict': True
    }
    extensions = [
        '.sublime-build',
        '.sublime-commands',
        '.sublime-completions',
        '.sublime-keymap',
        '.sublime-menu',
        '.sublime_metrics',
        '.sublime-mousemap',
        '.sublime-project',
        '.sublime_session',
        '.sublime-settings',
        '.sublime-theme',
        '.sublime-workspace',
    ]

    def run(self, cmd, code):
        # Use ST's loose parser for its setting files.
        strict = os.path.splitext(self.filename)[1] not in self.extensions

        try:
            if strict:
                self.__class__.regex = self.strict_regex
                json.loads(code)
            else:
                self.__class__.regex = self.loose_regex
                # sublime.decode_value(code)
            return ''
        except ValueError as err:
            return str(err)
