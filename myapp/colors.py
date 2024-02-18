import cv2
import numpy as np

def identify_colors(image_path, num_colors=3):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to a 2D array of pixels
    pixels = image_rgb.reshape((-1, 3))

    # Calculate the histogram
    print(pixels.shape)

    histogram = cv2.calcHist([pixels], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

    # Normalize the histogram
    histogram = histogram / histogram.sum()

    # Get the dominant colors based on the histogram
    dominant_colors = []
    for i in range(num_colors):
        max_index = np.unravel_index(histogram.argmax(), histogram.shape)
        color = [int(max_index[j] * 32 + 16) for j in range(3)]
        dominant_colors.append(color)
        histogram[max_index] = 0

    return dominant_colors

# Example usage
image_path = 'C:/Users/Darshan/FashionStylist/myapp/media/itemimages/t1f_oKmfMbg.jpg'
num_colors = 5
dominant_colors = identify_colors(image_path, num_colors)

print("Dominant Colors:")
for color in dominant_colors:
    print(f"RGB: {color}")





