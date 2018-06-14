
from kivy.app import App #This imports the App and makes it available

from kivy.uix.floatlayout import FloatLayout #This imports the BoxLayout and makes it available

from kivy.properties import StringProperty #This imports the StringProperty and makes it available

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition #imports the screen and screenmanager classes

from kivy.core.window import Window #import Window allows me to change background colour in line 35

from kivy.lang import Builder    #Imports builder, allowws me to set the root_widget as builder.load_file(Avondale.kv)

from kivy.uix.behaviors import ButtonBehavior #imports the button behaviours to be used for the ImageButton

from kivy.uix.image import Image #imports the image class so that the behaviours of images and the settable properties (eg source) can be used in the ImageButton widget

from kivy.uix.button import Button #imports the image class so that the behaviours of images and the settable properties (eg source) can be used in the ImageButton widget

from kivy.uix.gridlayout import GridLayout  #imports the Gridlayout option
from kivy.animation import Animation
from kivy.graphics import *
from kivy.uix.label import Label #imports the label widget so that i can dynamically create labels python side
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle #imports the colour and rectangle libraries so i can make coloured boxes.
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from API import *
import API
from Wishlists import *
import re
import glob
import time
import os
from functools import partial
import csv    #imports the csv module for data processing of csv files

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
ErrorMessage = ""
emailPassword = ""
FN =""
currentWishlist = ""
namesPlaced = False
editMode = False
wishlist_to_be_deleted = ""
#DEFINING POPUPS (unable to do it in kv file, screens and popups cannot go together)
Builder.load_string('''
<ErrorPopup>:

	title: "Error"
	title_size: 20
	title_align: 'center'
	size_hint: .6,.6
	separator_color: (1,1,1,1)
	background_normal: ''
	background: "../assets/PopupBackground.jpg"
	auto_dismiss: False
	FloatLayout:
		id: ErrorLayout
		Label:
			id: ErrorMessage
			text: root.ErrorMessage
			color: (1,0,0,1)
			pos: root.width/2*0.7, root.height/2
			font_size: root.height/8
			halign: 'center'
		Button:
			id: ButtonValue
			text: root.ButtonValue
			background_color: (0.141, 0.18431, 0.2549, 1)
			pos: root.width/2*1.3, root.height/2
			width: root.width/12
			height: root.width/14
			size_hint: 0.4,0.1
			on_press: root.dismiss()


''')

#--------------_CUSTOM WIDGETS_-------------------
class ImageButton(ButtonBehavior, Image):
	pass
#----------------POPUPS --------------
class ErrorPopup(Popup): #COMMENTED
	ErrorMessage = "" #sets ErrorMessage to  ""
	ButtonValue = "Retry" #sets ButtonValue to "Retry"

