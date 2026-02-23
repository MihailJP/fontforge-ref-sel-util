import fontforge
from . import (
    nestedRefs,
    distortedRefs,
)


def _selectGlyphsWithNestedRefsMenu(u, font):
    nestedRefs.selectGlyphsWithNestedRefs(font)


def _decomposeNestedRefsMenu(u, font):
    nestedRefs.decomposeNestedRefs(font)


def _selectGlyphsWithDistortedRefsMenu(u, font):
    distortedRefs.selectGlyphsWithDistortedRefs(font)


def fontforge_plugin_init(**kw):
    fontforge.registerMenuItem(
        callback=_selectGlyphsWithNestedRefsMenu,
        enable=lambda x, y: True,
        context="Font",
        submenu="_Select",
        name="Glyphs with _nested references"
    )
    fontforge.registerMenuItem(
        callback=_selectGlyphsWithDistortedRefsMenu,
        enable=lambda x, y: True,
        context="Font",
        submenu="_Select",
        name="Glyphs with _distorted references"
    )
    fontforge.registerMenuItem(
        callback=_decomposeNestedRefsMenu,
        enable=lambda x, y: True,
        context="Font",
        name="_Decompose nested references"
    )
