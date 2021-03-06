from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, StringProperty, \
        NumericProperty, BooleanProperty
from kivy.clock import Clock
from os.path import join, exists

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup

from kivy.garden.navigationdrawer import NavigationDrawer

import json
from settingsjson import general_settings

class NewTextInput(FloatLayout):

    text = StringProperty()
    multiline = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(NewTextInput, self).__init__(**kwargs)
        Clock.schedule_once(self.prepare, 0)

    def prepare(self, *args):
        self.n_textinput = self.ids.n_textinput.__self__
        self.n_label = self.ids.n_label.__self__
        self.view()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            self.edit()
            return True
        return super(NewTextInput, self).on_touch_down(touch)

    def edit(self):
        self.clear_widgets()
        self.add_widget(self.n_textinput)
        self.n_textinput.focus = True

    def view(self):
        self.clear_widgets()
        self.add_widget(self.n_label)

    def check_focus_and_view(self, textinput):
        if not textinput.focus:
            self.text = textinput.text
            self.view()

class MyDrop(DropDown):
    for i in range(5):
        print i

class NoteView(Screen):

    note_index = NumericProperty()
    note_title = StringProperty()
    note_content = StringProperty()
    
    data = ListProperty()

    def args_converter(self, row_index, item):
        return{
                'note_index': row_index,
                'note_content': item['content'],
                'note_title': item['title']}

    def searchbar(self):
        search = self.ids.notes 
        search_bar = BoxLayout(size_hint_y=0.1, orientation='horizontal')
        search_bar.add_widget(Button(text='Button'))
        search_bar.add_widget(TextInput(focus=True))
        search_bar.add_widget(Label(text='Number(?)'))
        search.add_widget(search_bar)

class NoteListItem(BoxLayout):

    note_title = StringProperty()
    note_index = NumericProperty()

class Notes(Screen):
    pass

class IdeasApp(App):
    
    data = ListProperty()

    def args_converter(self, row_index, item):
        return {
                'note_index': row_index,
                'note_content': item['content'],
                'note_title': item['title']}
    
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.notes = Notes(name='notes')
        self.load_notes()
        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.notes)
        return root

    def load_notes(self):
        if not exists(self.notes_fn):
            return
        with open(self.notes_fn, 'rb') as fd:
            data = json.load(fd)
        self.data = data

    def save_notes(self):
        with open(self.notes_fn, 'wb') as fd:
            json.dump(self.data, fd)

    def del_note(self, note_index):
        del self.data[note_index]
        self.save_notes()
        self.refresh_notes()
        self.go_notes()

    def edit_note(self, note_index):
        note = self.data[note_index]
        name = 'name{}'.format(note_index)

        if self.root.has_screen(name):
            self.root.remove_widget(self.root.get_screen(name))

        view = NoteView(
                name=name,
                note_index=note_index,
                note_title=note.get('title'),
                note_content=note.get('content'))

        self.root.add_widget(view)
        self.transition.direction = 'left'
        self.root.current = view.name

    def add_note(self):
        self.data.append({'title': 'New note', 'content': ''})
        note_index = len(self.data) - 1
        self.edit_note(note_index)

    def set_note_content(self, note_index, note_content):
        self.data[note_index]['content'] = note_content
        data = self.data
        self.data = []
        self.data = data
        self.save_notes()
        self.refresh_notes()

    def set_note_title(self, note_index, note_title):
        self.data[note_index]['title'] = note_title
        self.save_notes()
        self.refresh_notes()

    def refresh_notes(self):
        data = self.data
        self.data = []
        self.data = data

    def go_notes(self):
        self.transition.direction = 'right'
        self.root.current = 'notes'

    def build_config(self, config):
        config.setdefaults('General', {'Open_On_Startup': True})

    def build_settings(self, settings):
        settings.add_json_panel('General', self.config, data=general_settings)

    @property
    def notes_fn(self):
        return join(self.user_data_dir, 'note.json')

if __name__ == '__main__':
    IdeasApp().run()
