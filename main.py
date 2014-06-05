from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.garden.navigationdrawer import NavigationDrawer

Builder.load_string("""

<Notes@BoxLayout>: 
	top_layout: topLayout
	space_text: spacetext
	quick_settings: quicksettings
		
	orientation: "vertical" 
	BoxLayout:
		id: topLayout
		height: "40dp"
		size_hint_y: None
		pos_hint: {'top': 1}
		Button:
			text: "Settings"
			size_hint_x:0.1
			on_release: root.manager.current = 'settings'
#		Button:
#			text: "Notes"
#			size_hint_x:0.9
#			on_release: root.drop_down.open(self)

	BoxLayout:
		padding: 0, 40
		id: spacetext
		NavigationDrawer:
			anim_type: 'reveal_below_simple'
			BoxLayout:
				orientation: 'vertical'
				Button:
					text: 'press me'
				Label:
					text: 'do it please'
				Button: 
					text: 'you will not regret'
					
			Carousel:
				loop: False
				#size_hint_x: .85
				ScrollView:
					id: scrlv
					size_hint_x: 1
					TextInput:
						size_hint: 1, None
						height: max(self.minimum_height, scrlv.height)
				ScrollView:
					id: scrlv
					size_hint_x: 1
					TextInput:
						size_hint: 1, None
						height: max(self.minimum_height, scrlv.height)	
		
				ScrollView:
					id: scrlv
					size_hint_x: 1
					TextInput:
						size_hint: 1, None
						height: max(self.minimum_height, scrlv.height)
					
				ScrollView:
					id: scrlv
					size_hint_x: 1
					TextInput:
						size_hint: 1, None
						height: max(self.minimum_height, scrlv.height)
					
	BoxLayout:
		id: quicksettings
		height:'40dp'
		size_hint_y:None
		Button:
		Label:

<SettingsScreen>:
	BoxLayout:
		Label:
			text: "This is the settings"
		Button:
			text: "Back"	
			on_release: root.manager.current = 'home'
		
<ToDoScreen>:
	BoxLayout:
		height: "40dp"
		size_hint_y: 1, 0.5
		pos_hint: {'x': 0, 'y': .93}
		Button:
			text: "Settings"
			size_hint_x:0.1
			on_release: root.manager.current = 'settings'
		Button:
			text: "Notes"
			size_hint_x:0.9
			on_release: root.drop_down.open(self)
			
	Label:
		text: 'To do a to-do'
	
	BoxLayout:
		height:'40dp'
		size_hint_y:None
		Button:
		Label:

<SketchScreen>:
	BoxLayout:
		height: "40dp"
		size_hint_y: 1, 0.5
		pos_hint: {'x': 0, 'y': .93}
		Button:
			text: "Settings"
			size_hint_x:0.1
			on_release: root.manager.current = 'settings'
		Button:
			text: "Notes"
			size_hint_x:0.9
			on_release: root.drop_down.open(self)

	Label: 
		text: 'Sketch space'

	BoxLayout:
		height:'40dp'
		size_hint_y:None
		Button:
		Label:
							
<MyDrop>:
	Button:
		text: 'Notes'
		size_hint_y: None
		height: 40
		on_release: root.manager.current = 'home'
	Button:
		text: 'To-do'
		size_hint_y: None
		height: 40
		on_release: root.manager.current = 'todo'
	Button:
		text: 'Sketch'
		size_hint_y: None
		height: 40
		on_release: root.sm.current = 'sketch'

""")

class MyDrop(DropDown):
	for i in range(5):
		print i

class Notes(Screen, BoxLayout):
	top_layout = ObjectProperty(None)
	TextSpace = ObjectProperty(None)
	quick_settings = ObjectProperty(None)
	
	def __init__(self, *args, **kwargs):
		super(Notes, self).__init__(*args, **kwargs)
		self.drop_down = MyDrop()
		
		dropdown = DropDown()
		notes = ["Notes", "Sketch", "To-do"]
		for note in notes:
			btn = Button(text='%r' % note, size_hint_y=None, height=40)
		
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))
			
			dropdown.add_widget(btn)
		
		mainbutton = Button(text='Notes', size_hint=(1, 1))
		mainbutton.bind(on_release=dropdown.open)
		
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
		
		self.top_layout.add_widget(mainbutton)
	
class SettingsScreen(Screen):
	pass
	
class ToDoScreen(Screen):
	pass
	
class SketchScreen(Screen):
	pass
	
sm = ScreenManager(transition=SlideTransition(direction='up'))

sm.add_widget(Notes(name='home'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(ToDoScreen(name='todo'))
sm.add_widget(SketchScreen(name='sketch'))

class MyApp(App):
	def build(self):
		return sm

if __name__ == '__main__':
	MyApp().run()
