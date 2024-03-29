
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
import traceback
import time

Window.size = (1440,900)

#-------------------------------------------------------------------------------------------------
#										GLOBAL VARIABLES
#-------------------------------------------------------------------------------------------------

									#DEFINING COLOR VARIABLES
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
rgba_darkblue = (0.141, 0.18431, 0.2549, 1)
rgba_lightgrey =  (0.647, 0.647, 0.647, 1)
rgba_lightblue = (0.7608, 0.93725, 0.9137, 1)
rgba_greenblue = (0.3255, 0.764706, 0.71765,1)
rgba_white = (1,1,1,1)
colours = {
		"rgba_darkblue":(0.141, 0.18431, 0.2549, 1),
		"rgba_lightgrey":(0.647, 0.647, 0.647, 1),
		"rgba_lightblue":(0.7608, 0.93725, 0.9137, 1),
		'rgba_greenblue':(0.3255, 0.764706, 0.71765,1)
		}

									#OTHER GLOBAL VARIABLES
active = "SignUp"
ErrorMessage = ""
emailPassword = ""
FN =""
currentWishlist = ""
namesPlaced = False
editMode = False
wishlist_to_be_deleted = ""
#whilst named ViewingTargetsEmail, it refers to the user's wishlist that the root user is viewing, not the root users email adress
targetUser = ""
targetEmail = ""
deleted = []
validWishlistName = re.compile(
r'(.)*-(([a-zA-Z0-9]+(\.[a-zA-Z]*){0,2}@[a-zA-Z]+(\.[a-zA-Z]*)*)).csv'
)

validEmail = re.compile(r'[a-zA-Z0-9]+(\.[a-zA-Z]*){0,2}@[a-zA-Z]+(\.[a-zA-Z]*)*')#regex conditions for an email adress

#-------------------------------------------------------------------------------------------------
#										CUSTOM WIDGETS
#-------------------------------------------------------------------------------------------------
class ImageButton(ButtonBehavior, Image):
	pass
#-------------------------------------------------------------------------------------------------
#											POPUPS
#-------------------------------------------------------------------------------------------------


class ErrorPopup(Popup): #COMMENTED
	ErrorMessage = "" #sets ErrorMessage to  ""
	ButtonValue = "Retry" #sets ButtonValue to "Retry"

#Have to define popups as a builder string, popups and screens do not go together properly
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
			font_size: root.height/10
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

#-------------------------------------------------------------------------------------------------
#											SCREENS
#-------------------------------------------------------------------------------------------------


class Functions(Screen):
	'''

		Worth noting that whilst this class does not have a visible screen, it is very imoportant as it acts as a link between the API functions and the graphical interace.
		This class allows for the API functions to be called in the context of OOP with Kivy, and also allows me to add data validation before the function is called.

	'''
	def call_reload_shared_wishlists(self): #DONE
		reload_shared_wishlists()#calls the reload_shared_wishlists fucntion defined in API.py
	def call_sign_up(self, fullname, password, emailAddr):
		pattern = re.compile(r'[a-zA-Z0-9]+(\.[a-zA-Z]*){0,2}@[a-zA-Z]+(\.[a-zA-Z]*)*')#regex conditions for an email adress
		match = pattern.match(emailAddr) #Checks if emailAddr matches the pattern for an email adress. if False returns None


		#//TODO ADD LENGTH VALIDATIONS AS WELL


		#---------NO FULL NAME ERROR POPUP --------------
		if fullname.strip() == "":
			newValue = "Please Enter Full Name!"
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		#---------NO EMAIL ADRESS ERROR POPUP --------------
		if emailAddr.strip() == "":
			newValue = "\nPlease Enter an Email Adress!"
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		#---------INVALID EMAIL ERROR POPUP --------------
		if match == None:
			newValue = "\nPlease Enter a Valid Email Adresss!"
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		#---------NO PASSWORD ERROR POPUP --------------
		if password.strip() == "":
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

		ErrorPopup.ErrorMessage = "" #resets the error message back to nothing, or error messages will stack DOCUMENATION
	def call_login(self,email_input, password_input): #COMMENTED
		login = False
		print("Call_login in the Functions class was just called!")

		#--------NO EMAIL ADRESS ERROR POPUP-----------
		if email_input.strip() == "": #If there is no email adress, asks user to enter an email adress
			newValue = "\nPlease Enter an Email Address!" #Sets new value to "Please Enter an Email Adress!"
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		#---------NO PASSWORD ERROR POPUP --------------
		elif password_input.strip() == "": #If there is no password, asks user to enter a password
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
			ErrorPopup.ErrorMessage = "" #resets error Message
		else: #otherwise go to the loginvalidation screen
			self.parent.current = "LoginValidation"


	def call_share_wishist(self,to_addr):
		pattern = re.compile(r'[a-zA-Z0-9]+(\.[a-zA-Z]*){0,2}@[a-zA-Z]+(\.[a-zA-Z]*)*')#regex conditions for an email adress
		match = pattern.match(emailAddr) #Checks if emailAddr matches the pattern for an email adress. if False returns None
		#if the email adress is not valid
		if match == None:
			newValue = "\nPlease Enter a Valid Email Adresss!"
			ErrorPopup.ErrorMessage += newValue #adds new error message to existing one
		if to_addr != "":
			share_wishlist(to_addr, API.emailAddr, currentWishlist)

	def call_reload_wishlists(self):
		reload_wishlists()

	def call_save_wishlist(self):
		save(API.emailAddr,emailPassword,currentWishlist)


