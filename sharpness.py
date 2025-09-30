import cv2
import numpy as np

def compute_sharpness(image, block_size=50, threshold=100):

    h, w = image.shape
    sharpness_map = np.zeros((h // block_size, w // block_size), dtype=int)

    # Apply Laplacian
    laplacian = cv2.Laplacian(image, cv2.CV_64F, ksize=1) 
    
    for i in range(0, h - block_size, block_size):
        for j in range(0, w - block_size, block_size):
            block = laplacian[i:i+block_size, j:j+block_size]
            variance = block.var()
            if variance > threshold: # Variance threshold
                sharpness_map[i // block_size, j // block_size] = 1
            else:
                sharpness_map[i // block_size, j // block_size] = 0
    return sharpness_map

def apply_sharpness_overlay(image, sharpness_map, block_size=50):

    color_overlay = np.zeros_like(image, dtype=np.uint8)
    
    for i in range(sharpness_map.shape[0]):
        for j in range(sharpness_map.shape[1]):
            if sharpness_map[i, j] == 1:
                color = np.array([0, 255, 0]) # Green
            else:
                color = np.array([0, 0, 255]) # Red
            x = j * block_size
            y = i * block_size
            color_overlay[y:y+block_size, x:x+block_size] = color
    # Merge overlay with the original image
    result = cv2.addWeighted(image, 0.6, color_overlay, 0.5, 0)
    return result

# Load image
image_name = "FirstFocusPlane.jpg"
#image_name = "BestFocusPlane.jpg"
#image_name = "LastFocusPlane.jpg"

image_path = "./Images/" + image_name
result_path = "./Results/" + image_name

image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Compute sharpness matrix
block_size = 10 # Block size
threshold = 50 # Sharpness threshold
sharpness_map = compute_sharpness(gray, block_size, threshold)

# Apply overlay
result = apply_sharpness_overlay(image, sharpness_map, block_size)

# Save result
cv2.imwrite(result_path, result)

# Display result
cv2.imshow("Image sharpness", result)
cv2.waitKey(0)
cv2.destroyAllWindows()