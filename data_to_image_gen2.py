import cv2
import numpy as np
import os
import time


def encryption(filename):
    # Read file content
    with open(filename, "r", encoding="utf-8") as f:
        value = f.read()

    start_time = time.time()
    print(start_time)

    # Convert characters to 8-bit binary representation
    binary_value = "".join(format(ord(x), "08b") for x in value)
    length = len(binary_value)

    # Split binary string into chunks of 32 bits
    value2 = [binary_value[i:i + 32] for i in range(0, length, 32)]

    # Pad the last chunk if necessary
    last_error=""

    if len(value2[-1])<32:
        last_error="0"*(32-len(value2[-1]))
        value2[-1] = value2[-1].ljust(32, '0')

    # Convert binary strings to integer arrays
    value2 = np.array([int(chunk, 2) for chunk in value2])

    # Prepare array for storing pixel values
    pixel_values = np.zeros((len(value2), 4), dtype=np.uint8)
    for idx, val in enumerate(value2):
        pixel_values[idx] = [(val >> (8 * i)) & 0xFF for i in reversed(range(4))]

    # Reshape the pixel values array
    sqr2 = int(np.ceil(len(pixel_values) ** 0.5))
    pixel_values.resize((sqr2, sqr2, 4))

    # Prepare file name for output image
    numeric=len(last_error)
    directory = os.path.dirname(filename)
    file_name = os.path.basename(filename)
    name, extension = os.path.splitext(file_name)
    output_path = os.path.join(directory, f'{name.replace("-", "").replace("_", "")}-{numeric}_{(sqr2 ** 2) - len(value2)}.png')

    # Write the image
    cv2.imwrite(output_path, pixel_values)

    print("End time:", time.time() - start_time)

# Call the encryption function with the file name
encryption("temp/SampleTextFile_1000kb.txt")
