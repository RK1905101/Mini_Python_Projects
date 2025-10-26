import numpy as np
from PIL import Image

def load_image(path: str) -> np.ndarray:
    """
    Load an image from disk and convert it into a NumPy array (H, W, 3).
    
    Args:
        path (str): Path to the image file (.jpg/.png).
    Returns:
        np.ndarray: Image as NumPy array of dtype uint8.
    Raises:
        FileNotFoundError: If the image path is invalid.
        ValueError: If the file is not a supported image.
    """
    try:
        img = Image.open(path).convert("RGB")
    except FileNotFoundError:
        raise FileNotFoundError(f"Image not found: {path}")
    except OSError:
        raise ValueError(f"Unsupported or corrupt image file: {path}")
    return np.array(img, dtype=np.uint8)

def inspect_image(arr: np.ndarray, sample_size: int = 5, start: tuple = (0, 0)):
    """
    Inspect shape and a small block of pixels.
    
    Args:
        arr (np.ndarray): Image array.
        sample_size (int): Size of block to print.
        start (tuple): (row, col) start position.
    """
    row, col = start
    print("Image shape:", arr.shape)
    print(f"{sample_size}x{sample_size} block from {start}:")
    print(arr[row:row+sample_size, col:col+sample_size])