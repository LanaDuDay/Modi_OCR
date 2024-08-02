from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(img):
    """
    Preprocesses the given image to enhance its quality for better recognition.
    Steps:
    1. Convert to grayscale
    2. Enhance contrast
    3. Apply Gaussian blur filter
    4. Apply thresholding

    Args:
    img (PIL.Image.Image): The image to preprocess.

    Returns:
    PIL.Image.Image: The preprocessed image.
    """

    # Convert to grayscale
    img = img.convert('L')
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    #Apply a Gaussian blur filter
    #img = img.filter(ImageFilter.GaussianFilter(1))
    # Apply thresholding

    img = img.point(lambda p : p > 128 and 210)
    return img