class LoginScreen(Screen): #COMMENTED #TESTING DOCUMENTATION

	def switchScreen(self, *args): #COMMENTED #TESTING DOCUMENTATION
		'''
		This is essentially a NOT gate, if the active screen is “SignUp”, then change the active screen to “Login”, and change the global active variable to “Login”, to tell the program that “Login” is now the active screen and works the opposite way if “SignUp” is the active screen
		'''
		global active
		if active == "SignUp": #If current screen is SignUp, change screen to Login when pressed
			self.parent.current = "Login" #sets current screen to login screen
			active = "Login" #sets active variable to "Login"

		else:#If current screen is SignUp, change screen to Login when pressed
			self.parent.current = "SignUp" #changes screen to sign up screen
			active = "SignUp" #sets active variable to "SignUp"

	def openErrorPopup(self, *args): #COMMENTED #TESTING DOCUMENTATION
		'''
		This function opens the ErrorPopup.
		'''
		ErrorPopup().open() #opens the ErrorPopup

	def call_login(self,email_input, password_input):
		'''
		This function calls the call_login function defined in the Function class, the class where functions defined in API.py are called
		'''
		Functions.call_login(self,email_input, password_input) #COMMENTED #TESTING DOCUMENTATION

class SignUpScreen(Screen): #COMMENTED #TESTING DOCUMENTATION

	def switchScreen(self):#COMMENTED #TESTING
		'''
		This is essentially a NOT gate, if the active screen is “SignUp”, then change the active screen to “Login”, and change the global active variable to “Login”, to tell the program that “Login” is now the active screen and works the opposite way if “SignUp” is the active screen


		NOTE: Had to re-define the function, was unable to change screen from a function in another screen:
				ERROR --'NoneType' object has no attribute 'current'

		'''
		global active
		if active == "SignUp": #If current screen is SignUp, change screen to Login when pressed
			self.parent.current = "Login" #sets current screen to login screen
			active = "Login" #sets active variable to "Login"

		else:#If current screen is SignUp, change screen to Login when pressed
			self.parent.current = "SignUp" #changes screen to sign up screen
			active = "SignUp" #sets active variable to "SignUp"

	def call_sign_up(self,fullname, password, emailAddr):#COMMENTED #TESTING
		Functions.call_sign_up(self,fullname, password, emailAddr) #remove brackets and add self so that you dont instatiate the functions class, and you keep it as a screen.

