#!/usr/bin/python2.7 -tt
# -*- coding: utf-8 -*-
import os
import cssutils


def parsecss(file):
    css = cssutils.parseFile(file)
    return css


def get_selectors(file):
    css = parsecss(file)
    rules = list(css.cssRules.rulesOfType(cssutils.css.CSSRule.STYLE_RULE))
    selectors = [rule.selectorText for rule in rules]
    return selectors


def set_selectors(file, sel, dic):
    css = parsecss(file)
    selectors = get_selectors(file)
    index = selectors.index(sel)
    for key, value in dic.items():
        css.cssRules[index].style.setProperty(key, value)
    f = open(file, "w")
    f.write(css.cssText)
    f.close()
    return True
