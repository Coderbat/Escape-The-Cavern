'''
This file contains the logic for the game
'''
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class Logic:
    '''
    This class contains the main logic for the game
    '''

    def __init__(self,game_conditions,height,width):
        self.height = height
        self.width = width
        self.game_conditions = game_conditions
        self.halt_right = False
        self.halt_left = False
        self.jump = 0
        self.moving_id = None
        self.platform_direction = 'right'

    def overlapping(self,rect1, rect2):
        '''
        This function checks if two rectangles are overlapping
        '''
        if (rect1[0] < rect2[2] and rect1[2] > rect2[0] and
            rect1[1] < rect2[3] and rect1[3] > rect2[1]):
            return True
        return False

    def falling(self,char_position,game_conditions):
        '''
        This function checks if the character is falling
        '''
        above_platform = False
        if self.map_edge(char_position) and char_position[1] < (self.height*3/4) - 50:
            return True
        if 'platform' in game_conditions:
            for _,platform_cords in game_conditions['platform'].items():
                mid = False
                if char_position[2] > (platform_cords[0]+platform_cords[2])//2:
                    mid = True
                if self.overlapping(char_position, platform_cords): #checking if the character is on top the platform)
                    if char_position[3] <= platform_cords[1] + 1 :
                        above_platform = True
                    if char_position[2] >= platform_cords[0] and above_platform is False and mid is False:
                        self.halt_right = True
                    if char_position[0] <= platform_cords[2] and above_platform is False and mid is True:
                        self.halt_left = True
                    if char_position[1]<=platform_cords[3] and above_platform is False:
                        self.jump = 0
                        return True
                    if char_position[3] < platform_cords[1] + 1 \
                        and char_position[2]> platform_cords[0] \
                        and char_position[0] < platform_cords[2] :
                        return False
                    else:
                        return True
        if 'water' in game_conditions:
            for water_coords in game_conditions['water']:
                if self.overlapping(char_position,water_coords):
                    if char_position[0]> water_coords[0] \
                        and char_position[2]<water_coords[2]:
                        if int(char_position[3]) == int(water_coords[3]):
                            return False
                        return True
        
        if char_position[1] < (self.height*3/4) - 50:
            return True
    def drowning(self,char_position,game_conditions):
        '''
        This function checks if the character is drowning   
        '''
        if 'water' in game_conditions:
            for water in game_conditions['water']:
                if self.overlapping(game_conditions['water_start'][tuple(water)],char_position):
                    self.halt_left = True
                elif self.overlapping(game_conditions['water_end'][tuple(water)],char_position):
                    self.halt_right = True
                else:
                    self.halt_right = False
                    self.halt_left = False
            for water_coords in game_conditions['water']:
                if self.overlapping(char_position,water_coords):
                    return True
        else:
            self.halt_left = False
            self.halt_right = False
        return False

    def map_edge(self,char_position):
        '''
        This function checks if the character is at the edge of the map
        '''
        if char_position[0] < 0:
            self.halt_left = True
            return True
        else:
            return False

    def moving_platform(self,game_conditions,canvas,keys_status):
        '''
        This function moves the moving platforms
        '''
        if keys_status['escape'] is False:
            for platform,platform_cords in game_conditions['platform'].items():
                if len(platform_cords) == 0:
                    return
                if 'moving' in game_conditions:
                    if platform in game_conditions['moving']:
                        start = game_conditions['moving'][platform][0]
                        end = game_conditions['moving'][platform][1]
                        if platform_cords[0] <= start:
                            self.platform_direction = 'right'
                        elif platform_cords[2] >= end:
                            self.platform_direction = 'left'
                        if self.platform_direction == 'right':
                            canvas.move(platform,10,0)
                        elif self.platform_direction == 'left':
                            canvas.move(platform,-10,0)
                        platform_cords = canvas.coords(platform)
                        game_conditions['platform'][platform] = platform_cords
        self.moving_id = canvas.after(100,lambda: self.moving_platform(game_conditions,canvas,keys_status))


class Controls:
    '''
    This class contains the logic for the controls
    '''
    button_pressed = False
    right_key = 'right'
    left_key = 'left'
    up_key = 'up'

    def __init__(self, root, canvas,key_text):
        self.root = root
        self.canvas = canvas
        self.control_key = None
        self.text_id = None
        self.text_key = None
        self.button_window = None
        self.button_text_id = None
        self.key_text = key_text
        self.keys_status = {}
        self.x = 0
        self.y = 0

    def on_key_press(self, event):
        '''
        This function is called when a key is pressed it saves it as the control key
        '''
        self.control_key = event.keysym.lower()
        self.canvas.delete(self.text_id)
        if self.text_key is not None:
            self.canvas.delete(self.text_key)
        self.text_key = self.canvas.create_text(self.x + 200, self.y, text=self.control_key.upper(),font=("Helvetica", 20, "bold"))
        Controls.button_pressed = False
        self.root.unbind("<Key>")


    def place_button(self, x, y, image_path, width, height):
        '''
        This function places a button on the canvas
        '''
        image = Image.open(image_path)
        resized_image = image.resize((width, height))
        tk_image = ImageTk.PhotoImage(resized_image)
        control_button = tk.Button(self.root, image=tk_image, command=lambda: self.on_button_click(x,y))
        control_button.image = tk_image
        self.button_window = self.canvas.create_window(x, y, window=control_button)
        self.button_text_id = self.canvas.create_text(x +200, y, text=self.key_text.upper(),font=("Helvetica", 20, "bold"))
        self.x = x
        self.y = y

    def on_button_click(self,x,y):
        '''
        This function is called when the button is clicked it prompts the user to press a key
        '''
        if Controls.button_pressed:
            return
        Controls.button_pressed = True
        if self.key_text:
            self.canvas.delete(self.button_text_id)
        if self.text_id:
            self.canvas.delete(self.text_id)
        if self.text_key:
            self.canvas.delete(self.text_key)
        self.text_id = self.canvas.create_text(x+200, y, text="Press a key.",font=("Helvetica", 16, "bold"))
        self.root.bind("<Key>", self.on_key_press)

    @staticmethod
    def check_key(right,left,up):
        '''
        This function checks if the keys are valid
        '''
        reserved_keys = ['escape','b']
        previous_keys = [Controls.right_key,Controls.left_key,Controls.up_key]
        given_keys = [right,left,up]
        for key in given_keys:
            if key not in previous_keys and key in reserved_keys :
                key = key.upper()
                messagebox.showerror("Error", f"{key} Key already in use, Please select another key")
                return False
        if right in [left,up] and right is not None:
            messagebox.showerror("Error", "All keys must be different")
            return False
        elif left in [right,up] and left is not None:
            messagebox.showerror("Error", "All keys must be different")
            return False
        elif up in [right,left] and up is not None:
            messagebox.showerror("Error", "All keys must be different")
            return False
        return True
    
    @staticmethod
    def update_keys(right,left,up):
        '''
        This function updates the keys
        '''
        if right is not None:
            Controls.right_key = right
        if left is not None:
            Controls.left_key = left
        if up is not None:
            Controls.up_key = up


