from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import kivy.properties as Properties
from kivy.lang import Builder
import random
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Window.clearcolor=(1,1,1,1)

class ClickableButton(Button):
    def __init__(self,**kwargs):
        super(ClickableButton, self).__init__(**kwargs)
        self.mouse_button = None #mouse_button records what button is pressed
        self.bind(on_touch_down = self.callback_touch_down) #set up a function to be called on mouse events
    def callback_touch_down(self, instance, touch):
        self.mouse_button = touch.button #record what button is clicked on touch down on mouse events

def callback(instance):
    print('The <%s> button is being pressed' % instance.mouse_button)


class myLayout(Screen):
    #bombs_left = 0
    def __init__(self,**kwargs):
        super(myLayout,self).__init__(**kwargs)
        self.box = myBox(orientation='vertical',spacing=10)
        self.add_widget(self.box)
        self.box.label.text='hi'

        print self.box.bombs_left
        Clock.schedule_interval(self.update_bombs_left, 0.1)

    def update_bombs_left(self,time):
        self.box.label.text = str(self.box.myGrid.bombs_left)

class myBox(BoxLayout):
    bombs_left = 0
    box = None
    def __init__(self,**kwargs):
        super(myBox,self).__init__(**kwargs)
        self.myGrid = myGridLayout(size_hint=(1,0.75))
        self.add_widget(self.myGrid)
        button = ClickableButton()
        button.text = "Restart"
        button.size_hint = None,None
        button.size = 100,50
        button.bind(on_release=self.reset)
        self.add_widget(button)
        self.bombs_left = self.myGrid.bombs_left
        self.label = Label(size_hint=(None,None))
        self.label.color = (0,0,0,1)
        #label.bind(text = str(self.update_bombs))
        self.add_widget(self.label)     

    def update_bombs(self):
        print self.bombs_left

    def reset(self,instance):
        self.clear_widgets()
        self.__init__()
        