#---------------SCREENS----------------------
##--------_FUNCNTION SCREEN-----------------
class Functions(Screen):
	def call_reload_shared_wishlists(): #DONE
		reload_shared_wishlists()#calls the reload_shared_wishlists fucntion defined in API.py
	def call_sign_up(self, fullname, password, emailAddr):
		pattern = re.compile(r'[a-zA-Z0-9]+(\.[a-zA-Z]*){0,2}@[a-zA-Z]+(\.[a-zA-Z]*)*')#regex conditions for an email adress
		match = pattern.match(emailAddr) #Checks if emailAddr matches the pattern for an email adress. if False returns None


		#//TODO ADD LENGTH VALIDATIONS AS WELL


		#---------NO FULL NAME ERROR POPUP --------------
		if fullname == "":
			newValue = "Please Enter Full Name!"
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		#---------NO EMAIL ADRESS ERROR POPUP --------------
		if emailAddr == "":
			newValue = "\nPlease Enter an Email Adress!"
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		#---------INVALID EMAIL ERROR POPUP --------------
		if match == None:
			newValue = "\nPlease Enter a Valid Email Adresss!"
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		#---------NO PASSWORD ERROR POPUP --------------
		if password == "":
			newValue = "\nPlease Enter Password!"
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		else:
			#-------------ALREADY SIGNED UP ERROR POPUP-----------
			if sign_up(fullname, password, emailAddr) == False:
				newValue = "\n Someone has already signed up with this email adresss!"
				ErrorPopup.ErrorMessage += newValue
			#------------------SUCCESS ERROR POPUP----------------
			else:
				newValue = "Congratulations!\nYou have Successfully Signed Up!"
				ErrorPopup.ButtonValue = "Continue"
				ErrorPopup.ErrorMessage = newValue
				self.parent.current = "Login"


		LoginScreen().openErrorPopup()#opens error popup
		ErrorPopup.ButtonValue = "Retry"

		ErrorPopup.ErrorMessage = "" #resets the error message back to nothing, or error messages will stack
	def call_login(self,email_input, password_input): #COMMENTED
		login = False
		#--------NO EMAIL ADRESS ERROR POPUP-----------
		if email_input == "": #If there is no email adress, asks user to enter an email adress
			newValue = "\nPlease Enter an Email Address!" #Sets new value to "Please Enter an Email Adress!"
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		#---------NO PASSWORD ERROR POPUP --------------
		if password_input == "": #If there is no password, asks user to enter a password
			newValue = "\nPlease Enter Password!" #Sets new value to please enter an email adress
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		else:
			if login_to_app(email_input, password_input) == False: #calls the login_to_app function defined in API.py, if its false (ie, if the username/password is incorrect), tell the user that their username/password is incrorect
				newValue = "\n Incorrect Username/Password!" #sets new value to incorrect username/[assword]
				ErrorPopup.ErrorMessage += newValue
			else:
				login = True #sets login Flag to True
		if login == False: #if there is an erro in the login processes, then open the ErrorPopup
			LoginScreen().openErrorPopup()#opens error popup
		else: #otherwise go to the loginvalidation screen
			#self.parent.current = "LoginValidation" //TODO RE-ENABLE THIS #go to the login validation screen
			pass
	def callCreateWishlist(self, wishlist_name):
		MyWishlists().CreateWishlist(wishlist_name)
	def callPlaceWishlistNames(self, **kwargs):
		MyWishlists().PlaceWishlistNames(edit = False)


class NewWishlistScreen(Screen):
	def CreateWishlist(self, wishlist_name):
		if len(wishlist_name) < 10: #restriction on wishlist_name length , has to be less than 10 characters
			MyWishlists().CreateWishlist(wishlist_name)
			MyWishlists().PlaceWishlistNames(edit=False)
			self.parent.current = 'MyWishlists' #changes screen to MyWishlists
			self.ids.WishlistNameInput.text = "" #resets the text input to "" so it looks empty when they create a new wishlist
		else:
			self.ids.MessageLabel.text = "Please make sure your wishlist name is < 10 characters long!"

class LoginValidationScreen(Screen):
	Message = "Welcome! In order to use Wishlists software properly,\n we need to use your email password to send emails\n containing wishlists to your friends,\n and to search for wishlists that have been sent to you \nby your friends."
	def validate(self,password_input):
		global FN
		global emailPassword
		if auth(API.emailAddr,password_input,imap_url)== False:
			self.ids.MessageButton.text = "Incorrect password!\n Please input the password\n for the email that you signed up with"
		else:
			#self.parent.current = "Menu" #//TODO RE-ENABLE THIS
			emailPassword = password_input
			FN = API.fullName
			# print("\n,email password: " ,emailPassword,
			# 	  "\n email address:", API.emailAddr,
			# 	  "\n full name:", API.fullName,
			# 	  "\n app password:", API.appPassword)
	def ExitLoginScreen(self):
		self.parent.current = "Login"

class LoginScreen(Screen):
	def closePopup(self, *args):
		global login
		login.dismiss() #WORKS
	def switchScreen(self):
		global active

		if active == "SignUp": #If current screen is SignUp, change screen to Login when pressed
			self.parent.current = "Login"
			active = "Login"
		else:#If current screen is SignUp, change screen to Login when pressed
			self.parent.current = "SignUp"
			active = "SignUp"
	def openErrorPopup(self, *args):
		 ErrorPopup().open()
	def call_login(self,email_input, password_input):
		Functions.call_login(self,email_input, password_input)