class LoginValidationScreen(Screen):#COMMENTED #TESTING DOCUMENTATION
	Message = "Welcome! In order to use Wishlists software properly,\n we need to use your email password to send emails\n containing wishlists to your friends,\n and to search for wishlists that have been sent to you \nby your friends."
	#Validate Driver:
	# def on_enter(self):
	# 	self.validate('mqcrgsyqflmpqrnr')

	def validate(self,password_input, *args): #COMMENTED
		'''
		This function attempts to login to the gmail server with the password_input parameter, and the email address with which the user logged in with, stored as API.emailAddr. If the login attempt fails, change the error message to say that the login failed, and to try again. If the login attempt succeeds, change the screen to the Main Menu screen, and set the global emailPassword variable to contain the emailPassword(passed as a parameter , password_input)
		'''
		global FN #imports the global FN variable
		global emailPassword #imports the global emailPassword variable
		#tries to login to server given emailAddr and password_input
		if auth(API.emailAddr,password_input,imap_url)== False:
			#if password is incorrect, tell uesr
			self.ids.MessageButton.text = "Incorrect password!\n Please input the password\n for the email that you signed up with"
			#print("Incorrect password!\n Please input the password\n for the email that you signed up with, False") #TESTING DOCUMENTATION
			return False
		#otherwise go to Menu, set emailPassword to password input
		else:
			self.parent.current = "Menu" #//TODO RE-ENABLE THIS
			#set emailPassword to password_input
			emailPassword = password_input
			#set FN to the API.fullName variable
			FN = API.fullName
			#print("True, FN set to",FN,"emailPassword set to", emailPassword) #TESTING DOCUMENTATION
			return True

class MainMenu(Screen):
	welcome = "Welcome,"
	firstname = StringProperty()
	def on_enter(self):
		self.firstname = str(FN.split(" ")[0] +"!")

