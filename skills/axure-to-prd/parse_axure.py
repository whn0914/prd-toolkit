#!/usr/bin/env python3
"""
parse_axure.py — Extract human-readable text from Axure RP source files.

Axure .rp files use a proprietary binary format (magic: ac ef 09 00).
Content blocks are compressed with raw DEFLATE (gzip framing, wbits=-15).

Usage:
    python3 parse_axure.py <file.rp>

Output: JSON with keys:
    - pages:   list of { name, text_content }
    - sitemap: top-level page/folder names
    - notes:   all annotation and note strings
"""

import sys
import zlib
import re
import json

GZIP_MAGIC = b'\x1f\x8b\x08'
GZIP_HEADER_LEN = 10  # fixed header size when flags=0x00


def find_gzip_positions(data: bytes) -> list[int]:
    positions = []
    i = 0
    while i < len(data) - 3:
        if data[i:i+3] == GZIP_MAGIC:
            positions.append(i)
            i += 3
        else:
            i += 1
    return positions


def decompress_block(data: bytes, pos: int) -> bytes | None:
    deflate_start = pos + GZIP_HEADER_LEN
    try:
        return zlib.decompress(data[deflate_start:], -15)
    except zlib.error:
        return None


def extract_strings(raw: bytes) -> list[str]:
    """Extract meaningful strings from a decompressed binary block."""
    text = raw.decode('utf-8', errors='replace')
    # Match sequences containing Chinese characters or multi-word Latin text
    pattern = re.compile(
        r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]'   # Chinese
        r'[^\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]{0,200}|'
        r'[A-Za-z\u4e00-\u9fff][^\x00-\x1f\x7f]{3,120}'
    )
    results = []
    seen = set()
    for m in pattern.finditer(text):
        s = m.group().strip()
        # Skip pure noise: only digits/symbols, font names, hex strings
        if not s or len(s) < 2:
            continue
        if re.fullmatch(r'[a-f0-9\-]{8,}', s):
            continue
        if s in seen:
            continue
        seen.add(s)
        results.append(s)
    return results


# Strings that are structural Axure metadata, not content
_AXURE_NOISE = {
    'Axure:Page', 'Axure:Diagram', 'Axure:DiagramObject', 'Axure:Style',
    'Axure:DesignDocument', 'AdaptiveViewSet', 'StyleCache', 'LibraryName',
    'Default', 'fill-type', 'solid', 'fill-color', 'OffsetX', 'OffsetY',
    'BlurRadius', 'Spread', 'HorizontalAlignment', 'VerticalAlignment',
    'ColorSaturation', 'ColorBrightness', 'IndentLevel', 'ListType',
    'TypefaceToFullName', 'TypefaceToCssName', 'PingFang SC', 'Arial',
    'Helvetica', 'Regular', 'Italic', 'Bold', 'Semibold', 'Ultralight',
    'Stretch', 'diagram-objects', 'name-block', 'text-block', 'IsContained',
    'IsLocked', 'SelectedStyleGroup', 'SubmitButton', 'AutoFitHeight',
    'HackLegacyContainedObjects', 'ruler-guide-set', 'AnnLinkList',
    'GroupsClean', 'diagram-object-id', 'parent-diagram-id',
    'property-dictionary', 'VisibleFromSettings', 'PreserveCornersRectangle',
    'fit-to-image', 'Width', 'Height', 'Start', 'End', 'Hash',
    'Paragraph', 'Table Cell', 'Connector', 'Image', 'Label',
}

_NOISE_PREFIXES = (
    "'Arial", "'PingFang", "'Helvetica", 'PingFang SC',
    'Arial Bold', 'Arial Italic', 'Helvetica Bold', 'Helvetica Light',
)

_SKIP_PATTERN = re.compile(
    r'^[a-zA-Z0-9_\-\.]{1,6}$|'        # very short identifiers
    r'^[A-Z][a-z]+[A-Z]|'               # CamelCase XML tags
    r'^\d+$|'                           # pure numbers
    r'%&|JFIF|EXIF'                     # binary artefacts
)


def is_content(s: str) -> bool:
    if s in _AXURE_NOISE:
        return False
    if any(s.startswith(p) for p in _NOISE_PREFIXES):
        return False
    if _SKIP_PATTERN.search(s):
        return False
    # Must have at least one Chinese char or be a multi-word sentence
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in s)
    has_words = len(s.split()) >= 3 or (len(s) > 8 and ' ' in s)
    return has_chinese or has_words


def classify_blocks(blocks: list[tuple[int, list[str]]]) -> dict:
    """
    Classify extracted strings into sitemap names, page content, and notes.
    Heuristic: the DesignDocument block (largest, contains 废纸篓/sitemap)
    is metadata; page blocks contain interaction/label text.
    """
    sitemap = []
    pages = []
    notes = []

    for _pos, strings in blocks:
        content_strings = [s for s in strings if is_content(s)]
        if not content_strings:
            continue

        # DesignDocument block: contains sitemap-level names
        if any('废纸篓' in s or 'PMS' in s or '美宿' in s for s in content_strings):
            sitemap.extend(content_strings)
        else:
            # Page block: separate inline notes (longer, paragraph-like)
            short = [s for s in content_strings if len(s) <= 30]
            long_ = [s for s in content_strings if len(s) > 30]
            pages.append({
                'labels': short,
                'notes': long_,
            })
            notes.extend(long_)

    return {
        'sitemap': list(dict.fromkeys(sitemap)),
        'pages': pages,
        'notes': list(dict.fromkeys(notes)),
    }


def parse(path: str) -> dict:
    with open(path, 'rb') as f:
        data = f.read()

    positions = find_gzip_positions(data)
    blocks = []
    for pos in positions:
        raw = decompress_block(data, pos)
        if raw and len(raw) > 500:
            strings = extract_strings(raw)
            blocks.append((pos, strings))

    return classify_blocks(blocks)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 parse_axure.py <file.rp>', file=sys.stderr)
        sys.exit(1)
    result = parse(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
