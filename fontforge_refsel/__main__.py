import sys

import fontforge

from . import (
    nestedRefs,
    distortedRefs,
    unreachables,
    searchRefs,
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


def _selectWhatRefers(u, font):
    searchRefs.selectWhatRefers(font, u)


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
        callback=_selectWhatRefers,
        enable=None,
        data=False,
        context="Font",
        submenu=[tr.get("_Select"), tr.get("Glyphs _referring currently selected glyphs")],
        name=tr.get("_Direct refs only"),
    )
    fontforge.registerMenuItem(
        callback=_selectWhatRefers,
        enable=None,
        data=True,
        context="Font",
        submenu=[tr.get("_Select"), tr.get("Glyphs _referring currently selected glyphs")],
        name=tr.get("_Including indirect refs"),
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
