from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from jnius import autoclass
# from math import floor
from os import path
import calculation as cul

def get_android_DCIM():
	try:
		Environment = autoclass('android.os.Environment')
		# sdpath = Environment.getExternalStorageDirectory().getAbsolutePath()
		sdpath = Environment.getExternalStorageDirectory().getAbsolutePath()
	# Not on Android
	except:
		sdpath = '/storage/emmc/'

	return sdpath

if platform == 'android':
	from android.permissions import request_permissions, Permission
	from android.storage import primary_external_storage_path
	request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
					 Permission.READ_EXTERNAL_STORAGE])
	SDPATH = get_android_DCIM()

	# PythonActivity = autoclass('org.kivy.android.PythonActivity')
	# activity = PythonActivity.mActivity
	# Context = autoclass('android.content.Context')
	# vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
	# vibrator.vibrate(10000)

	Hardware = autoclass('org.renpy.android.Hardware')
	min_error = 0.05
else:
	from kivy.config import Config
	Config.set('graphics', 'width', '1040')
	Config.set('graphics', 'height', '480')
	

class MainWindow(Screen):
	pass

class CompassWindow(Screen):
	pass

class TrackCameraWindow(Screen):
	camera = ObjectProperty(None)
	camera_model = ObjectProperty(None)
	tracker = ObjectProperty(None)
	date = ObjectProperty(None)
	location = ObjectProperty(None)
	track_len = ObjectProperty(None)
	photo_len = ObjectProperty(None)

	def push_camera(self, text):
		self.camera = text

	def push_camera_model(self, text):
		self.camera_model = text

	def push_tracker(self, text):
		self.tracker = text

	def push_date(self, text):
		self.date = text

	def push_location(self, text):
		self.location = text

	def push_next(self):
		print('Camera:', self.camera)
		print('Camera Model:', self.camera_model.text)
		print('track_len:', self.track_len.text, '(mm)')
		print('photo_len:', self.photo_len.text, '(mm)')
		print('Tracker:', self.tracker)
		print('Date:', self.date)
		print('Location:', self.location)
		if platform == "android":
			if (self.track_len.text != "" and self.photo_len.text != ""):
				min_error = 0.05/ ((int(self.photo_len.text)/int(self.track_len.text))*5)
			print(min_error)

class TrackDetailWindow(Screen):
	def on_enter(self, *args):
		try:
			self.ids.image.source = self.manager.ids.fileselectscreen.ids.filechooser.selection[0]
		except:
			self.ids.image.source = 'black.png'
			print("No image loading")

	def push_topdirection(self, text):
		self.top_direction = text
		if (text == "N"):
			self.ids.bot_direction.text = "S"
		else:
			self.ids.bot_direction.text = "N"

	def push_leftdirection(self, text):
		self.left_direction = text
		if (text == "E"):
			self.ids.right_direction.text = "W"
		else:
			self.ids.right_direction.text = "E"

	def push_hemisphere(self, text):
		self.hemisphere = text

	def push_short(self, text):
		self.short = text

	def push_orientation(self, text):
		self.orientation = text

class FileSelectWindow(Screen):
	def on_enter(self, *args):
		if platform == 'android':
			self.ids.filechooser.path = path.join(SDPATH, 'Nikon_WU')
			print("SDPATH", SDPATH)
		else:
			self.ids.filechooser.path = "/home/keng/Documents/git_project/deepskytracker"

	def load(self, path, filename):
		pass