class MyWishlists(Screen):

	def on_enter(self):

		#imports the global editMode
		global editMode
		#imports global ViewingTargetsEmail
		global ViewingTargetsEmail
		#imports global current Wishlist
		global currentWishlist
		currentWishlist = ""
		#changse the email adress's wishlist that the user is viwing is their own wishlists


		ViewingTargetsEmail = API.emailAddr

		self.ids.ItemsGrid.clear_widgets()
		self.ids.SaveButton.opacity = 0
		self.ids.ShareButton.opacity = 0
		self.ids.WishlistNameLabel.opacity = 0
		self.ids.ItemsButton.opacity = 0
		#checks if still in edit mode, if it is, draw butons as red with different buton
		if not editMode:
			self.PlaceWishlistNames(edit=False) #callPlaceWishlistNames with edit kwarg as false
			editMode = False #sets the editMode switch to false

		else:
			self.ids.EditModeText.opacity = 1 #makes the EDIT MODE text visible
			self.ids.ReloadButton.opacity = 0 #makes the reloadbutton dissapear
			self.editWishlists() #calls the editWishlists function
			editMode = True #sets the EditMode switch to true

	def checkIfSaved(self,**kwargs):

		global currentWishlist #imports the global current wishlist variable
		#------------CHECKS IF CURRENT WISHLIST HAS BEEN SAVED BEFORE SWITCHING TO NEW ONE------
		''' This block of code compares the contents of a wishlist with the contents of the text inputs on the screen. If they are different, the user has unsaved changes'''
		if currentWishlist == "":
			return
		try:
			items = [] #initialises an empty items list
			for child in self.ids.ItemsGrid.children: #get every child of the grid, ie every item in the list
				if child.text != '':
					print(child.text)
					items.append(child.text) #add the text ( the wishlist item) to the items list

			items = self.sortArray(items) #sorts the items list using an insertion sort
			items.reverse() #reverses the item list, chose not to put this into the sortArray for readability.
			Expected_items = items #sets expected items to be the items on screen
			print(currentWishlist)


			given = OpenWishlistFromName(currentWishlist) #sets given to be the wishlist currentlys aved
			given = self.sortArray(given) #Sorts the given wishlist
			given.reverse() #reverses the given list

			if Expected_items != given: #if items in the list on screen are not the same as the items actually in the list THEN
				#sets error message to "You have unsaved changes!"
				if kwargs['popup']:
					ErrorPopup.ErrorMessage = "You have unsaved changes!"
					#opens the error popup
					LoginScreen().openErrorPopup()
				return False
			else:
				return True
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
		if self.checkIfSaved(popup = True) == False: #checks if the wishlist has been saved before placing a new wishlist , with the popup kwarg as true, meainng that if the focused wishlist hasnt been saved, a popup will show, informing the user that they have unsaved changes.
			return
		elif wishlist_name == "": #if currentwishlist is none, dont return
			return

		#------------UPDATING SCREEN WITH BUTONS AND NAME----------------
		'''This block of code places the name of the wishlist as a heading, places the items button for the top of the wishlist, scrolls the wishlist scroll view to the top, and makes the save button and share button visible'''
		currentWishlist = wishlist_name #sets current wishlist to wishlist_name
		try:
			self.ids.WishlistNameLabel.text = str("{" + wishlist_name.replace("_"," ")+"}") #replaces _ with " " if there is an _ in the name (for aesthetics)
		except:
			self.ids.WishlistNameLabel.text = str("{" + wishlist_name +  "}") #just places the wishlsitname on screen with the { } as decorations
		self.ids.ItemsButton.opacity = 1 #makes the items header visible
		self.ids.ScrollView.scroll_y = 1 #makes scroll view scroll to top
		self.ids.ShareButton.opacity = 1 #makes share button visible
		self.ids.SaveButton.opacity = 1 #makes save button visible
		self.ids.WishlistNameLabel.opacity = 1 #makes heading visible


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
				hint_text_color = rgba_white,
				multiline = False)
			self.ids.ItemsGrid.add_widget(TI) #adds text input to the grid

	def PlaceWishlistNames(self, *args, **kwargs):
		'''

		PlaceWishlistNames(edit wipe)
		'''
		global namesPlaced #imports the namesPlaced variable so we can change it to true once the names are placed
		list_wishlists = glob.glob("Wishlists/*.csv") #gets list of wishlists
		names = [] #sets names to empty list


		filenamePattern = re.compile(r'\/.*-') #regex pattern to find name of wishlist in the filename

		self.ids.NamesGrid.clear_widgets()


		layout = self.ids.NamesGrid

		layout.bind(minimum_height=layout.setter('height'))#sets minium height to the layouts height, allows for scrolling
		#adds each name of the of each of the wishlists  in the list of wishlists.
		for item in list_wishlists:
			print(item)
			emailInFile = validEmail.search(item).group(0)[:-4] #gets the email adress in the filename
			if validWishlistName.search(item) is not None and item not in deleted:
				#conditional makes sure only the user's who is logged in wishlist's are displayed
				if emailInFile == API.emailAddr:
					wishlist_name = filenamePattern.findall(item)[0][1:-1]
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
						btn.bind(on_press = partial(self.PlaceWishlistItems, wishlist_name)) #binds the placewishlistItems function to thebuton
						btn.background_color = rgba_lightblue #sets the background to lightblue
					#if edit is a kwargument then:
					else:
						#set buton press to delete the wishlist, rather than display the wishlist
						btn.bind(on_press= partial(self.deleteWishlist, wishlist_name))
						#changes the background_color to red, for visual, that you are deleting if you click.
						btn.background_color = (1,0,0,1)
					self.ids.NamesGrid.add_widget(btn)
		namesPlaced = True

	def editWishlists(self):
		''' Makes wishlists delete themselves upon button click '''
		#clears the
		self.ids.NamesGrid.clear_widgets()
		self.PlaceWishlistNames(edit=True)

	def deleteWishlist(self, wishlist_name, *args):
		global wishlist_to_be_deleted
		wishlist_to_be_deleted = wishlist_name
		self.parent.current = "deleteWishlist"


	#---------------------------------------------------------------------------------------------
	#									Button press functions
	#---------------------------------------------------------------------------------------------
	'''
		It's worth noting that writing individual functiosn for on_press and on_release of each buton seems messy, it actually allows for increased maintainabily and possibility of expansion.

		For example, currently when you release the buton, all it does is change the image source back to normal, which could easily be done in kivy, without the need for a function specifically to be called when the buton released, however, if in future I wanted to make it change the picture AND move it AND do something else, I would then have to write a function called when the buton was released. In pre-defining these functions, I'm saving myself time in the case of possible expansion.
	'''
	#---- SAVE BUTTON-----
	def animateUpdatedText(self):
		anim  = Animation(opacity = 0, duration=0.01) + Animation(color=(1,0,0,0), duration=0.3) #flashes red
		anim += Animation(opacity = 1, duration=0.1) + Animation(color=(1,0,0,1), duration=1)#flashes red
		anim += Animation(opacity = 0, duration=0.1) + Animation(color=(1,0,0,0), duration = 0.3)
		anim.repeat = False #makes it so it doesnt continually flash and hurt someones eyes-- User suggestion
		anim.start(self.ids.updatedInfo) #starts the animation

	def pressed_save_button(self):
		self.ids.SaveButton.source = "../assets/saveicon_down.png" #sets image to the "down" version
		if not self.checkIfSaved(popup=False): #if the wishlist is not already saved then save it
			try:
				self.ids.updatedInfo.text = "Saving Wishlist"
				self.animateUpdatedText()
				time.sleep(1)
				self.CreateWishlist() #calls the CreateWishlist function, SAVING THE FILE LOCALLY
				Functions().call_save_wishlist()
				self.ids.updatedInfo.text = "Wishlist Saved!"
			except Exception as e:
				print(e)
				traceback.print_exc()
				self.ids.updatedInfo.text = "An error occurred while saving your wishlist!"
			#
		else:
			self.ids.updatedInfo.text = "This wishlist is already saved!"
		#starts the animation
		self.animateUpdatedText()

	def released_save_button(self):
		self.ids.SaveButton.source = "../assets/saveicon.png" #sets image back to normal

	#--SHARE BUTTON---

	def pressed_share_button(self):
		self.parent.current = "ShareWishlist"

	def released_share_button(self):
		self.ids.ShareButton.source = "../assets/shareicon.png" #sets image back to normal image

	#----NEW WISHLIST BUTTON -----
	def pressed_new_wishlist_button(self):
		self.ids.NewWishlist.source = "../assets/plusbutton_down.png" #sets the image to the 'down' version
		self.parent.current = "NewWishlist" #changes the screen to the NewWishlist screen

	def released_new_wishlist_button(self):
		self.ids.NewWishlist.source = "../assets/plusbutton.png" #sets the image to the normal image

	#---EDIT WISHLIST BUTTON-------

	def pressed_edit_button(self):
		#sets image to the edit icon down image
		self.ids.EditWishlists.source = "../assets/editicon_down.png"
		global editMode
		#makes use of a binary switch to determine if edit mode is on or not. If edit mode is "On" and thebuton is clicked, then edit mode is turned off, and set to False. Vice versa
		if editMode:
			self.ids.EditModeText.opacity = 0 #makes the EDIT MODE text visible
			self.ids.ReloadButton.opacity = 1 #makes the reload Button visible
			self.PlaceWishlistNames(edit=False) #calls the PlaceWishlistNames with edit kwarg being False
			editMode = False #sets editMode switch to False

		else:
			self.ids.EditModeText.opacity = 1 #makes the EDIT MODE text visible
			self.ids.ReloadButton.opacity = 0 #makes the reloadButton invisible
			self.editWishlists() #calls the editWishlists function
			editMode = True #sets editMode switch to true

	def released_edit_button(self):
		self.ids.EditWishlists.source = "../assets/editicon.png"

	#----RELOAD WISHLIST BUTTON -----
	def pressed_reload_wishlist_button(self):
		self.ids.ReloadButton.source = "../assets/reloadicon_down.png"
		Functions().call_reload_wishlists() #checks server for any new wishlists
		self.PlaceWishlistNames(edit=False) #re places the wihslist
		self.PlaceWishlistItems(currentWishlist)

	def released_reload_wishlist_button(self):
		self.ids.ReloadButton.source = "../assets/reloadicon.png"

