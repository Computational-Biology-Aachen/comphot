#!/usr/bin/env python3
# /// script
# dependencies = ["polib"]
# ///
"""
Convert .po locale files from reference/comphot/locales/ into messages/*.json.

Rules:
  - msgid is lower-cased to produce the JSON key (already snake_case in source)
  - Whether a key is split into bio_/math_ variants is decided from the EN source:
      · If 4bio-en == 4math-en → single unprefixed key in all locales
      · If 4bio-en != 4math-en → bio_<key> and math_<key> in all locales
    This keeps the key schema consistent across languages.
  - Leading markdown heading markers (# / ## / ### …) are stripped from values
  - Empty msgstr entries fall back to the EN value so all primary locales
    end up with the same key set (required by Paraglide)
  - Output JSON files are sorted by key for stable diffs

Validation:
  - Primary locales (en, de, fr) must have identical key sets → hard error
  - Secondary locales (es, pl) are partially translated → warning only

Usage (from repo root):
    uv run utils/po_to_json.py
"""

import json
import re
import sys
import tempfile
from pathlib import Path

import polib  # type: ignore[import-untyped]

REPO_ROOT = Path(__file__).parent.parent
LOCALES_DIR = REPO_ROOT / "reference" / "comphot" / "locales"
MESSAGES_DIR = REPO_ROOT / "messages"

AUDIENCES: dict[str, str] = {"4bio": "bio", "4math": "math"}
PRIMARY_LOCALES = ["en", "de", "fr"]
SECONDARY_LOCALES: list[str] = []
ALL_LOCALES = PRIMARY_LOCALES + SECONDARY_LOCALES


# -- Helpers --------------------------------------------------------------------


def strip_heading_markers(text: str) -> str:
    """Remove leading markdown heading markers.

    '## Model construction' → 'Model construction'
    '### Guiding Questions' → 'Guiding Questions'
    """
    return re.sub(r"^#+\s*", "", text).strip()


def normalize_po_content(content: str) -> str:
    """Join non-standard backslash-continued lines found in some source .po files.

    'long value \\\n        continued' → 'long value continued'
    """
    lines = content.splitlines(keepends=True)
    result: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        while re.search(r"\\\s*\n$", line):
            line = re.sub(r"\\\s*\n$", " ", line)
            i += 1
            if i < len(lines):
                line = line.rstrip(" ") + lines[i].lstrip()
        result.append(line)
        i += 1
    return "".join(result)


def parse_po(path: Path) -> dict[str, str]:
    """Return {msgid: msgstr} for all non-empty entries, normalising line continuations."""
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    normalized = normalize_po_content(raw)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".po", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(normalized)
        tmp_path = tmp.name
    try:
        po = polib.pofile(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)
    return {entry.msgid: entry.msgstr for entry in po if entry.msgid and entry.msgstr}


def load_audience_translations(locale: str) -> tuple[dict[str, str], dict[str, str]]:
    """Return (bio_translations, math_translations) for a locale."""
    bio_path = LOCALES_DIR / "4bio" / locale / "LC_MESSAGES" / "main.po"
    math_path = LOCALES_DIR / "4math" / locale / "LC_MESSAGES" / "main.po"
    bio = {k: strip_heading_markers(v) for k, v in parse_po(bio_path).items()}
    math = {k: strip_heading_markers(v) for k, v in parse_po(math_path).items()}
    return bio, math


# -- Core logic -----------------------------------------------------------------


def compute_split_schema(
    en_bio: dict[str, str], en_math: dict[str, str]
) -> tuple[set[str], set[str]]:
    """Classify every msgid as 'shared' or 'split' based on EN values.

    shared: bio value == math value → single unprefixed key
    split:  bio value != math value → bio_<key> and math_<key>
    """
    all_msgids = set(en_bio) | set(en_math)
    shared: set[str] = set()
    split: set[str] = set()
    for msgid in all_msgids:
        b = en_bio.get(msgid, "")
        m = en_math.get(msgid, "")
        if b == m:
            shared.add(msgid)
        else:
            split.add(msgid)
    return shared, split


