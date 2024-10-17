'''
This file contains the classes used to create animations in the game.
'''
import tkinter as tk
from PIL import Image, ImageTk

class AnimateCoin:
    '''
    This class is used to animate the coin. The gif is divided into multiple images and then displayed one after the other.
    This works by deleting the previous image and replacing it with the next image.
    '''
    def __init__(self, root, x, y, delay, canvas, size):
        self.root = root
        self.x = x
        self.y = y
        self.delay = delay
        self.size = size
        self.images = []
        self.canvas = canvas
        self.image_file = 'images/coin.gif'
        self._after_id = None
        self._disappear_coin_id = None
        self.collected = False
        image = Image.open(self.image_file)
        frames = image.n_frames
        for i in range(frames):
            image.seek(i)
            resized_image = image.resize(self.size)
            photo = ImageTk.PhotoImage(resized_image)
            self.images.append(photo)
        self.canvas.pack()
        self.image_on_canvas = None
        self.show_frame(0)

    def show_frame(self, count):
        '''
        This function is used to display the next image in the gif to make an animation effect.
        '''
        img = self.images[count]
        if self.image_on_canvas is not None:
            self.canvas.delete(self.image_on_canvas)
        self.image_on_canvas = self.canvas.create_image(self.x, self.y, image=img)
        self._after_id = self.root.after(self.delay, lambda: self.show_frame((count+1) % len(self.images)))

    def stop(self):
        '''
        This function takes the coin to the top then deletes it
        '''
        if self._after_id is not None:
            if self.y > -60:
                self.canvas.move(self.image_on_canvas, 0, -30)
                self.y -= 30
                self._disappear_coin_id = self.root.after(self.delay, self.stop)
            else:
                self.delete()
                
    def delete(self):
        '''
        This function deletes the coin
        '''
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        if self._disappear_coin_id is not None:
            self.root.after_cancel(self._disappear_coin_id)
            self._disappear_coin_id = None
        self.canvas.delete(self.image_on_canvas)
        self.image_on_canvas = None

class AnimatedButton:
    '''
    This class is used to create an animated button
    '''
    def __init__(self, root, canvas, path, width, height, command, x, y):
        self.image, self.image_large = self.create_button_image(path, width, height)
        self.button = tk.Button(root, image=self.image, command=command)
        self.button.bind("<Enter>", self.on_button_hover)
        self.button.bind("<Leave>", self.on_button_leave)
        self.id = canvas.create_window(x, y, window=self.button)
        self.canvas = canvas

    def create_button_image(self, path, width, height):
        '''
        This function is used to create the button image and the large button image
        '''
        image = Image.open(path).resize((width, height))
        image_large = Image.open(path).resize((int(width * 1.16), int(height * 1.16)))
        return ImageTk.PhotoImage(image), ImageTk.PhotoImage(image_large)

    def on_button_hover(self, event):
        '''
        This function is used to change the button image when the mouse is hovered over the button
        '''
        event.widget['image'] = self.image_large
        event.widget.lift()

    def on_button_leave(self, event):
        '''
        This function is used to change the button image when the mouse leaves the button
        '''
        event.widget['image'] = self.image

    def remove(self):
        '''
        This function is used to remove the button
        '''
        self.canvas.delete(self.id)

class CharacterSelection:
    '''
    This class is used to create the character selection screen
    '''
    def __init__(self, root, canvas, width, height):
        self.root = root
        self.canvas = canvas
        self.width = width
        self.height = height
        self.character_image = None
        self.character = None
        self.character_images_list = ['spiderMan.png','captain.png','hulk.png','IronMan.png','nomad.png','ply.png']
        self.image_path = self.character_images_list[0]
        self.image_index = 0

    def create_character_image(self):
        '''
        This function is used to create the character image
        '''
        self.get_image()
        self.character = self.canvas.create_image(self.width/2-65, self.height/2 - 50, anchor=tk.NW, image=self.character_image)

    def get_image(self):
        '''
        This function is used to get the image of the character
        '''
        self.image_path = "images/SquareCharacterFiles/" + self.image_path
        self.character_image = Image.open(self.image_path).resize((150,150))
        self.character_image = ImageTk.PhotoImage(self.character_image)

    def change_character(self,action):
        '''
        This function is used to change the character image
        '''
        if action == 'next':
            self.image_index += 1
            if self.image_index > len(self.character_images_list)-1:
                self.image_index = 0
            self.image_path = self.character_images_list[self.image_index]
        elif action == 'previous':
            self.image_index -= 1
            if self.image_index == -1:
                self.image_index = len(self.character_images_list)-1
            self.image_path = self.character_images_list[self.image_index]
        self.get_image()
        self.canvas.itemconfig(self.character,image=self.character_image)


class AnimatedCharacter:
    '''
    This class is used to create an animated character image
    '''
    def __init__(self, canvas, image_path, x, y,new_width, new_height):
        self.canvas = canvas
        self.image_path = image_path
        self.x = x
        self.y = y
        self.new_width = new_width
        self.new_height = new_height
        self.speed = 5
        image = Image.open(self.image_path)
        image = image.resize((self.new_width, self.new_height))
        self.image = ImageTk.PhotoImage(image)
        self.image_id = self.canvas.create_image(self.x, self.y, image=self.image)
        self.direction = 'up'

    def animate_up(self,start,end):
        '''
        This function is used to create an jumping animation
        '''
        image_coords = self.canvas.coords(self.image_id)
        if len(image_coords)== 0:
            return
        if image_coords[1] <= start:
            self.direction = 'down'
        elif image_coords[1]+self.new_height >= end:
            self.direction = 'up'
        if self.direction == 'up':
            self.canvas.move(self.image_id, 0, -self.speed)
        elif self.direction == 'down':
            self.canvas.move(self.image_id, 0, self.speed)

        self.canvas.after(10, lambda:self.animate_up(start,end)) 

    def animate_left(self,start,end):
        '''
        This function is used to create a running animation towards the left
        '''
        image_coords = self.canvas.coords(self.image_id)
        if len(image_coords)== 0:
            return
        if image_coords[0] <= end:
            self.canvas.coords(self.image_id, start, image_coords[1])
        else:
            self.canvas.move(self.image_id, -self.speed, 0)

        self.canvas.after(10, lambda:self.animate_left(start,end))

    def animate_right(self,start,end):
        '''
        This function is used to create a running animation towards the right 
        '''
        image_coords = self.canvas.coords(self.image_id)
        if len(image_coords)== 0:
            return
        if image_coords[0] >= end:
            self.canvas.coords(self.image_id, start, image_coords[1])
        else:
            self.canvas.move(self.image_id, self.speed, 0)

        self.canvas.after(10, lambda:self.animate_right(start,end))
