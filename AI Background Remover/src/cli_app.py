import argparse
from rembg import remove

def remove_background(input_image, output_image="output.png"):
    with open(input_image, "rb") as i:
        with open(output_image, "wb") as o:
            o.write(remove(i.read()))
    print(f"✅ Background removed! Saved as {output_image}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Background Remover CLI Tool")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", default="output.png", help="Output image path")
    args = parser.parse_args()

    remove_background(args.input, args.output)
