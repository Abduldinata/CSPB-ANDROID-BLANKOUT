# CSPB Touch Mapper

Simple Python utility to generate `touch_addbutton` coordinates from a rectangle selection.

## What it does

1. Open an image (recommended: your target layout image, e.g. 1280x720).
2. Right-click and drag on canvas to mark button area.
3. Tool converts rectangle to normalized values (`x1 y1 x2 y2`).
4. Generates one CSPB line in this format:

```
touch_addbutton "name" "texture" "command" x1 y1 x2 y2 r g b a round
```

## Run

From workspace root:

```powershell
python tools/cspb_touch_mapper.py
```

## Optional dependency

If you want reliable TGA loading, install Pillow:

```powershell
pip install pillow
```

Without Pillow, the tool still works with Tk-supported image types (PNG/JPG/GIF/BMP).

## Notes

- Set Base Resolution to the coordinate system you target (default `1280x720`).
- If your image is exactly that resolution, output is directly aligned.
- Use `Append To Batch` then `Export Batch` to build many buttons quickly.
