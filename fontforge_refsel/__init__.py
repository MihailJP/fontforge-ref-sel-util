"""Fontforge Utility Plugin on References and Selections

This plugin helps finding:

- Glyphs with nested references and flatten such references
- Glyphs with distorted references and unlink references
- Unused glyphs and remove them (Python 3.12+)"""

from .distortedRefs import glyphHasDistortedRefs, selectGlyphsWithDistortedRefs
from .nestedRefs import glyphHasNestedRefs, selectGlyphsWithNestedRefs, decomposeNestedRefs
from .unreachables import unusedGlyphs, selectUnusedGlyphs

__all__ = [
    # distortedRefs
    "glyphHasDistortedRefs",
    "selectGlyphsWithDistortedRefs",

    # nestedRefs
    "glyphHasNestedRefs",
    "selectGlyphsWithNestedRefs",
    "decomposeNestedRefs",

    # unreachables
    "unusedGlyphs",
    "selectUnusedGlyphs",
]
