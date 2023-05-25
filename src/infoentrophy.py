import numpy as np
from PIL import Image

def information_entropy(image_path):
    # Load stego image
    image = Image.open(image_path)
    pixels = np.array(image.convert('L')).ravel()

    # Calculate pixel value frequencies
    counts = np.bincount(pixels)
    frequencies = counts / float(np.sum(counts))

    # Calculate information entropy
    entropy = -np.sum([p * np.log2(p) for p in frequencies if p != 0])

    return entropy

