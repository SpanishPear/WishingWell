
from kivy.app import App #This imports the App and makes it available

from kivy.uix.floatlayout import FloatLayout #This imports the BoxLayout and makes it available

from kivy.properties import StringProperty #This imports the StringProperty and makes it available

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition #imports the screen and screenmanager classes

from kivy.core.window import Window #import Window allows me to change background colour in line 35

from kivy.lang import Builder    #Imports builder, allowws me to set the root_widget as builder.load_file(Avondale.kv)

from kivy.uix.behaviors import ButtonBehavior #imports the button behaviours to be used for the ImageButton

from kivy.uix.image import Image #imports the image class so that the behaviours of images and the settable properties (eg source) can be used in the ImageButton widget

from kivy.uix.button import Button #imports the image class so that the behaviours of images and the settable properties (eg source) can be used in the ImageButton widget

import csv    #imports the csv module for data processing of csv files
from kivy.uix.gridlayout import GridLayout  #imports the Gridlayout option
from kivy.animation import Animation
from kivy.graphics import *
from kivy.uix.label import Label #imports the label widget so that i can dynamically create labels python side
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle #imports the colour and rectangle libraries so i can make coloured boxes.


from kivy.properties import ObjectProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from API import *
import re
Window.size = (1440,900)


#Light Blue: #C2EFE9
#	rgb(194, 239, 233)
#	(0.7608, 0.93725, 0.9137)
#	HSV(0.4778, 0.1883, 0.9373)

#Green Blue: #53C3B7
#	rgb(83, 195, 183)
#	(0.3255, 0.764706, 0.71765)
#	HSV(0.4821, 0.5744, 0.7647)

#Dark Blue #242F410
#	rgb(36, 47, 65)
#	(0.141, 0.18431, 0.2549)
#	HSV(0.5990,0.4324,0.2902)

#Light Grey Text Colour: #a5a5a5
#	rgb(165,165,165)
#	(0.647, 0.647, 0.647)
#
#-----------DEFINING GLOBAL VARIABLES------------
#DEFINING COLOR VARIABLES
rgba_darkblue = (0.141, 0.18431, 0.2549, 1)
rgba_lightgrey =  (0.647, 0.647, 0.647, 1)
rgba_lightblue = (0.7608, 0.93725, 0.9137, 1)
rgba_greenblue = (0.3255, 0.764706, 0.71765,1)
rgba_white = (1,1,1,1)
colours = {"rgba_darkblue":(0.141, 0.18431, 0.2549, 1), "rgba_lightgrey":(0.647, 0.647, 0.647, 1), "rgba_lightblue":(0.7608, 0.93725, 0.9137, 1), 'rgba_greenblue':(0.3255, 0.764706, 0.71765,1)}
#DEFINING OTHER  VARIABLES
active = "SignUp"


#DEFINING POPUPS (unable to do it in kv file, screens and popups cannot go together)
Builder.load_string('''
<ErrorPopup>:

	title: "Error"
	title_size: 20
	title_align: 'center'
	size_hint: .6,.6

	FloatLayout:
		Label:
			text: 'YEET'

''')

#--------------_CUSTOM WIDGETS_-------------------
class Functions(Screen):
	def call_reload_shared_wishlists(): #DONE
		reload_shared_wishlists()
	def call_sign_up(fullname, password, emailAddr):
		pattern = re.compile(r'[a-zA-Z0-9]+(\.[a-zA-Z]*){0,2}@[a-zA-Z]+(\.[a-zA-Z]*)*')#regex conditions for an email adress
		match = pattern.match(emailAddr)
		if fullname == "":
			#//TODO ERROR MESSAGE POPUP
			pass
		elif password == "":
			#//TODO ERROR MESSAGE POPUP
			pass
		elif emailAddr == "":
			#//TODO ERROR MESSAGE POPUP
			pass
		elif match == None:
			#//TODO ERROR MESSAGE POPUP
			pass
		else:
			sign_up(fullname, password, emailAddr)
	def call_login(email_input, password_input):
		login_to_app(email_input, password_input)


class ErrorPopup(Popup):
	pass

class LoginScreen(Screen):

	def switchScreen(self):
		global active

		if active == "SignUp":
			self.parent.current = "Login"
			active = "Login"
		else:
			self.parent.current = "SignUp"
			active = "SignUp"
	def openPopup(self, *args):
		 ErrorPopup().open()
	def call_login(self,email_input, password_input):
		Functions.call_login(email_input, password_input)

class SignUpScreen(Screen):
	functionObject = ObjectProperty(None)
	def switchScreen(self):
		global active

		if active == "SignUp":
			self.parent.current = "Login"
			active = "Login"
		else:
			self.parent.current = "SignUp"
			active = "Signup"
	def call_sign_up(self,fullname, password, emailAddr):
		Functions.call_sign_up(fullname, password, emailAddr)



class TermsAndConditions(Screen):
	pass
class ScreenManager(ScreenManager):
	pass

root_widget = Builder.load_file("TheWishingWell.kv")

class WishingWell(App):
	def build(self):
		return root_widget

if __name__ == '__main__':
	WishingWell().run()
