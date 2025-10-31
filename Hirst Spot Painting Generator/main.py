import argparse
import random
from typing import Optional

from palette import extract_palette
from renderer import draw_turtle_grid, render_png


def dry_run(info):
    palette = extract_palette(info.get('image', 'hirst-painting.jpg'), info.get('palette_count', 10))
    print('Dry run:')
    print(f" rows={info['rows']}, cols={info['cols']}, dot_size={info['dot_size']}, spacing={info['spacing']}")
    print(f" background={info['bg_color']}")
    print(f" palette (first {min(10, len(palette))}): {palette[:10]}")


def main(argv: Optional[list] = None):
    parser = argparse.ArgumentParser(description='Hirst spot painting generator')
    parser.add_argument('--rows', type=int, default=10)
    parser.add_argument('--cols', type=int, default=10)
    parser.add_argument('--dot-size', type=int, default=20)
    parser.add_argument('--spacing', type=int, default=50)
    parser.add_argument('--bg-color', default='black')
    parser.add_argument('--image', default='hirst-painting.jpg')
    parser.add_argument('--no-window', action='store_true', help='Run a dry-run without opening the turtle window')
    parser.add_argument('--export', type=str, default=None, help='Export output to PNG file (headless)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for reproducible output')

    args = parser.parse_args(argv)

    if args.seed is not None:
        random.seed(args.seed)

    info = {
        'rows': args.rows,
        'cols': args.cols,
        'dot_size': args.dot_size,
        'spacing': args.spacing,
        'bg_color': args.bg_color,
        'image': args.image,
        'palette_count': 10,
    }

    if args.no_window and not args.export:
        dry_run(info)
        return

    palette = extract_palette(args.image, 10)

    # If export requested, try headless PNG render
    if args.export:
        try:
            render_png(args.export, args.rows, args.cols, args.dot_size, args.spacing, args.bg_color, palette)
            print(f'Exported PNG to: {args.export}')
        except Exception as e:
            print('Failed to export PNG:', e)
            print('You can install Pillow via: pip install pillow')
        # if no-window was requested, return after exporting
        if args.no_window:
            return

    # Otherwise open a turtle window and draw interactively
    draw_turtle_grid(args.rows, args.cols, args.dot_size, args.spacing, args.bg_color, palette)


if __name__ == '__main__':
    main()
