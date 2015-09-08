# -*- coding: utf-8 -*-
__author__ = 'gulliver - Radek Simkanic'


class AnsiColors:
    COLOR_BLACK = 0
    COLOR_RED = 1
    COLOR_GREEN = 2
    COLOR_YELLOW = 3
    COLOR_BLUE = 4
    COLOR_PURPLE = 5
    COLOR_CYAN = 6
    COLOR_WHITE_GRAY = 7
    COLOR_DEFAULT = 9

    def __init__(self, ansi_formatter, color_param):
        if not isinstance(ansi_formatter, AnsiFormatter):
            raise ValueError("Type must be class AnsiFormatter!")
        self._ansi_formatter = ansi_formatter
        self._color_param = color_param
        self._color = self.COLOR_DEFAULT

    def __int__(self):
        return self._color

    def _callBack(self):
        self._ansi_formatter._createParam(
            self._color_param,
            int(self)
        )
        return self._ansi_formatter

    def black(self):
        self._color = self.COLOR_BLACK
        return self._callBack()

    def red(self):
        self._color = self.COLOR_RED
        return self._callBack()

    def green(self):
        self._color = self.COLOR_GREEN
        return self._callBack()

    def yellow(self):
        self._color = self.COLOR_YELLOW
        return self._callBack()

    def blue(self):
        self._color = self.COLOR_BLUE
        return self._callBack()

    def purple(self):
        self._color = self.COLOR_PURPLE
        return self._callBack()

    def cyan(self):
        self._color = self.COLOR_CYAN
        return self._callBack()

    def white(self):
        self._color = self.COLOR_WHITE_GRAY
        return self._callBack()

    def default(self):
        self._color = self.COLOR_DEFAULT
        return self._callBack()

class AnsiFormatter:
    _FORMAT = "<ESCAPE>[<PARAMS>m"
    _PARAMS_SEPARATOR = ";"

    ESCAPE_8 = "\033"
    ESCAPE_16 = "\x1b"
    ESCAPE_C = "\e"

    _PARAM_END = "0"
    _PARAM_BOLD = "1" # or light color
    _PARAM_FOREGROUND = "3<COLOR>"
    _PARAM_BACKGROUND = "4<COLOR>"
    _PARAM_LIGHT_FOREGROUND = "9<COLOR>"
    _PARAM_LIGHT_BACKGROUND = "10<COLOR>"
    _PARAM_UNDERLINE = "4"
    _PARAM_BLINKING = "5"
    _PARAM_SWITCH_BACKGROUND_AND_FOREGROUND = "7"
    _PARAM_INVISIBLE_TEXT = "8" # for example: password

    COLOR_BLACK = 0
    COLOR_RED = 1
    COLOR_GREEN = 2
    COLOR_YELLOW = 3
    COLOR_BLUE = 4
    COLOR_PURPLE = 5
    COLOR_CYAN = 6
    COLOR_WHITE_GRAY = 7
    COLOR_DEFAULT = 9

    def __init__(self, escape = 8):
        if escape == 8:
            self.escape = self.ESCAPE_8
        elif escape == 16:
            self.escape = self.ESCAPE_16
        elif escape == "c" or escape == "C":
            self.escape = self.ESCAPE_C
        else:
            self.escape = self.ESCAPE_8

        self._params = []
        self._params_type = []
        self._str_fragments = []

    def _isColor(self, number):
        return number >= 0 and number <= 9 and number != 8

    def _isNonparametric(self, param):
        return param in [
            self._PARAM_BOLD, self._PARAM_UNDERLINE, self._PARAM_BLINKING,
            self._PARAM_SWITCH_BACKGROUND_AND_FOREGROUND, self._PARAM_INVISIBLE_TEXT
        ]

    def _createParam(self, param, number=None):
        if self._PARAM_END in self._params_type:
            return False

        if param == self._PARAM_END:
            if len(self._params_type):
                return False
            self._params = [param]
            self._params_type = [self._PARAM_END]
        elif param in [self._PARAM_FOREGROUND, self._PARAM_LIGHT_FOREGROUND] and self._isColor(number) and self._PARAM_BACKGROUND not in self._params_type:
            param = str(param).replace("<COLOR>", str(number))
            self._params.append(param)
            self._params_type.append(self._PARAM_FOREGROUND)
        elif param in [self._PARAM_BACKGROUND, self._PARAM_LIGHT_BACKGROUND] and self._isColor(number) and self._PARAM_FOREGROUND not in self._params_type:
            param = str(param).replace("<COLOR>", str(number))
            self._params.append(param)
            self._params_type.append(self._PARAM_FOREGROUND)
        elif param == self._PARAM_INVISIBLE_TEXT and self._PARAM_FOREGROUND not in self._params_type:
            self._params.append(param)
            self._params_type.append(self._PARAM_FOREGROUND)
        elif self._isNonparametric(param) and param not in self._params_type:
            self._params.append(param)
            self._params_type.append(param)
        else:
            return False

        return True

    def __str__(self):
        return "".join(self._str_fragments)

    def get(self, get_also_empty_code = False):
        if get_also_empty_code == False and len(self._params) == 0:
            return ""
        params = self._PARAMS_SEPARATOR.join(self._params)
        code = self._FORMAT.replace("<ESCAPE>", self.escape)
        return code.replace("<PARAMS>", params)

    def reset(self):
        """
        Reset only text formats, no remove strings
        :return:
        """
        self._params = []
        self._params_type = []
        return self

    def clear(self):
        """
        Reset all.
        :return:
        """
        self._params = []
        self._params_type = []
        self._str_fragments = []
        return self

    def end(self):
        self._createParam(self._PARAM_END)
        return self

    # or/and light
    def bold(self):
        self._createParam(self._PARAM_BOLD)
        return self

    def underline(self):
        self._createParam(self._PARAM_UNDERLINE)
        return self

    # not supported?
    def blinking(self):
        self._createParam(self._PARAM_BLINKING)
        return self

    #switch background and foreground color
    def switch(self):
        self._createParam(self._PARAM_SWITCH_BACKGROUND_AND_FOREGROUND)
        return self

    def invisibleText(self):
        self._createParam(self._PARAM_INVISIBLE_TEXT)
        return self

    def lightColor(self, color = None):
        if color == None:
            return AnsiColors(self, self._PARAM_LIGHT_FOREGROUND)
        self._createParam(self._PARAM_LIGHT_FOREGROUND, color)
        return self

    def color(self, color = None):
        if color == None:
            return AnsiColors(self, self._PARAM_FOREGROUND)
        self._createParam(self._PARAM_FOREGROUND, color)
        return self

    def lightBackground(self, color = None):
        if color == None:
            return AnsiColors(self, self._PARAM_LIGHT_BACKGROUND)
        self._createParam(self._PARAM_LIGHT_BACKGROUND, color)
        return self

    def background(self, color = None):
        if color == None:
            return AnsiColors(self, self._PARAM_BACKGROUND)
        self._createParam(self._PARAM_BACKGROUND, color)
        return self

    def text(self, string):
        if len(self._params_type) == 0:
            self._str_fragments.append(string)
            return self
        if self._PARAM_END in self._params_type:
            self.reset()
            self._str_fragments.append(string)
            return self
        self._str_fragments.append(self.get())
        self._str_fragments.append(string)
        self._str_fragments.append(self.reset().end().get())
        self.reset()
        return self

    def echo(self):
        print("".join(self._str_fragments))
        self.clear()
        return self
