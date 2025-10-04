from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog

class ImageConverter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Button
        self.select_button = Button(text="Select JPG File", size_hint_y=None, height=40)
        self.select_button.bind(on_release=self.open_file_dialog)
        self.add_widget(self.select_button)

        # Label text
        self.info_label = Label(text="Click the button to select a JPG file", size_hint_y=None, height=40)
        self.add_widget(self.info_label)

        # image output
        self.output_image = KivyImage()
        self.add_widget(self.output_image)

        # hide tkinter
        self.tk_root = tk.Tk()
        self.tk_root.withdraw()

    def open_file_dialog(self, instance):
        file_path = filedialog.askopenfilename(
            title="Select a JPG file",
            filetypes=[("JPEG files", "*.jpg;*.jpeg")]
        )
        if file_path:
            self.convert_and_resize(file_path)

    def convert_and_resize(self, jpg_path):
        try:
            img = Image.open(jpg_path)
            max_size = 800
            img.thumbnail((max_size, max_size))
            base, _ = os.path.splitext(jpg_path)
            png_path = base + ".png"
            img.save(png_path, "PNG")

            self.info_label.text = f"Converted and resized image saved as:\n{png_path}"

            # Update the Kivy Image widget to show the PNG
            self.output_image.source = png_path
            self.output_image.reload()

        except Exception as e:
            self.info_label.text = f"Error: {str(e)}"
            self.output_image.source = ''
            self.output_image.texture = None

class ImageConverterApp(App):
    def build(self):
        return ImageConverter()

if __name__ == '__main__':
    ImageConverterApp().run()