class TrackShowWindow(Screen):
	needle_angle = NumericProperty(0)
	total_rolls = NumericProperty(0)
	total_teeths = NumericProperty(0)
	status = StringProperty("")
	# a_x = NumericProperty(0)
	# o_x = NumericProperty(0)
	target_angle = NumericProperty(0)

	def update_suggestion(self):
		if (self.status == "overR"):
			self.ids.suggest_status.text = "Please reset the tracker and Rotate to Left!"
		elif (self.status == "overL"):
			self.ids.suggest_status.text = "Please reset the tracker and Rotate to Right!"
		else:
			self.ids.suggest_status.text = "Rotate to " + self.status + " :"

	def update_calculate(self, *args):
		try:
			# calculate the angle and number of rolls and teeth
			image = self.manager.ids.trackdetailscreen.ids.image.source
			hemisphere = self.manager.ids.trackdetailscreen.hemisphere
			short = self.manager.ids.trackdetailscreen.short
			orientation = self.manager.ids.trackdetailscreen.orientation
			if (orientation == "landscape"):
				direction = self.manager.ids.trackdetailscreen.ids.top_direction.text
			else:
				direction = self.manager.ids.trackdetailscreen.ids.left_direction.text
			self.status, self.angle_adjust, self.total_rolls, self.total_teeths = cul.get_angle(image, hemisphere, short, direction, orientation)
			self.update_suggestion()
			print(self.status)
			print(self.angle_adjust)
			print(self.total_rolls, "rolls")
			print(self.total_teeths, "teeths")
		except:
			print("Error!")

	def start_rotate(self):
		if platform == 'android':
			print('hardware', Hardware)
			# print(Hardware.getHardwareSensors())
			if (self.status != "overR" and self.status != "overL"):
				self.reset_rotate()
				try:
					Clock.schedule_interval(self.update_compass, 1/10)
				except:
					self.stop_rotate()

	def stop_rotate(self):
		if platform == 'android':
			Clock.unschedule(self.update_compass)
			Hardware.orientationSensorEnable(False)
			Hardware.accelerometerEnable(False)

	def reset_rotate(self):
		if platform == 'android':
			if (self.status == 'U' or self.status == 'D'):
				Hardware.accelerometerEnable(True)
				(self.start_angle,_,_) = Hardware.accelerometerReading()
				self.target_angle = self.start_angle + self.angle_adjust
			elif (self.status == 'L' or self.status == 'R'):
				Hardware.orientationSensorEnable(True)
				(self.start_angle,_,_) = Hardware.orientationSensorReading()
				self.target_angle = self.start_angle + self.angle_adjust

			if (self.target_angle < 0):
				self.target_angle = 360 + self.target_angle
			elif (self.target_angle >= 360):
				self.target_angle = self.target_angle - 360

	def update_compass(self, *args):
		if (self.status == 'U' or self.status == "D"):
			(a_x, _,_) = Hardware.accelerometerReading()
			cur_angle = (a_x/10) *90

			if (cur_angle <= self.target_angle*(1+min_error) and cur_angle >= self.target_angle*(1-min_error)):
				self.ids.image_center.source = 'center_full.png'
				self.ids.image_up.source = 'arrow_edge.png'
				self.ids.image_down.source = 'arrow_edge.png'
			if (cur_angle > self.target_angle):
				self.ids.image_center.source = 'center_edge.png'
				self.ids.image_up.source = 'arrow_edge.png'
				self.ids.image_down.source = 'arrow_full.png'
			elif (cur_angle < self.target_angle):
				self.ids.image_center.source = 'center_edge.png'
				self.ids.image_up.source = 'arrow_full.png'
				self.ids.image_down.source = 'arrow_edge.png'

		elif (self.status == 'L' or self.status == 'R'):
			(cur_angle, _,_) = Hardware.orientationSensorReading()

			left_distance = cul.distanceL(cur_angle, self.target_angle)
			right_distance = cul.distanceR(cur_angle, self.target_angle)

			if (cur_angle <= self.target_angle*(1+min_error) and cur_angle >= self.target_angle*(1-min_error)):
				self.ids.image_center.source = 'center_full.png'
				self.ids.image_left.source = 'arrow_edge.png'
				self.ids.image_right.source = 'arrow_edge.png'
			elif (left_distance < right_distance):
				self.ids.image_center.source = 'center_edge.png'
				self.ids.image_left.source = 'arrow_full.png'
				self.ids.image_right.source = 'arrow_edge.png'
			elif (left_distance > right_distance):
				self.ids.image_center.source = 'center_edge.png'
				self.ids.image_left.source = 'arrow_edge.png'
				self.ids.image_right.source = 'arrow_full.png'
				

class SettingWindow(Screen):
	def on_spinner_select(self, text):
		print(text)

class WindowManager(ScreenManager):
	pass

kv = Builder.load_file("my.kv")

class MyApp(App):

	def build(self):
		return kv

if __name__ == "__main__":

	main_app = MyApp()
	main_app.run()