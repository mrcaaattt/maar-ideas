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

Builder.load_file('https://raw.githubusercontent.com/mrcaaattt/maar-ideas/master/main.kv')

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
