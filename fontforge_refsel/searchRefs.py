from numbers import Real

import fontforge


def whatRefers(glyph: fontforge.glyph) -> list[str]:
    """
    Checks which glyph in the font refers given glyph

    :param glyph: Fontforge glyph object
    :return: ``list`` of name of glyphs which refers
    :rtype: list[str]
    """
    return [g.glyphname for g in glyph.font.glyphs() if [n for n, _, _ in g.references if n == glyph.glyphname]]


def selectWhatRefers(font: fontforge.font, moreless: Real = 0):  # type: ignore
    """
    Selects glyphs referring selected glyphs

    :param font: Fontforge font object
    :type font: fontforge.font
    :param moreless: If positive, selects relevant glyphs in addition to the current selection. \
    If negative, deselects such glyphs. If zero, forgets current selection and then selects.
    :type moreless: numbers.Real
    """
    originalSelection: list[fontforge.glyph] = list(font.selection.byGlyphs)
    referredBy = set()
    for glyph in originalSelection:
        referredBy |= set(whatRefers(glyph))
    if moreless == 0:
        font.selection.none()
    for glyph in referredBy:
        font.selection.select(('more',) if moreless >= 0 else ('less',), glyph)  # type: ignore
