Fontforge Utility Plugin on References and Selections
=====================================================

This plugin helps finding:

- Glyphs with nested references and flatten such references
- Glyphs with distorted references and unlink references
- Unused glyphs and remove them

Required Python version is:

- 3.9 to 3.11 for limited features
  - "Select unused glyphs" menu will be disabled in this case due to
    possible crash
- 3.12 or later for full features

Details
-------

### Glyphs with nested references

Nested references are known to cause problems in certain environments.
More information can be found at
[fontbakery issue 2961](https://github.com/fonttools/fontbakery/issues/2961)
and [arrowtype issue 412](https://github.com/arrowtype/recursive/issues/412).

### Glyphs with distorted references

While each references can have affine transformation,
[ttfautohint](https://freetype.org/ttfautohint/) tool cannot deal with
distorted references well. Unlinking such references will be needed if
you plan to use ttfautohint.

### Unused glyphs (Python ≥ 3.12 only)

When a glyph is expressed as unused or unreachable, such glyphs
neither has Unicode encodings nor is referenced from another glyph or
a GSUB table. They can be dropped to reduce the file size.

Install
-------

```shell
pip3 install fontforge-ref-sel-util
```

### Make sure Fontforge Python module is usable

In interactive mode of Python, run:

```python
import fontforge
```

If it raises ``ModuleNotFoundError`` exception, install Fontforge first. If
installed, make sure the build option set that the Python module gets also
installed. If already so, Python interpreter does not recognize the module
path where the required module.

```shell
export PYTHONPATH=/path/to/fontforge/python/module:$PYTHONPATH
```

Usage
-----

### In Fontforge GUI

This plugin adds following items into "Tools" menu:

- Select
  - Glyphs with nested references
  - Glyphs with distorted references
  - Unused glyphs
- Decompose nested references

### In Python script

```python
import fontforge
import fontforge_refsel

font = fontforge.open('path/to/font.sfd')

# Select glyphs with nested references
fontforge_refsel.selectGlyphsWithNestedRefs(font)      # set selection
fontforge_refsel.selectGlyphsWithNestedRefs(font, 0)   # set selection
fontforge_refsel.selectGlyphsWithNestedRefs(font, 1)   # append selection
fontforge_refsel.selectGlyphsWithNestedRefs(font, -1)  # deselect

# Select glyphs with distorted references
# (i.e. non-identity linearly transformed references)
fontforge_refsel.selectGlyphsWithDistortedRefs(font)      # set selection
fontforge_refsel.selectGlyphsWithDistortedRefs(font, 0)   # set selection
fontforge_refsel.selectGlyphsWithDistortedRefs(font, 1)   # append selection
fontforge_refsel.selectGlyphsWithDistortedRefs(font, -1)  # deselect

# Select unreachable glyphs
fontforge_refsel.selectUnusedGlyphs(font)      # set selection
fontforge_refsel.selectUnusedGlyphs(font, 0)   # set selection
fontforge_refsel.selectUnusedGlyphs(font, 1)   # append selection
fontforge_refsel.selectUnusedGlyphs(font, -1)  # deselect

# Check a glyph
glyph = font['foo']
result = fontforge_refsel.glyphHasNestedRefs(glyph)
result = fontforge_refsel.glyphHasDistortedRefs(glyph)
result = glyph.glyphname in fontforge_refsel.unusedGlyphs(font)

# List of glyphs with...
result = [glyph.glyphname for glyph in filter(fontforge_refsel.glyphHasNestedRefs, font.glyphs())]
result = [glyph.glyphname for glyph in filter(fontforge_refsel.glyphHasDistortedRefs, font.glyphs())]
result = list(fontforge_refsel.unusedGlyphs(font))  # unusedGlyphs() returns a frozenset object

# Decompose nested references
fontforge_refsel.decomposeNestedRefs(font)         # selected glyphs
fontforge_refsel.decomposeNestedRefs(font, False)  # selected glyphs
fontforge_refsel.decomposeNestedRefs(font, True)   # all glyphs
# if no glyphs are selected, processes all glyphs

# Unlink distorted references (Python < 3.12 may crash)
fontforge_refsel.selectGlyphsWithDistortedRefs(font)
font.unlinkReferences()
font.removeOverlap()  # may or may not needed

# Drop unused glyphs (Python < 3.12 may crash)
for glyph in fontforge_refsel.unusedGlyphs(font):
    font.removeGlyph(glyph)
```
