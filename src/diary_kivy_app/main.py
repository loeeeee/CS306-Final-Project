from kivy.app import App
from kivy.uix.label import Label

class DiaryApp(App):
    def build(self):
        return Label(text='Hello, Diary App!')

if __name__ == '__main__':
    DiaryApp().run()
