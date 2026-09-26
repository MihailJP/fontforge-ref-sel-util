import fontforge


def whatRefers(glyph: fontforge.glyph) -> list[str]:
    """
    Checks which glyph in the font refers given glyph

    :param glyph: Fontforge glyph object
    :return: ``list`` of name of glyphs which refers
    :rtype: list[str]
    """
    return [g.glyphname for g in glyph.font.glyphs() if [n for n, _, _ in g.references if n == glyph.glyphname]]
