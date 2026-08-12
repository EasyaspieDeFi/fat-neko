#!/usr/bin/env python3
"""Rebuild assets/cosmetics/art.json from what's actually on disk.

Run this after adding or replacing cosmetic art:

    python3 tools/sync_cosmetics.py

A hand-drawn assets/cosmetics/<id>.png always wins over the generated
assets/cosmetics/_gen/<id>.png of the same name. The app reads the resulting
art.json instead of probing both paths, which is what keeps the console clean.

The site is static (GitHub Pages), so there is no directory listing at runtime —
this manifest is how the browser learns which art exists.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
COS = os.path.normpath(os.path.join(HERE, "..", "assets", "cosmetics"))
GEN = os.path.join(COS, "_gen")
def is_garment(stem):
    """Working files share the folder with the art: reference sprite, contact sheet,
    author templates. Anything underscore-prefixed or TEMPLATE* is not a garment."""
    return not stem.startswith("_") and not stem.startswith("TEMPLATE")


def pngs(d):
    if not os.path.isdir(d):
        return {}
    return {f[:-4]: f for f in sorted(os.listdir(d))
            if f.endswith(".png") and is_garment(f[:-4])}


def main():
    gen, hand = pngs(GEN), pngs(COS)
    art = {i: "_gen/" + f for i, f in gen.items()}
    art.update({i: f for i, f in hand.items()})          # hand-drawn overrides generated

    out = os.path.join(COS, "art.json")
    with open(out, "w") as f:
        json.dump(art, f, indent=1, sort_keys=True)
        f.write("\n")

    overridden = sorted(set(hand) & set(gen))
    only_hand = sorted(set(hand) - set(gen))
    print(f"art.json: {len(art)} items ({len(gen)} placeholder, {len(hand)} hand-drawn)")
    if overridden:
        print("  overriding placeholders: " + ", ".join(overridden))
    if only_hand:
        print("  hand-drawn only: " + ", ".join(only_hand))


if __name__ == "__main__":
    main()
