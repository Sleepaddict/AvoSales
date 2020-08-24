# NOTE to future self on pyinstaller errors:
# 1) try compiling pyinstaller in a conda env with older python versions
# 2) conda install all the needed modules for app in that env
# 3) create a cli.py file outside of everything else
# 4) update cli.spec file generated the first time by pyinstaller
# add the datafiles collector function to cli.spec
# to ensure/import the relevant folders into the final .exe
# 5) activate the conda env and run pyinstaller from within it, POINT TO .spec file
# https://realpython.com/pyinstaller-python/
# https://stackoverflow.com/questions/57253470/python-ssl-import-error-in-pyinstaller-generated-executable
# https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Collect-Data-Files

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window 
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
import database

# MyLabel not really needed i think...
class MyLabel(Label):       #so that we can customise and ensure the user interface is consistent(in terms of size etc)

    def __init__(self, **kwargs):
        Label.__init__(self, **kwargs)
        self.bind(size=self.setter('text_size'))
        self.padding = (20, 20)
        
class UI(GridLayout):
    def __init__(self, **kwargs):
        super(UI,self).__init__(**kwargs)
        
        # initialize this so that we can access later on
        self.region = ""
        
        # change background color of app
        Window.clearcolor = (1,1,1,1)
        
        # By default, the size_hint is (1, 1), so a Widget will take the full size of the parent
        # here we want to make the top section narrower
        top_layout = GridLayout(cols = 3, 
                                size_hint_y = 0.2) 
        self.add_widget(top_layout)
        
        # add a placeholder image for the bottom section when app is first started
        # using self so that can access the image source and update later
        self.wimg = Image(source = 'images/Seeds in a Pot Final Version Updated.png')
        self.add_widget(self.wimg)
        
        # add label and dropdown to top (selection)
        l1 = MyLabel(text="Select Region", 
                     font_size=24,
                     #halign='left', 
                     valign='middle',
                     color = (0,0,0,1))
        top_layout.add_widget(l1)
        
        dropdown = DropDown()
        # makes use of imported module function
        region_list = database.get_regionlist(database.create_connection())
        # create an option for all the regions possible
        for index in region_list:
            btn = Button(text=index,
                         color = (0,0,0,1),
                         size_hint_y=None, 
                         height=44,
                         background_normal = '',
                         background_color = (0.7,0.7,0.9,0.9)
                         )
            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        # create a big main button for the dropdown (i think dropdown is somehow binded to it)
        # i used self.mainbutton here so that set_region can update its text, if not mainbutton will be undefined
        self.mainbutton = Button(text="Pls select region",
                                 color = (0,0,0,1),
                            font_size=18,
                            halign='left', 
                            valign='middle',
                            #change the button appearance
                            background_normal = 'images/button_normal.png',
                            background_down = 'images/button_down.png'
                            )
        self.mainbutton.bind(on_release=dropdown.open)
        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        dropdown.bind(on_select=self.set_region)

        top_layout.add_widget(self.mainbutton)
        
        # add confirm button next to dropdown
        cfm_btn = Button(text="Confirm",
                         color = (0,0,0,1),
                         font_size = 18, 
                         size_hint_x = 0.2,
                         background_normal = 'images/button_normal.png',
                         background_down = 'images/button_down.png')
        cfm_btn.bind(on_release = self.query) # makes use of imported module function
        top_layout.add_widget(cfm_btn)
        
    def set_region(self,instance, text):
        self.mainbutton.text = text
        self.region = text
        
    # makes use of imported module function
    def query(self, instance):
        conn = database.create_connection()
        
        database.query_sales_by_region(conn, self.region)
        self.wimg.source = 'images/' + self.region + '.png' 


class Visualizer(App):

    def build(self):
        return UI(rows = 2)
        
if __name__ == '__main__':
    Visualizer().run()