def build_locale_json(
    locale: str,
    shared_msgids: set[str],
    split_msgids: set[str],
    en_bio: dict[str, str],
    en_math: dict[str, str],
) -> dict[str, str]:
    """Build the JSON dict for one locale using the EN-derived split schema.

    Missing translations fall back to the EN value so the key set stays uniform
    across all primary locales.
    """
    bio, math = load_audience_translations(locale)
    result: dict[str, str] = {}

    for msgid in sorted(shared_msgids | split_msgids, key=str.lower):
        snake_key = msgid.lower()

        if msgid in shared_msgids:
            # Single unprefixed key; bio and math have the same content in EN
            val = bio.get(msgid) or math.get(msgid) or en_bio.get(msgid, "")
            if val:
                result[snake_key] = val

        else:  # split key
            bio_val = bio.get(msgid) or en_bio.get(msgid, "")
            math_val = math.get(msgid) or en_math.get(msgid, "")
            if bio_val:
                result[f"bio_{snake_key}"] = bio_val
            if math_val:
                result[f"math_{snake_key}"] = math_val

    return result


def build_secondary_locale_json(
    locale: str,
    shared_msgids: set[str],
    split_msgids: set[str],
) -> dict[str, str]:
    """Build JSON for a partially-translated secondary locale.

    No EN fallback — only include keys that actually have translations.
    """
    bio, math = load_audience_translations(locale)
    result: dict[str, str] = {}

    for msgid in sorted(shared_msgids | split_msgids, key=str.lower):
        snake_key = msgid.lower()

        if msgid in shared_msgids:
            val = bio.get(msgid) or math.get(msgid) or ""
            if val:
                result[snake_key] = val
        else:
            bio_val = bio.get(msgid, "")
            math_val = math.get(msgid, "")
            if bio_val:
                result[f"bio_{snake_key}"] = bio_val
            if math_val:
                result[f"math_{snake_key}"] = math_val

    return result


# -- Main -----------------------------------------------------------------------


def main() -> int:
    print("Loading EN source to derive split schema...")
    en_bio, en_math = load_audience_translations("en")
    shared_msgids, split_msgids = compute_split_schema(en_bio, en_math)
    print(
        f"  {len(shared_msgids)} shared keys, "
        f"{len(split_msgids)} split keys "
        f"(→ {len(shared_msgids) + 2 * len(split_msgids)} total JSON keys)\n"
    )

    results: dict[str, dict[str, str]] = {}

    for locale in PRIMARY_LOCALES:
        print(f"Processing {locale}...", end=" ")
        results[locale] = build_locale_json(
            locale, shared_msgids, split_msgids, en_bio, en_math
        )
        print(f"{len(results[locale])} keys")

    for locale in SECONDARY_LOCALES:
        print(f"Processing {locale} (secondary)...", end=" ")
        results[locale] = build_secondary_locale_json(
            locale, shared_msgids, split_msgids
        )
        print(f"{len(results[locale])} keys (partial)")

    # -- Validate ---------------------------------------------------------------
    print()
    ok = True
    ref_keys = set(results["en"])

    print("Validating primary locales (en, de, fr):")
    for locale in PRIMARY_LOCALES:
        locale_keys = set(results[locale])
        missing = ref_keys - locale_keys
        extra = locale_keys - ref_keys
        if missing or extra:
            print(f"  ✗ {locale}: {len(missing)} missing, {len(extra)} extra")
            for k in sorted(missing)[:5]:
                print(f"      missing: {k!r}")
            for k in sorted(extra)[:5]:
                print(f"      extra:   {k!r}")
            ok = False
        else:
            print(f"  ✓ {locale}: {len(locale_keys)} keys match en")

    print("Validating secondary locales (es, pl) — warnings only:")
    for locale in SECONDARY_LOCALES:
        locale_keys = set(results[locale])
        untranslated = ref_keys - locale_keys
        extra = locale_keys - ref_keys
        status = "~" if untranslated or extra else "✓"
        note = f"{len(untranslated)} untranslated" if untranslated else "complete"
        if extra:
            note += f", {len(extra)} extra"
        print(f"  {status} {locale}: {note}")

    if not ok:
        print("\n✗ Primary locale key mismatch — aborting without writing files.")
        return 1

    # -- Write JSON -------------------------------------------------------------
    print()
    for locale, data in results.items():
        out_path = MESSAGES_DIR / f"{locale}.json"
        out_path.write_text(
            json.dumps(data, ensure_ascii=False, indent="\t") + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {out_path.relative_to(REPO_ROOT)}  ({len(data)} keys)")

    print("\n✓ Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
