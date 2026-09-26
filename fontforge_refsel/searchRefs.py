from numbers import Real

import fontforge


def whatRefers(glyph: fontforge.glyph, indirect: bool = False) -> list[str]:
    """
    Checks which glyph in the font refers given glyph

    :param glyph: Fontforge glyph object
    :param indirect: Include indirect references
    :return: ``list`` of name of glyphs which refers
    :rtype: list[str]
    """
    if indirect:
        glyphs = set()
        delta = set()
        assert glyphs is not delta
        new = set(whatRefers(glyph))
        while new:
            delta = new
            glyphs |= delta
            new = set()
            for g in list(delta):
                new |= set(whatRefers(glyph.font[g]))
        return sorted(list(glyphs), key=lambda g: glyph.font[g].originalgid)
    else:
        return [g.glyphname for g in glyph.font.glyphs() if [n for n, _, _ in g.references if n == glyph.glyphname]]


def selectWhatRefers(font: fontforge.font, indirect: bool = False, moreless: Real = 0):  # type: ignore
    """
    Selects glyphs referring selected glyphs

    :param font: Fontforge font object
    :type font: fontforge.font
    :param indirect: Include indirect references
    :type indirect: bool
    :param moreless: If positive, selects relevant glyphs in addition to the current selection. \
    If negative, deselects such glyphs. If zero, forgets current selection and then selects.
    :type moreless: numbers.Real
    """
    originalSelection: list[fontforge.glyph] = list(font.selection.byGlyphs)
    referredBy = set()
    for glyph in originalSelection:
        referredBy |= set(whatRefers(glyph, indirect))
    if moreless == 0:
        font.selection.none()
    for glyph in referredBy:
        font.selection.select(('more',) if moreless >= 0 else ('less',), glyph)  # type: ignore
