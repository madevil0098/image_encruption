from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
import sys
import os
import tkinter as tk
from tkinter import filedialog
from kivy.clock import Clock
from threading import Thread
import time
import cv2
import numpy
from bitarray import bitarray
import cv2
import numpy as np
import os
# Initialize tkinter (to create the file dialog)
tk_root = tk.Tk()
tk_root.withdraw()  # Hide the main tkinter window

def get_asset_path(relative_path):
    """ Returns the correct path for assets (images) depending on whether the app is packaged or not """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.dirname(__file__), relative_path)

def encryption_tec(filename):
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


def decrypt_tec(image_filename: str) -> None:
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
    #start_time = time.time()

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

class IconButton(ButtonBehavior, Image):
    """ Custom button class with image behavior for user interaction feedback. """
    def __init__(self, **kwargs):
        super(IconButton, self).__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = False


class Encryption(BoxLayout):
    """ Layout for selecting a file from the filesystem. """
    def __init__(self, **kwargs):
        super(Encryption, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Open button to trigger file chooser
        self.open_button = Button(text='Select text file', size_hint=(1, 0.2))
        self.open_button.bind(on_press=self.show_file_chooser)
        self.add_widget(self.open_button)

        # Label to display the selected file
        self.selected_file_label = Label(text='Selected file: None', size_hint=(1, 0.2), halign='left')
        self.add_widget(self.selected_file_label)

    def show_file_chooser(self, instance):
        """ Display the native file chooser dialog. """
        selected_file = filedialog.askopenfilename(title="Select a file",filetypes=[("Text Files", "*.txt")]  )  # Show file dialog
        if selected_file:
            self.selected_file_label.text = f"Selected file: {selected_file}"
            Thread(target=self.process_file, args=(selected_file,)).start()

    def update_label(self, text):
        """ Update the label text on the main thread. """
        self.selected_file_label.text = text

    def process_file(self, file_path):
        """ Simulate processing the selected file. """
        # Update the label to indicate processing has started
        Clock.schedule_once(lambda dt: self.update_label(f"Processing {file_path}..."), 0)
        print(20)
        # Simulate a long-running process (like file reading/processing)
        encryption_tec(file_path)  # Simulate processing delay

        # Update the label after processing is complete
        Clock.schedule_once(lambda dt: self.update_label(f"Completed: {file_path}"), 0)

class Decryption(BoxLayout):
    """ Layout for selecting a file from the filesystem. """
    def __init__(self, **kwargs):
        super(Decryption, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Open button to trigger file chooser
        self.open_button = Button(text='Select png File', size_hint=(1, 0.2))
        self.open_button.bind(on_press=self.show_file_chooser)
        self.add_widget(self.open_button)

        # Label to display the selected file
        self.selected_file_label = Label(text='Selected file: None', size_hint=(1, 0.2), halign='left')
        self.add_widget(self.selected_file_label)

    def show_file_chooser(self, instance):
        """ Display the native file chooser dialog. """
        selected_file = filedialog.askopenfilename(title="Select a PNG file",
        filetypes=[("PNG Files", "*.png")] )  # Show file dialog
        if selected_file:
            self.selected_file_label.text = f"Selected file: {selected_file}"
            Thread(target=self.process_file, args=(selected_file,)).start()

    def update_label(self, text):
        """ Update the label text on the main thread. """
        self.selected_file_label.text = text

    def process_file(self, file_path):
        """ Simulate processing the selected file. """
        # Update the label to indicate processing has started
        Clock.schedule_once(lambda dt: self.update_label(f"Processing {file_path}..."), 0)

        # Simulate a long-running process (like file reading/processing)
        decrypt_tec(file_path)  # Simulate processing delay

        # Update the label after processing is complete
        Clock.schedule_once(lambda dt: self.update_label(f"Completed: {file_path}"), 0)


class BlockButton(ButtonBehavior, BoxLayout):
    def __init__(self, block_name, block_info, **kwargs):
        super(BlockButton, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.width = dp(150)
        self.height = dp(150)

        # Image of the block
        self.block_image = Image(source=block_info, size_hint=(1, 0.8), allow_stretch=True)
        self.add_widget(self.block_image)

        # Label for block name
        self.block_label = Label(text=block_name, size_hint=(1, 0.2),
                                 color=(1, 1, 1, 1), font_size=dp(16), halign="center", valign="middle")
        self.block_label.bind(size=self._update_text)
        self.add_widget(self.block_label)

    def _update_text(self, instance, size):
        self.block_label.text_size = size
class BlockSelectionScreen(Screen):
    """ Screen for selecting blocks. """
    def __init__(self, **kwargs):
        super(BlockSelectionScreen, self).__init__(**kwargs)

        # Scroll view to display block buttons
        scroll_view = ScrollView(size_hint=(1, 1))
        self.layout = GridLayout(cols=2, padding=dp(20), spacing=dp(20), size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # Adding block buttons
        self.add_block_button("Encryption", "image/3470475.png", self.go_to_encryption)
        self.add_block_button("Decryption", "image/download.jpeg", self.go_to_decryption)

        # Add layout to scroll view and scroll view to screen
        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)

    def add_block_button(self, block_name, image_path, on_press):
        """ Helper method to add a block button to the layout. """
        block_button = BlockButton(block_name, get_asset_path(image_path))
        block_button.bind(on_press=on_press)
        self.layout.add_widget(block_button)

    

    def go_to_encryption(self, *args):
        """ Transition to the encryption screen. """
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'Encryption'

    def go_to_decryption(self, *args):
        """ Transition to the decryption screen. """
        self.manager.transition = SlideTransition(direction='up')
        self.manager.current = 'Decryption'

class EncryptionScreen(Screen):
    """ Encryption screen containing file selector. """
    def __init__(self, **kwargs):
        super(EncryptionScreen, self).__init__(**kwargs)
        self.file_selector = Encryption()
        self.add_widget(self.file_selector)
        print(5)
        back_button = Button(text="Back", size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

    def go_back(self, instance):
        """ Transition back to the selection screen. """
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'selection'  # Adjust this based on your screen manager names


class DecryptionScreen(Screen):
    """ Decryption screen containing file selector. """
    def __init__(self, **kwargs):
        super(DecryptionScreen, self).__init__(**kwargs)
        self.Decryption = Decryption()
        self.add_widget(self.Decryption)
        print(4)
        back_button = Button(text="Back", size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

    def go_back(self, instance):
        """ Transition back to the selection screen. """
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'selection'  # Adjust this based on your screen manager names


class PavingApp(App):
    def build(self):
        Window.set_icon(get_asset_path('image/160KB-14_159.png'))  # Set app icon
        sm = ScreenManager()
        sm.add_widget(BlockSelectionScreen(name='selection'))
        sm.add_widget(EncryptionScreen(name='Encryption'))  # Renamed to BlockCalculatorScreen
        sm.add_widget(DecryptionScreen(name='Decryption'))  # Renamed to BlockCalculatorScreen
        
        return sm


if __name__ == '__main__':
    PavingApp().run()
