import sys

import fontforge

from . import (
    nestedRefs,
    distortedRefs,
    unreachables,
)
from .translation import tr, setTranslation


def _selectGlyphsWithNestedRefsMenu(u, font):
    nestedRefs.selectGlyphsWithNestedRefs(font)


def _decomposeNestedRefsMenu(u, font):
    nestedRefs.decomposeNestedRefs(font)


def _selectGlyphsWithDistortedRefsMenu(u, font):
    distortedRefs.selectGlyphsWithDistortedRefs(font)


def _selectUnusedGlyphsMenu(u, font):
    unreachables.selectUnusedGlyphs(font)


def fontforge_plugin_init(**kw):
    setTranslation()
    fontforge.registerMenuItem(
        callback=_selectGlyphsWithNestedRefsMenu,
        enable=None,
        context="Font",
        submenu=tr.get("_Select"),
        name=tr.get("Glyphs with _nested references"),
    )
    fontforge.registerMenuItem(
        callback=_selectGlyphsWithDistortedRefsMenu,
        enable=None,
        context="Font",
        submenu=tr.get("_Select"),
        name=tr.get("Glyphs with _distorted references"),
    )
    fontforge.registerMenuItem(
        callback=_selectUnusedGlyphsMenu,
        enable=None,
        context="Font",
        submenu=tr.get("_Select"),
        name=tr.get("_Unused glyphs"),
    )
    fontforge.registerMenuItem(
        callback=_decomposeNestedRefsMenu,
        enable=lambda *_: sys.version_info >= (3, 12),
        context="Font",
        name=tr.get("_Decompose nested references"),
    )
