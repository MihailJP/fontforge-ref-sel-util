import fontforge
from . import (
    nestedRefs,
    distortedRefs,
    unreachables,
)
import sys


def _selectGlyphsWithNestedRefsMenu(u, font):
    nestedRefs.selectGlyphsWithNestedRefs(font)


def _decomposeNestedRefsMenu(u, font):
    nestedRefs.decomposeNestedRefs(font)


def _selectGlyphsWithDistortedRefsMenu(u, font):
    distortedRefs.selectGlyphsWithDistortedRefs(font)


def _selectUnusedGlyphsMenu(u, font):
    unreachables.selectUnusedGlyphs(font)


def fontforge_plugin_init(**kw):
    fontforge.registerMenuItem(
        callback=_selectGlyphsWithNestedRefsMenu,
        enable=None,
        context="Font",
        submenu="_Select",
        name="Glyphs with _nested references"
    )
    fontforge.registerMenuItem(
        callback=_selectGlyphsWithDistortedRefsMenu,
        enable=None,
        context="Font",
        submenu="_Select",
        name="Glyphs with _distorted references"
    )
    fontforge.registerMenuItem(
        callback=_selectUnusedGlyphsMenu,
        enable=None,
        context="Font",
        submenu="_Select",
        name="_Unused glyphs"
    )
    fontforge.registerMenuItem(
        callback=_decomposeNestedRefsMenu,
        enable=lambda *_: sys.version_info >= (3, 12),
        context="Font",
        name="_Decompose nested references"
    )