class myGridLayout(GridLayout):    
    def __init__(self,**kwargs):
        super(myGridLayout,self).__init__(**kwargs)    
        self.cols=10
        self.rows=self.cols
        self.button_grid = []
        self.game_over = False
        self.win = False
        self.spacing = 1
        for row in range(self.cols):
            row_arr = []
            for col in range(self.rows):
                button = ClickableButton()
                button.bind(on_release=self.released)
                button.col = col
                button.row = row
                button.clicked = False
                button.isMine = False
                button.isFlagged = False
                button.background_normal = "white.png"
                button.background_color = (0.62,0.647,0.91,1)
                self.add_widget(button)
                row_arr.append(button)
            self.button_grid.append(row_arr)
        self.grid = [[0 for i in range(10)] for j in range(10)]
        self.num_of_bombs=10
        self.bombs_left = self.num_of_bombs
        bomb_arr = []
        while len(bomb_arr) != self.num_of_bombs:
            bombpos_x = int(random.random()*10)
            bombpos_y = int(random.random()*10)
            if (bombpos_x,bombpos_y) not in bomb_arr:
                bomb_arr.append((bombpos_x,bombpos_y))
            else: print 'duplicate'
        for bomb in bomb_arr: self.grid[bomb[0]][bomb[1]] = "*"
        print self.grid

    def get_adjacent(self,instance):
        row = instance.row
        col = instance.col
        self.button_grid[row][col].clicked = True
        adjacent_arr = []
        count = 0
        if self.grid[row][col] == '*':
            self.button_grid[row][col].isMine = True
            #self.button_grid[row][col].text = self.grid[row][col]
            #self.button_grid[row][col].background_normal = "circle_hit.png"
            self.button_grid[row][col].background_color = (0,0,0,1)
            if not self.game_over:self.win_check(instance)
            return
        for r in range(max(row-1,0),min(row+2,10)): 
            for c in range(max(col-1,0),min(col+2,10)):
                adjacent_arr.append(self.button_grid[r][c])          
                if self.grid[r][c] == '*':
                    self.button_grid[r][c].isMine = True
                    self.button_grid[r][c].color = (0,0,0,1)
                    count = count +1
                self.button_grid[row][col].text = ""
                self.button_grid[row][col].background_color = (0.871,0.875,0.89,1)
        if count > 0 and not self.button_grid[row][col].isMine and not self.button_grid[row][col].isFlagged:
            self.button_grid[row][col].text = str(count)
            if count == 1: self.button_grid[row][col].color = (0,0.118,1,1)
            elif count == 2: self.button_grid[row][col].color = (0.027,0.569,0,1)
            elif count==3: self.button_grid[row][col].color = (1,0.129,0.129,1)
            elif count==4: self.button_grid[row][col].color = (0.576,0,0.639,1)
            elif count==5: self.button_grid[row][col].color = (0.671,0.125,0.039,1)
            elif count==6: self.button_grid[row][col].color = (0, 1, 1,1)
            elif count==7: self.button_grid[row][col].color = (0.98,0.659,0.145,1)
            elif count==8: self.button_grid[row][col].color = (1,1,1,1)
            else:
                self.button_grid[row][col].color = (0,0,0,1)
            return
        for adj in adjacent_arr:
            if not adj.clicked and count<1 and not adj.isFlagged: self.get_adjacent(adj)

    def set_flag(self,instance):
        if instance.isFlagged:
            instance.text = ""
            instance.color = (1,1,1,1)
            self.bombs_left = self.bombs_left+1 
            instance.isFlagged = False           
        elif instance.text == "" and not instance.clicked and not instance.isFlagged:
            instance.text = "|>"
            self.bombs_left = self.bombs_left-1
            instance.color = (0,0,0,1)
            instance.isFlagged = True
        
    def update_bombs_left(self):
        return self.bombs_left

    def released(self,instance):
        if self.game_over: return
        if instance.mouse_button == 'left':
            if instance.isFlagged:return
            if not self.game_over: 
                self.get_adjacent(instance)
                self.win_check(instance)
        elif instance.mouse_button == 'right': 
            self.set_flag(instance)           
        self.update_bombs_left()
        
    def win_check(self,instance):
        flag_count = 0
        if instance.isMine and not instance.isFlagged:
            self.end_game()
        else:
            for r in self.button_grid:
                for c in r:
                    #print self.button_grid[c.row][c.col].isFlagged
                    if (not self.button_grid[c.row][c.col].clicked) or (self.button_grid[c.row][c.col].isFlagged and self.grid[c.row][c.col]=="*"):
                        flag_count = flag_count+1
            if flag_count == self.num_of_bombs:
                self.win = True
                self.end_game()
        print flag_count
        
    def end_game(self):
        self.game_over = True
        for r in self.button_grid:
            for c in r:
                if self.win and self.grid[c.row][c.col] == '*' and self.button_grid[c.row][c.col].isFlagged or self.win and not self.button_grid[c.row][c.col].clicked:
                    self.button_grid[c.row][c.col].background_color = (0.659,0.929,0.624,1)
                    
                elif self.grid[c.row][c.col] == '*' and not self.win:
                    self.button_grid[c.row][c.col].text = "" 
                    #if self.button_grid[c.row][c.col].background_normal != "circle_hit.png":
                        #self.button_grid[c.row][c.col].background_normal = "circle.png"
                    if self.button_grid[c.row][c.col].background_color == [0, 0, 0, 1]:
                        self.button_grid[c.row][c.col].background_color = (0.980, 0.031, 0,1)
                        print 'hi'
                    else:
                        #(0.980, 0.031, 0,1)
                        #(0.89,0.686,0.686,1)
                        self.button_grid[c.row][c.col].background_color = (0.89,0.686,0.686,1)
        print self.win
                    
class myApp(App):
    def build(self):
        return myLayout()
    print App.get_running_app()

if __name__ == "__main__":
    myApp().run()