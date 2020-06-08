import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MyGrid(GridLayout):
	def __init__(self, **kwargs):
		super(MyGrid, self).__init__(**kwargs)

		# info layer
		self.inside = GridLayout()
		self.inside.cols = 2

		self.inside.add_widget(Label(text="Name: "))
		self.name = TextInput(multiline=False)
		self.inside.add_widget(self.name)

		self.inside.add_widget(Label(text="Last Name: "))
		self.last_name = TextInput(multiline=False)
		self.inside.add_widget(self.last_name)

		self.inside.add_widget(Label(text="male: "))
		self.male = TextInput(multiline=False)
		self.inside.add_widget(self.male)

		self.cols = 1
		self.add_widget(self.inside)
		button = Button(text="submit", font_size=40)
		button.bind(on_press=self.pressed)
		self.add_widget(button)

	def pressed(self, instence):
		name = self.name.text
		last_name = self.last_name.text
		male = self.male.text

		print("Name:",name,"last_name:",last_name,"male:",male)

		# print("pressed")

class MyApp(App):
	def build(self):
		return MyGrid()

if __name__ == "__main__":
	MyApp().run()