class SharedWishlists(Screen):
	def on_enter(self):
		#imports the global editMode
		self.ids.EditModeText.opacity = 0 #makes the EDIT MODE text dissapear
		self.ids.ReloadButton.opacity = 1 #makes the reloadbutton appear
		self.ids.EditWishlists.opacity = 0 #makes the editButton dissapear
		self.ids.backButton.opacity = 0 #makes the back button dissapear
		self.ids.ItemsButton.opacity =0 #makes the Items button dissapear
		self.ids.WishlistNameLabel.text = "" #makes the text an empty string


		self.PlaceWishlistUsers() #callPlaceWishlistNames with edit kwarg as false
		self.ids.ItemsGrid.clear_widgets() #COMMENTED

	def PlaceWishlistItems(self,wishlist_name, *args): #COMMENTED
		'''Locates, opens and outputs the contents of a wishlist given its name. Places the
		items on the screen displays the wishlists name and displays the share and save buttons. '''

		#had to copy and paste the function, rather than calling the function already defined in myWishlsits, or it would break and the wishlists would not be displayed properly. Likely to do with an issue with ID referencing from another screen.
		global currentWishlist #imports the global current wishlist variable
		global targetUser #imports the global target user variable
		global targetEmail #imports the global target email variable

		#------------UPDATING SCREEN WITH BUTONS AND NAME----------------
		'''This block of code places the name of the wishlist as a heading, places the items button for the top of the wishlist, scrolls the wishlist scroll view to the top, and makes the save button and share button visible'''
		currentWishlist = wishlist_name #sets current wishlist to wishlist_name
		try:
			self.ids.WishlistNameLabel.text = str("{" + wishlist_name.replace("_"," ")+"}") #replaces _ with " " if there is an _ in the name (for aesthetics)
		except:
			self.ids.WishlistNameLabel.text = str("{" + wishlist_name +  "}") #just places the wishlsitname on screen with the { } as decorations

		#defines the items button with the following parameters:
		self.ids.ScrollView.scroll_y = 1 #makes scroll view scroll to top
		self.ids.UserNameLabel.text = targetUser #sets the UserNameLabel to the target user's name
		self.ids.ItemsButton.opacity = 1 #makes the items button visible

		#-------------PLACING WISHLIST ON SCREEN-----------------
		'''This block of code places the wishlist items in text inputs INSIDE the scroll view on the screen. '''
		items = [] #sets items to []
		pattern = re.compile(r'\/.*-') #regex pattern to find name of string given CSV filename
		self.ids.ItemsGrid.clear_widgets() #Removes existing wishlist from screen
		layout = self.ids.ItemsGrid #sets layout to the GridLayout
		layout.bind(minimum_height=layout.setter('height')) #sets grid to minimum height, allows for scrolling
		wishlist_path = "Wishlists/"+wishlist_name + "-" +targetEmail+'.csv'  #sets wishlist path given the wishlist name and email adress
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
			#defines the text input widget, with all the following parameters
			TI = TextInput(
				text = text,
				size_hint = (None, None),
				size = (Window.size[0],Window.size[1]/24),
				background_color = rgba_darkblue,
				foreground_color = rgba_white,
				hint_text_color = rgba_white,
				disabled = True,
				disabled_foreground_color = rgba_white

				)
			self.ids.ItemsGrid.add_widget(TI) #adds text input to the grid

	def PlaceWishlistNames(self, *args, **kwargs): #COMMENTED
		'''

		PlaceWishlistNames(edit wipe)
		'''
		global namesPlaced #imports the namesPlaced variable so we can change it to true once the names are placed
		global targetUser #imports global targetUser variable
		global targetEmail #imports global targetEmail variable
		list_wishlists = glob.glob("Wishlists/*.csv") #gets list of wishlists
		names = [] #sets names to empty list
		#sets the regex conditions for a valid Wishlist name



		filenamePattern = re.compile(r'\/.*-') #regex pattern to find name of wishlist in the filename
		#self.SetData(args[0].strip())
		with open("userdata/users.csv") as f:
			#defines a DictREader for the csv file
			reader = csv.DictReader(f)
			#go through each row in the file, if the user is equal to the user passed to the function, then set that user and email to be the target user and email respectfully
			for row in reader:
				if row['user'].strip() == args[0]:
					targetUser = row["user"].strip()
					targetEmail = row["email"].strip()

		self.ids.NamesGrid.clear_widgets() #clears widgets from NamesGrid
		self.ids.backButton.opacity = 1 #makes back button visible
		self.ids.EditWishlists.opacity = 1 #makes EditWishlists buton visible

		layout = self.ids.NamesGrid #sets layout to be self.ids.NamesGrid

		layout.bind(minimum_height=layout.setter('height'))#sets minium height to the layouts height, allows for scrolling
		#adds each name of the of each of the wishlists  in the list of wishlists.

		#for each wishlist pathname:
		for item in list_wishlists:

			#emailInFile is the email adress found in the filename of the wishlist currently being looked at

			#target is the email adress that was passed to the function as an argument, ie it is a SPECIFIC user's email, the root user wants to see every wishlist by that user.

			#the loop then checks through ALL wishlists filenames, and IF wishlist was written by the desired user (ie if filename contains targetEmail) then place it on screen.

			#finds the email adress in the filename using regex and string splicing to remove the .csv
			emailInFile = validEmail.search(item).group(0)[:-4]
			#if the wishilst was written by user whos button was clicked:
			if targetEmail == emailInFile:
				#gets the wishlist name from the filename using regex
				wishlist_name = filenamePattern.findall(item)[0][1:-1]
				#replaces the underscores with space, sets the wishlist_name_displayed
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
					btn.bind(on_press = partial(self.PlaceWishlistItems, wishlist_name)) #binds the placewishlistItems function to thebuton
					btn.background_color = rgba_lightblue #sets the background to lightblue
				#if edit is a kwargument then:
				else:
					#set buton press to delete the wishlist, rather than display the wishlist
					btn.bind(on_press= partial(self.deleteWishlist, wishlist_name))
					#changes the background_color to red, for visual, that you are deleting if you click.
					btn.background_color = (1,0,0,1)
				#adds the button to the namesGrid
				self.ids.NamesGrid.add_widget(btn)
		#sets namesplaced to true, for maintainabily
		namesPlaced = True

	def PlaceWishlistUsers(self, *args, **kwargs):
		#imports global targetEmail
		global targetEmail
		#imports global targetUser
		global targetUser
		list_wishlists = glob.glob("Wishlists/*.csv") #gets list of wishlists
		names = [] #sets names to empty list
		users = [] #sets users to empty list
		#sets regex conditions for valid

		filenamePattern = re.compile(r'\/.*-') #regex pattern to find name of wishlist in the filename
		self.ids.NamesGrid.clear_widgets()
		layout = self.ids.NamesGrid #sets layout to the names Grid

		layout.bind(minimum_height=layout.setter('height'))#sets minium height to the layouts height, allows for scrolling
		#adds each name of the of each of the wishlists  in the list of wishlists.


		for item in list_wishlists:
			try:
				#searches the item
				sent_from = validEmail.search(item)
				#identifies the email, the string slicing removes the .csv from the end
				sent_from = sent_from.group(0)[:-4]
				sent_from.strip()
			except:
				sent_from = ""
				#TODO chuck exception
			'''Find the email_address, match it to a user in users.csv, and append the user to the users list'''
			with open('userdata/users.csv') as f:
				reader = csv.DictReader(f)
				for row in reader: #for every row in the file)

					#if the email in the row is the email in the file AND the user of that email is not already in the users list AND the user is not the user logged in, THEN add them to the users list
					if row["email"]== sent_from and row["user"].strip() not in users and row['email'] != API.emailAddr:
							global ViewingTargetsEmail

							#strips the new line and indentation
							users.append(row["user"].strip())

		for user in users:
			#define the buton with the text to be the users name
			btn = Button(
				text = user,
				size_hint = (None, None),
				size = (Window.size[0]/8,Window.size[1]/24),
				halign = 'center',
				color = (0,0,0,1))
			#sets button press to call the placeWishlist Names function
			btn.bind(on_press = partial(self.PlaceWishlistNames, user, edit = False))
			#sets background color to blue
			btn.background_color = rgba_lightblue
			self.ids.NamesGrid.add_widget(btn)

	def editWishlists(self):
		''' Makes wishlists delete themselves upon button click '''
		#clears the
		self.ids.NamesGrid.clear_widgets()
		self.PlaceWishlistNames(edit=True)

	def deleteWishlist(self, wishlist_name, *args):
		global wishlist_to_be_deleted
		wishlist_to_be_deleted = wishlist_name
		self.parent.current = "deleteWishlist"



	#---------------------------------------------------------------------------------------------
	#									Button press functions
	#---------------------------------------------------------------------------------------------
	'''
		It's worth noting that writing individual functiosn for on_press and on_release of each buton seems messy, it actually allows for increased maintainabily and possibility of expansion.

		For example, currently when you release the buton, all it does is change the image source back to normal, which could easily be done in kivy, without the need for a function specifically to be called when the buton released, however, if in future I wanted to make it change the picture AND move it AND do something else, I would then have to write a function called when the buton was released. In pre-defining these functions, I'm saving myself time in the case of possible expansion.
	'''
	#---EDIT WISHLIST BUTTON-------

	def pressed_edit_button(self):
		#sets image to the edit icon down image
		self.ids.EditWishlists.source = "../assets/editicon_down.png"
		global editMode
		#makes use of a binary switch to determine if edit mode is on or not. If edit mode is "On" and thebuton is clicked, then edit mode is turned off, and set to False. Vice versa
		if editMode:
			self.ids.EditModeText.opacity = 0 #makes the EDIT MODE text visible
			self.ids.ReloadButton.opacity = 1 #makes the reload Button visible
			self.PlaceWishlistNames(edit=False) #calls the PlaceWishlistNames with edit kwarg being False
			editMode = False #sets editMode switch to False

		else:
			self.ids.EditModeText.opacity = 1 #makes the EDIT MODE text visible
			self.ids.ReloadButton.opacity = 0 #makes the reloadButton invisible
			self.editWishlists() #calls the editWishlists function
			editMode = True #sets editMode switch to true

	def released_edit_button(self):
		self.ids.EditWishlists.source = "../assets/editicon.png"

	#----RELOAD WISHLIST BUTTON -----
	def pressed_reload_wishlist_button(self):

		self.ids.ReloadButton.source = "../assets/reloadicon_down.png"

		Functions().call_reload_shared_wishlists() #checks server for any new wishlists

		self.PlaceWishlistNames(edit=False) #re places the wihslist


		#if user presses reload_reload_wishlist before they have clicked on a wishlist, then it will be unable to place the wishlist, meainng that it will crash. Try/except catches the exception
		try:
			self.PlaceWishlistItems(currentWishlist)
		except:
			pass

	def released_reload_wishlist_button(self):
		self.ids.ReloadButton.source = "../assets/reloadicon.png"

	#----BACK  BUTTON -----
	def pressed_back_button(self):
		self.ids.backButton.source = "../assets/rightarrow_down.png"
		self.PlaceWishlistUsers()
		self.ids.EditWishlists.opacity = 0
		self.ids.backButton.opacity = 0
		self.ids.UserNameLabel.text = ""

	def released_back_button(self):
		self.ids.backButton.source = "../assets/rightarrow.png"

