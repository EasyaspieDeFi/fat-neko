# Fat Neko cosmetics — art brief

Everything Fat Neko wears is one transparent PNG drawn on a shared **400 × 400** canvas.
Get that canvas right and the app handles the rest: your art scales as he grows, squashes
when he eats, and squashes again on his idle blink, all without you anchoring anything.

## The canvas

| | |
|---|---|
| Canvas size | **400 × 400**, transparent |
| Base sprite | 300 × 272, sits at **(50, 112)** inside it |
| Format | PNG, transparent background, no padding changes |

The base sprite is cropped so tight that his ears touch the top edge — there is no room
for a hat inside it. The 400 × 400 "doll" canvas is what adds the headroom.

**Start from `TEMPLATE.png`** — it is the cat already placed at the right offset. Open it,
add a layer, draw on that layer, hide the cat layer, export just your layer at 400 × 400.

`TEMPLATE_guides.png` is the same thing with the anchor lines marked.

## Anchor lines (doll coordinates)

| Line | y | Use |
|---|---|---|
| `CROWN_Y` | 135 | top of the skull, between the ears |
| `HAT_Y` | **168** | hats extend *down* to here so they overlap the forehead and ear bases |
| `EYE_CY` | 207 | eye line — eyes centred at x=186 and x=264 |
| `COLLAR_Y` | 268 | bottom of the face patch; reads as the chin, where collars sit |
| `BODY_BOT` | 383 | his feet |

Horizontal centres: **head x=210**, **body x=198**. He is drawn very slightly turned, so
the face patch sits a little right of the ear midpoint — trust the template over symmetry.

Pixel blocks in the base sprite are about **11 px**. Matching that keeps new art reading as
part of the same cat. The sprite was resampled at some point so the grid drifts by a pixel
here and there; eyeball it against the template rather than snapping to exact multiples.

## Slots and draw order

Pick one slot per garment. Draw order is fixed:

```
back  ─── drawn BEHIND the cat (capes, wings, jetpacks, auras)
          ██ THE CAT ██
body  ─── collars, scarves, jackets, bibs
head  ─── hats, crowns, headphones
face  ─── glasses, monocles, eyepatches
offhand ─ shield side, drawn at x≈74 (shields, trophies, gloves)
hand  ─── held props, drawn at x≈300 (swords, staves, instruments)
```

Only one item per slot can be worn at a time, so two hats never fight. `hand` and
`offhand` are separate slots specifically so a sword and shield can be worn together.

Held things must **overlap the body outline** — the cat has no visible paws, so anything
floating clear of the silhouette reads as detached rather than held. Anchor them around
`HELD_Y = 318` (belly height), not up beside the head.

## Replacing a placeholder

Every item currently ships a generated placeholder in `_gen/`. To replace one, drop your
PNG in **this** folder using the same filename, then run:

```bash
python3 tools/sync_cosmetics.py
```

A file here always beats the `_gen/` one of the same name. Nothing else changes — no code
edit, no manifest to hand-write. The sync script just rebuilds `art.json` by looking at
what is on disk, which the app needs because GitHub Pages can't list a directory.

`_contact_sheet.png` shows every current placeholder on the cat — useful for checking that
a new piece sits at the same scale and weight as the rest.

## Adding a brand new item

New garments need one line in the `COSMETICS` list in `index.html` (id, slot, name,
rarity, and how it unlocks). Drop the art here with a matching filename, run the sync
script, and it appears in the wardrobe.

## Style notes

The base palette, if you want to stay inside it:

| | |
|---|---|
| teal | `#90E0D0` |
| teal shadow | `#50A090` |
| white | `#F0F0F0` |
| purple | `#A080F0` |
| outline | `#000000`, roughly 5 px |

Placeholders use a hard black keyline all the way around, matching the sprite. Nothing
enforces that — it is just what currently makes them look like they belong together.
