#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'gulliver - Radek Simkanic'

from ansi_formater import *

def ansiDemoFormatter():
    print AnsiFormatter().lightColor().red().get() + "holy world" + AnsiFormatter().end().get() +\
          AnsiFormatter().background().blue().color().yellow().get() + "Hello World" + AnsiFormatter().end().get()

    af = AnsiFormatter()
    af.bold().color(AnsiFormatter.COLOR_GREEN)
    print af.get() + "Test" + af.reset().end().get()

    print AnsiFormatter().bold().background().red().color().white().get() + "Test 2" + AnsiFormatter().end().get()

    print AnsiFormatter().bold().background(AnsiFormatter.COLOR_RED).color(3).get() + "Test 3" + AnsiFormatter().end().get()

    AnsiFormatter().text("classic text")\
        .bold().text("bold text")\
        .bold().color().red().text("bold and red text")\
        .color().green().text("green text")\
        .echo()\
        .text("again classic text").switch().text("inverted text")\
        .echo()

    af.clear()
    af.background().red().color().white().bold().text("Hi")
    af.echo()
    af.background().green()
    af.color().yellow()
    af.text("iH")
    af.echo()


if __name__ == "__main__":
    ansiDemoFormatter()
