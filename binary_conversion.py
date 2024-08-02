import cv2
import os

def convert_to_binary(image_path, output_path):
    """
    Converts a color image to a binary image and saves it.

    Args:
    image_path (str): The path to the input color image.
    output_path (str): The path to save the binary image.
    """
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply binary thresholding
    _, binary_image = cv2.threshold(gray_image, 170, 200, cv2.THRESH_BINARY)
    # Save the binary image
    cv2.imwrite(output_path, binary_image)

def convert_all_images_to_binary(input_folder, output_folder):
    """
    Converts all images in the input folder to binary images and saves them in the output folder.

    Args:
    input_folder (str): The folder containing the input images.
    output_folder (str): The folder to save the binary images.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            convert_to_binary(input_path, output_path)