class DeleteScreen(Screen):
	Message = "Are you sure you want\n to delete this wishlist?" #cant import the actual name for some reason :/
	def deleteWishlist(self):
		wishlist_name = wishlist_to_be_deleted
		try:
			wishlist_name = wishlist_name.replace(" ","_") #if the name contains an underscore, replace it with a space
		except:
			pass
		filepath ="Wishlists/"+wishlist_name + "-" +ViewingTargetsEmail+'.csv'
		deleted.append(filepath)
		os.remove(filepath) #deletes the wishlist
		self.parent.current = "MyWishlists"

class NewWishlistScreen(Screen):
	def CreateWishlist(self, wishlist_name):
		if len(wishlist_name) < 10: #restriction on wishlist_name length , has to be less than 10 characters
			MyWishlists().CreateWishlist(wishlist_name)
			MyWishlists().PlaceWishlistNames(edit=False)
			self.parent.current = 'MyWishlists' #changes screen to MyWishlists
			self.ids.WishlistNameInput.text = "" #resets the text input to "" so it looks empty when they create a new wishlist
		else:
			self.ids.MessageLabel.text = "Please make sure your wishlist name is < 10 characters long!"

class ShareWishlistScreen(Screen):
	def share_wishlist(self, to_addr):
		Functions().call_share_wishist(to_addr)
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
