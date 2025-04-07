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

# Initialize tkinter (to create the file dialog)
tk_root = tk.Tk()
tk_root.withdraw()  # Hide the main tkinter window

def get_asset_path(relative_path):
    """ Returns the correct path for assets (images) depending on whether the app is packaged or not """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.dirname(__file__), relative_path)

class FileSelector(BoxLayout):
    """ Layout for selecting a file from the filesystem. """
    def __init__(self, title, file_types, **kwargs):
        super(FileSelector, self).__init__(**kwargs)
        self.orientation = 'vertical'
        print(title)
        # Open button to trigger file chooser
        self.open_button = Button(text=f'Select {title} file', size_hint=(1, 0.2))
        self.open_button.bind(on_press=lambda x: self.show_file_chooser(file_types))
        self.add_widget(self.open_button)

        # Label to display the selected file
        self.selected_file_label = Label(text='Selected file: None', size_hint=(1, 0.2), halign='left')
        self.add_widget(self.selected_file_label)

    def show_file_chooser(self, file_types):
        """ Display the native file chooser dialog. """
        selected_file = filedialog.askopenfilename(title="Select a file", filetypes=file_types)  # Show file dialog
        if selected_file:
            self.selected_file_label.text = f"Selected file: {selected_file}"
            Thread(target=self.process_file, args=(selected_file,)).start()

    def update_label(self, text):
        """ Update the label text on the main thread. """
        Clock.schedule_once(lambda dt: setattr(self.selected_file_label, 'text', text))

    def process_file(self, file_path):
        """ Simulate processing the selected file. """
        self.update_label(f"Processing {file_path}...")
        time.sleep(5)  # Simulate processing delay
        self.update_label(f"Completed: {file_path}")

class BlockButton(BoxLayout):
    """ Layout for each block button with image and label. """
    def __init__(self, block_name, image_path, on_press, **kwargs):
        super(BlockButton, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.width = dp(150)
        self.height = dp(150)

        # Block image
        self.block_image = Image(source=image_path, size_hint=(1, 0.8), allow_stretch=True)
        self.add_widget(self.block_image)

        # Block name label
        self.block_label = Label(text=block_name, size_hint=(1, 0.2), color=(1, 1, 1, 1), 
                                 font_size=dp(16), halign="center", valign="middle")
        self.block_label.bind(size=self._update_text)
        self.add_widget(self.block_label)

        # Bind the button press event
        self.bind(on_touch_down=on_press)

    def _update_text(self, instance, size):
        """ Adjust text size according to the label size. """
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
        self.add_block_button("Encryption", "3470475.png", self.go_to_encryption)
        self.add_decryption_button("Decryption", "download.jpeg", self.go_to_decryption)

        # Add layout to scroll view and scroll view to screen
        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)

    def add_block_button(self, block_name, image_path, on_press):
        """ Helper method to add a block button to the layout. """
        block_button = BlockButton(block_name, get_asset_path(image_path), on_press)
        self.layout.add_widget(block_button)

    def add_decryption_button(self, block_name, image_path, on_press):
        """ Helper method to add a decryption block button to the layout. """
        block_button = BlockButton(block_name, get_asset_path(image_path), on_press)
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
        self.file_selector = FileSelector(title='text', file_types=[("Text Files", "*.txt")])
        self.add_widget(self.file_selector)
        print(5)
        

class DecryptionScreen(Screen):
    """ Decryption screen containing file selector. """
    def __init__(self, **kwargs):
        super(DecryptionScreen, self).__init__(**kwargs)
        self.file_selector = FileSelector(title='PNG', file_types=[("PNG Files", "*.png")])
        self.add_widget(self.file_selector)
        print(4)

class PavingApp(App):
    def build(self):
        Window.set_icon(get_asset_path('image/brick.png'))  # Set app icon
        sm = ScreenManager()
        sm.add_widget(BlockSelectionScreen(name='selection'))
        sm.add_widget(EncryptionScreen(name='Encryption'))  
        sm.add_widget(DecryptionScreen(name='Decryption'))  
        return sm

if __name__ == '__main__':
    PavingApp().run()
