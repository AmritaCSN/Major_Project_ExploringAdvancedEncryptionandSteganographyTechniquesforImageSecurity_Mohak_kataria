import numpy as np
from PIL import Image

def information_entropy(image_path):
    '''
    This method caclulates entropy which gives a measure of Stegno Image,
    which gives a measure of how secure is the data - higher is better
    '''
    # Load stego image
    image = Image.open(image_path)
    pixels = np.array(image.convert('L')).ravel()

    # Calculate pixel value frequencies
    counts = np.bincount(pixels)
    frequencies = counts / float(np.sum(counts))

    # Calculate information entropy
    entropy = -np.sum([p * np.log2(p) for p in frequencies if p != 0])

    return entropy

