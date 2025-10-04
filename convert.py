from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from PIL import Image as PILImage
import os

class ImageConverter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.filechooser = FileChooserIconView(filters=['*.jpg', '*.jpeg'])
        self.add_widget(self.filechooser)

        self.size_input = TextInput(
            hint_text='Masukkan ukuran baru (contoh: 200x200)',
            size_hint_y=None,
            height=40,
            multiline=False
        )
        self.add_widget(self.size_input)

        self.status_label = Label(text='Pilih file JPG dan masukkan ukuran baru', size_hint_y=None, height=30)
        self.add_widget(self.status_label)

        self.convert_button = Button(text='Resize dan Convert ke PNG', size_hint_y=None, height=40)
        self.convert_button.bind(on_press=self.convert_image)
        self.add_widget(self.convert_button)

    def convert_image(self, instance):
        selection = self.filechooser.selection
        if not selection:
            self.status_label.text = 'Error: Tidak ada file yang dipilih!'
            return

        file_path = selection[0]
        size_text = self.size_input.text.strip()

        if 'x' not in size_text:
            self.status_label.text = 'Error: Format ukuran salah! Gunakan format WxH, misal 200x200'
            return

        try:
            width, height = map(int, size_text.lower().split('x'))
        except ValueError:
            self.status_label.text = 'Error: Ukuran harus angka, contoh 200x200'
            return

        try:
            # Buka gambar dengan PIL
            img = PILImage.open(file_path)
            # Resize gambar
            img = img.resize((width, height), PILImage.ANTIALIAS)

            # Simpan gambar sebagai PNG di folder yang sama dengan nama baru
            base, _ = os.path.splitext(file_path)
            new_file = base + '_resized.png'
            img.save(new_file, 'PNG')

            self.status_label.text = f'Sukses! Gambar disimpan di: {new_file}'
        except Exception as e:
            self.status_label.text = f'Error saat memproses gambar: {str(e)}'

class ImageConverterApp(App):
    def build(self):
        Window.size = (600, 600)
        return ImageConverter()

if __name__ == '__main__':
    ImageConverterApp().run()
