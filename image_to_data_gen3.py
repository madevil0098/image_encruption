import cv2
from bitarray import bitarray
import numpy as np
import time
import os

def decrypt(image_filename: str) -> None:
    # Load the image
    image_data = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)
    if image_data is None:
        print(f"Error: Unable to load image '{image_filename}'")
        return

    # Extract numeric values from filename
    try:
        num = int(image_filename.split("_")[1].split(".")[0])
        num2 = int(image_filename.split("-")[1].split("_")[0])
    except (IndexError, ValueError) as e:
        print(f"Error extracting numbers from filename: {e}")
        return

    # Start timing
    start_time = time.time()
    print(start_time)
    def pixel_to_binary(image_array: np.ndarray, numeric: int) -> list[str]:
        temp = len(image_array)
        #print(f"Image shape: {image_array.shape}, Total pixels: {image_array.size}")
        
        # Reshape and trim the array
        image_array.resize((temp * temp, 4))
        image_array = image_array[:len(image_array) - numeric]

        # Prepare a list to hold binary representations
        binary_values = []

        # Process each pixel to convert to binary
        for ind in range(len(image_array)):
            pixel_values = image_array[ind].astype(int)  # Ensure pixel values are integers
            total = sum(pixel_values[i] * (256 ** (3 - i)) for i in range(len(pixel_values)))  # Use 3 - i for correct order
            
            # Convert total to binary and pad with zeros
            binary_string = bin(total)[2:].zfill(32)
            binary_values.append(binary_string)

        return binary_values

    def binary_to_string(binary_list: list[str], trim_count: int) -> str:
        # Join the binary strings and trim excess characters
        binary_data = "".join(binary_list)[:-trim_count]
        
        # Convert binary string to bytes
        bit_array = bitarray(binary_data)
        try:
            return bit_array.tobytes().decode("utf-8")
        except Exception as e:
            print(f"Error decoding bytes: {e}")
            return ""

    # Convert pixel data to binary
    binary_data = pixel_to_binary(image_data, num)

    # Convert binary data back to string
    output_string = binary_to_string(binary_data, num2)

    # Prepare the output file path
    directory = os.path.dirname(image_filename)
    base_name = os.path.splitext(os.path.basename(image_filename))[0]
    output_path = os.path.join(directory, f"{base_name.split('-')[0]}.txt")

    # Write the output string to a text file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_string)

    # Print the elapsed time
    print("End time:", time.time() - start_time)

# Example usage
decrypt("temp/SampleTextFile1000kb-8_6.png")
