import fontforge
from numbers import Real


__all__ = ["glyphHasDistortedRefs", "selectGlyphsWithDistortedRefs"]


def glyphHasDistortedRefs(glyph: fontforge.glyph) -> bool:
    """
    Checks if glyph has distorted references

    While each references can have affine transformation, ttfautohint tool
    cannot deal with distorted references well.

    This function checks if given glyph has references with linear transformation
    which are scaled, rotated, skewed, or flipped.
    Parallel translations are not checked.

    :param glyph: Fontforge glyph object
    :type glyph: fontforge.glyph
    :return: ``True`` if at least one reference is distorted, ``False`` otherwise
    :rtype: bool
    """
    for ref in glyph.references:
        (srcglyph, matrix, _) = ref
        if matrix[:4] != (1, 0, 0, 1):
            return True
    return False


def selectGlyphsWithDistortedRefs(font: fontforge.font, moreless: Real = 0):
    """
    Selects glyphs with distorted references

    :param font: Fontforge font object
    :type font: fontforge.font
    :param moreless: If positive, selects relevant glyphs in addition to the current selection. \
    If negative, deselects such glyphs. If zero, forgets current selection and then selects.
    :type moreless: numbers.Real
    """
    glyphsWithDistortedRefs = set()
    for glyph in font.glyphs():
        if glyphHasDistortedRefs(glyph):
            glyphsWithDistortedRefs.add(glyph.glyphname)
    if moreless == 0:
        font.selection.none()
    for glyph in glyphsWithDistortedRefs:
        font.selection.select(('more',) if moreless >= 0 else ('less',), glyph)