class SignUpScreen(Screen):
	def switchScreen(self):
		global active
		if active == "SignUp":#If current screen is SignUp, change screen to Login when pressed
			self.parent.current = "Login"
			active = "Login"

		else:#If current screen is SignUp, change screen to Login when pressed
			self.parent.current = "SignUp"
			active = "Signup"
	def call_sign_up(self,fullname, password, emailAddr):
		Functions.call_sign_up(self,fullname, password, emailAddr)

class MainMenu(Screen):
	welcome = "Welcome,"
	firstname = ''
	def on_enter(self):
		Functions.call_login(self,'shrey.somaiya@gmail.com','***REMOVED***') #//TODO DISABLE THIS
		LoginValidationScreen.validate(self, '***REMOVED***') #//TODO DISABLE THIS
		self.firstname = FN.split(" ")[0] +"!"

class MyWishlists(Screen):
	def on_enter(self):
		global editMode
		#checks if still in edit mode, if it is, draw butons as red with different buton
		if not editMode:
			self.PlaceWishlistNames(edit=False)
			editMode = False

		else:
			self.editWishlists()
			editMode = True
	def checkIfSaved(self):

		global currentWishlist #imports the global current wishlist variable
		#------------CHECKS IF CURRENT WISHLIST HAS BEEN SAVED BEFORE SWITCHING TO NEW ONE------
		''' This block of code compares the contents of a wishlist with the contents of the text inputs on the screen. If they are different, the user has unsaved changes'''
		try:
			items = [] #initialises an empty items list
			for child in self.ids.ItemsGrid.children: #get every child of the grid, ie every item in the list
				if child.text != '':
					print(child.text)
					items.append(child.text) #add the text ( the wishlist item) to the items list

			items = self.sortArray(items) #sorts the items list using an insertion sort
			items.reverse() #reverses the item list, chose not to put this into the sortArray for readability.
			Expected_items = items #sets expected items to be the items on screen



			given = OpenWishlistFromName(currentWishlist) #sets given to be the wishlist currentlys aved
			given = self.sortArray(given) #Sorts the given wishlist
			given.reverse() #reverses the given list

			if Expected_items != given: #if items in the list on screen are not the same as the items actually in the list THEN
				#sets error message to "You have unsaved changes!"
				ErrorPopup.ErrorMessage = "You have unsaved changes!"
				#opens the error popup
				LoginScreen().openErrorPopup()
				return False
			else:
				print(True)
		except Exception as e:
			pass

	def sortArray(self, array):
		'''Sorts a given array using an insertion sort'''
		 # Traverse through 1 to len(arr)
		for i in range(1, len(array)):

			key = array[i]

			# Move elements of array[0..i-1], that are
			# greater than key, to one position ahead
			# of their current position
			position = i-1
			while position >=0 and key < array[position] :
					array[position+1] = array[position]
					position -= 1
			array[position+1] = key
		return array

	def CreateWishlist(self, *args): #COMMENTED
		'''Creates a wishlist given a wishlist_name (in args), or saves the current wishlsit'''
		global currentWishlist #get the name of the current wishlist opened
		global namesPlaced
		items = [] #sets items to list with header "items"
		if args:
			wishlist_name = args[0] #sets wishlist name to first argument
			wishlist_name = wishlist_name.replace(' ', "_")
		else:
			wishlist_name = currentWishlist #sets wishlist_name to name of the current wishlist
		if wishlist_name is not "":
			try: #Use of try except because if it will fail if we are creatinga  new wishlsit from scratch
				for child in self.ids.ItemsGrid.children: #get every child of the grid, ie every item in the list
					print(child.text)
					items.append(child.text) #add the text (the wishlist item) to the items list
			except:
				namesPlaced = False
			items.append("items") #we add this LAST becuase when we reverse it, we want it first!
			items.reverse() #reverses the item list
			wishlist = items #sets wishlist to equal the items list.
			filepath ="Wishlists/"+wishlist_name + "-" +API.emailAddr+'.csv'
			with open(filepath, "w") as output: #open the wishlist file corresponding to the wishlist open in the program
				writer = csv.writer(output, lineterminator='\n')# set up a csv writer
				for item in wishlist:
					writer.writerow([item]) #write the wishlist in the program to the file ( save it )
				for i in range(100-len(wishlist)):
					writer.writerow("")  #write everything else as a . (csv doesntlike blank rows)

	def PlaceWishlistItems(self,wishlist_name, *args):

		'''Locates, opens and outputs the contents of a wishlist given its name. Places the
		items on the screen displays the wishlists name and displays the share and save buttons. '''
		global currentWishlist #imports the global current wishlist variable
		if self.checkIfSaved() == False:
			return


		#------------UPDATING SCREEN WITH BUTONS AND NAME----------------
		'''This block of code places the name of the wishlist as a heading, places the items button for the top of the wishlist, scrolls the wishlist scroll view to the top, and makes the save button and share button visible'''
		currentWishlist = wishlist_name #sets current wishlist to wishlist_name
		try:
			self.ids.WishlistNameLabel.text = str("{" + wishlist_name.replace("_"," ")+"}") #replaces _ with " " if there is an _ in the name (for aesthetics)
		except:
			self.ids.WishlistNameLabel.text = str("{" + wishlist_name +  "}") #just places the wishlsitname on screen with the { } as decorations
		#defines the items button with the following parameters:
		ItemsButton = Button(
			size_hint = (None, None),
			size = ((Window.size[0]*2)/2.65,Window.size[1]/22),
			text = "ITEMS",
			halign = 'center',
			pos_hint = {"center_x": 0.58,"center_y": 0.72	 },
			background_color = (0,0,0,1),
			background_down = ""
		)
		self.ids.RightPanel.add_widget(ItemsButton) #adds the items rectangle at the top
		self.ids.ScrollView.scroll_y = 1 #makes scroll view scroll to top
		self.ids.ShareButton.opacity = 1 #makes share button visible
		self.ids.SaveButton.opacity = 1 #makes save button visible

		#-------------PLACING WISHLIST ON SCREEN-----------------
		'''This block of code places the wishlist items in text inputs INSIDE the scroll view on the screen. '''
		items = [] #sets items to []
		pattern = re.compile(r'\/.*-') #regex pattern to find name of string given CSV filename
		self.ids.ItemsGrid.clear_widgets() #Removes existing wishlist from screen
		layout = self.ids.ItemsGrid #sets layout to the GridLayout
		layout.bind(minimum_height=layout.setter('height')) #sets grid to minimum height, allows for scrolling
		wishlist_path = "Wishlists/"+wishlist_name + "-" +API.emailAddr+'.csv'  #sets wishlist path given the wishlist name and email adress
		with open(wishlist_path) as f: #open the file
			reader = csv.DictReader(f) #opens a reader
			for row in reader: #for every row in the file
				items.append(row['items']) #appends the item in the wishlist to the items list

		#This loop goes through the wishlist, and creates a text input for each item. If there is no item, the text input's text value is "", and is still placed on screen
		for i in range(100):
			try:
				text = items[i] #sets text to item in wishlist
			except:
				text ='' #if there is no item, sets text to " "
			#defines the text input widget, with all its properties (self explanetory)
			TI = TextInput(
				text = text,
				size_hint = (None, None),
				size = (Window.size[0],Window.size[1]/24),
				background_color = rgba_darkblue,
				foreground_color = rgba_white,
				hint_text_color = rgba_white)
			self.ids.ItemsGrid.add_widget(TI) #adds text input to the grid

	def PlaceWishlistNames(self, *args, **kwargs):
		'''

		PlaceWishlistNames(edit wipe)
		'''
		global namesPlaced #imports the namesPlaced variable so we can change it to true once the names are placed
		list_wishlists = glob.glob("Wishlists/*.csv") #gets list of wishlists
		names = [] #sets names to empty list
		pattern = re.compile(r'\/.*-') #regex pattern to find name of wishlist in the filename

		self.ids.NamesGrid.clear_widgets()


		layout = self.ids.NamesGrid

		layout.bind(minimum_height=layout.setter('height'))#sets minium height to the layouts height, allows for scrolling
		#adds each name of the of each of the wishlists  in the list of wishlists.
		for item in list_wishlists:
			wishlist_name = pattern.findall(item)[0][1:-1]
			try:
				wishlist_name_displayed = wishlist_name.replace("_"," ") #if the name contains an underscore, replace it with a space
			except:
				wishlist_name_displayed = wishlist_name #otherwise set the name displayed to the name found
			#create the name button
			btn = Button(
				text = str(wishlist_name_displayed),
				size_hint = (None, None),
				size = (Window.size[0]/8,Window.size[1]/24),
				halign = 'center',
				color = (0,0,0,1))
			#ie if kwargs["edit"]==False
			if not kwargs["edit"]:
				btn.bind(on_press = partial(self.PlaceWishlistItems, wishlist_name))
				btn.background_color = rgba_lightblue
			#if edit is a kwargument then:
			else:
				#set buton press to delete the wishlist, rather than display the wishlist
				btn.bind(on_press= partial(self.deleteWishlist, wishlist_name))
				#changes the background_color to red, for visual, that you are deleting if you click.
				btn.background_color = (1,0,0,1)

			self.ids.NamesGrid.add_widget(btn)
		namesPlaced = True
		print("loop finished")





	def editWishlists(self):
		''' Makes wishlists delete themselves upon button click '''
		#clears the
		self.ids.NamesGrid.clear_widgets()
		self.PlaceWishlistNames(edit=True)

	def deleteWishlist(self, wishlist_name, *args):
		global wishlist_to_be_deleted
		wishlist_to_be_deleted = wishlist_name
		self.parent.current = "deleteWishlist"
	#-------Button press functions-----

	#---- SAVE BUTTON-----

	def pressed_save_button(self):
		self.ids.SaveButton.source = "../assets/saveicon_down.png" #sets image to the "down" version
		self.CreateWishlist() #calls the CreateWishlist function

	def released_save_button(self):
		self.ids.SaveButton.source = "../assets/saveicon.png" #sets image back to normal

	#--SHARE BUTTON---

	def pressed_share_button(self):
		self.ids.ShareButton.source = "../assets/shareicon_down.png" #sets image to the 'down' version
	def released_share_button(self):
		self.ids.ShareButton.source = "../assets/shareicon.png" #sets image back to normal image

	#----NEW WISHLIST BUTTON -----
	def pressed_new_wishlist_button(self):
		self.ids.NewWishlist.source = "../assets/plusbutton_down.png"
		self.parent.current = "NewWishlist"

	def released_new_wishlist_button(self):
		self.ids.NewWishlist.source = "../assets/plusbutton.png"

	#---EDIT BUTTON WISHLIST-------

	def pressed_edit_button(self):
		#sets image to the edit icon down image
		self.ids.EditWishlists.source = "../assets/editicon_down.png"
		global editMode
		#makes use of a binary switch to determine if edit mode is on or not. If edit mode is "On" and thebuton is clicked, then edit mode is turned off, and set to False. Vice versa
		if editMode:
			print("edit == False")
			self.PlaceWishlistNames(edit=False)
			editMode = False

		else:
			self.editWishlists()
			editMode = True

	def released_edit_button(self):
		self.ids.EditWishlists.source = "../assets/editicon.png"


class deleteScreen(Screen):
	Message = "Are you sure you want\n to delete this wishlist?" #cant import the actual name for some reason :/
	def deleteWishlist(self):
		wishlist_name = wishlist_to_be_deleted
		try:
			wishlist_name = wishlist_name.replace(" ","_") #if the name contains an underscore, replace it with a space
		except:
			pass
		filepath ="Wishlists/"+wishlist_name + "-" +API.emailAddr+'.csv'
		os.remove(filepath) #deletes the wishlist
		self.parent.current = "MyWishlists"



class TermsAndConditions(Screen):
	pass
class ScreenManager(ScreenManager):
	pass

root_widget = Builder.load_file("TheWishingWell.kv")
sm = ScreenManager()
class WishingWell(App):
	def build(self):
		return root_widget

if __name__ == '__main__':
	WishingWell().run()
