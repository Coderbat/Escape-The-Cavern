'''
This is the main file of the game
'''
#1280x720
#Imports
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from PIL import Image, ImageTk
import levels
import data_handeling
import game_logic
import animation

class Menu:
    '''
    This class contains all the functions and variables related to the menus of the game
    '''
    def __init__(self):
        self.continue_button = None
        self.new_game_button = None
        self.controls_button = None
        self.quit_button = None
        self.username = None
        self.password = None
        self.rect_id = None
        self.button_resume_id = None
        self.button_retry_id = None
        self.button_menu_id = None
        self.button_quit_id = None
        self.pause_menu_active = False
        self.right = None
        self.left = None
        self.up = None
        self.load_position = False
        self.coin_history = None
        self.position = None
        # self.down = None
        self.on_controls_menu = False
        self.controls_set = False
        self.return_button = None
        self.char_select = None
        self.platforms = []
        self.trophy = None
        self.trophy_id = None
        self.trophy_image = None

    def start_menu(self):
        '''
        This function creates the start menu of the game
        '''
        self.username = None
        self.platforms = []
        Main.god_mode = False
        Main.level = 0
        Main.score = 0
        self.coin_history = None
        canvas.create_text(WIDTH / 2, 50, text="Game Title", font=("Arial", 24))
        background_image = Image.open(r"images/gray-painted-background.jpg")
        background_image = background_image.resize((WIDTH, HEIGHT))
        background = ImageTk.PhotoImage(background_image)
        canvas.create_image(0, 0, image=background, anchor='nw')
        canvas.background = background
        logo_image = Image.open(r"images/menu/homepagelogo.png")
        logo = ImageTk.PhotoImage(logo_image)
        canvas.create_image(200, 40, image=logo, anchor='nw')
        canvas.logo = logo

        #creating the buttons
        self.continue_button = animation.AnimatedButton\
            (root, canvas, "images/menu/ContinueButton.png", \
             300, 100, self.on_button_continue_clicked, 160, HEIGHT / 2 - 50)
        self.new_game_button = animation.AnimatedButton\
            (root, canvas, "images/menu/NewGameButton.png", \
             300, 100, self.on_button_newgame_clicked, 160, HEIGHT/2+50)
        self.quit_button = animation.AnimatedButton\
            (root, canvas, "images/menu/QuitButton.png", \
             300, 100, self.on_button_quit_clicked, 160, HEIGHT / 2 + 150)

        #creating the character selection screen
        self.char_select = animation.CharacterSelection(root, canvas, WIDTH, HEIGHT)
        self.char_select.create_character_image()
        animation.AnimatedButton\
            (root, canvas, "images/menu/NextSquareButton.png",\
              50, 50, lambda: self.char_select.change_character('next'), WIDTH/2+150, HEIGHT / 2+20)
        animation.AnimatedButton\
            (root, canvas, "images/menu/BackSquareButton.png", \
             50, 50, lambda: self.char_select.change_character('previous'), WIDTH/2-130, HEIGHT / 2+20)
        self.show_leaderboard()

    def show_leaderboard(self):
        '''
        This function shows the leaderboard in the start menu
        '''
        leaderboard_data = data_handeling.load("leaderboard.dat")
        canvas.create_rectangle(945,158,1235,575,fill="black",outline="#d0d0d0",width=5)
        leaderboard_image = Image.open(r"images/Leaderboard.png")
        leaderboard_image = leaderboard_image.resize((256, 28))
        leaderboard_text = ImageTk.PhotoImage(leaderboard_image)
        canvas.create_image(967, 175, image=leaderboard_text, anchor='nw')
        canvas.leaderboard = leaderboard_text
        canvas.create_text\
            (WIDTH - 250, 230, text="Username", font=("Helvetica", 16, "bold"),fill='white')
        canvas.create_text\
            (WIDTH - 100, 230, text="Score", font=("Helvetica", 16, "bold"),fill='white')
        if leaderboard_data is None:
            return
        leaderboard_data.sort(key=lambda x: x["score"], reverse=True)

        #writing the leaderboard data to the canvas
        for i, player_data in enumerate(leaderboard_data, 1):
            if self.username == player_data['username']:
                canvas.create_text\
                    (WIDTH - 300, 250 + i * 30, text=f"{i}. {player_data['username']}", anchor="w", font=("Helvetica", 16),fill='red')
                canvas.create_text\
                    (WIDTH - 100, 250 + i * 30, text=f"{player_data['score']}", anchor="w", font=("Helvetica", 16),fill='red')
            else:
                canvas.create_text\
                    (WIDTH - 100, 250 + i * 30, text=f"{player_data['score']}", anchor="w", font=("Helvetica", 16),fill='white')
                canvas.create_text\
                    (WIDTH - 300, 250 + i * 30, text=f"{i}. {player_data['username']}", anchor="w", font=("Helvetica", 16),fill='white')
            if i == 10:
                break

    def pause_menu(self):
        '''
        This function creates the pause menu in the game
        '''
        self.rect_id = canvas.create_rectangle\
            (WIDTH/2-200, HEIGHT/2-300, WIDTH/2+200, HEIGHT/2+300, fill="#cccccc", outline='black',width=10)
        self.button_resume_id = animation.AnimatedButton\
            (root, canvas, "images/menu/ResumeButton.png", 300, 100, self.resume, WIDTH/2, HEIGHT / 2 - 200)
        self.button_retry_id = animation.AnimatedButton\
            (root, canvas, "images/menu/RetryButton.png", 300, 100, self.retry_clicked,WIDTH/2, HEIGHT / 2 - 100)
        self.controls_button = animation.AnimatedButton\
            (root, canvas, "images/menu/ControlsButton.png", 300, 100, self.on_button_controls_clicked, WIDTH/2, HEIGHT / 2 )
        self.button_menu_id = animation.AnimatedButton\
            (root, canvas, "images/menu/MenuButton.png", 300, 100, self.main_menu_clicked, WIDTH/2, HEIGHT / 2 + 100)
        self.button_quit_id = animation.AnimatedButton\
            (root, canvas, "images/menu/QuitButton.png", 300, 100, self.on_button_quit_clicked,WIDTH/2, HEIGHT / 2 + 200)
        self.pause_menu_active = True

    def game_over_menu(self):
        '''
        This function creates the game over menu in the game
        '''
        self.rect_id = canvas.create_rectangle\
            (WIDTH/2-200, HEIGHT/2-300, WIDTH/2+200, HEIGHT/2+200, fill="#cccccc", outline='black',width=10)
        canvas.create_text\
            (WIDTH/2, HEIGHT/2 -200, text="You Died!",font=("Helvetica", 40, "bold"),fill='red')
        self.button_retry_id = animation.AnimatedButton\
            (root, canvas, "images/menu/RetryButton.png", 300, 100, self.retry_clicked,WIDTH/2, HEIGHT / 2 - 100)
        self.button_menu_id = animation.AnimatedButton\
            (root, canvas, "images/menu/MenuButton.png", 300, 100, self.main_menu_clicked, WIDTH/2, HEIGHT / 2)
        self.button_quit_id = animation.AnimatedButton\
            (root, canvas, "images/menu/QuitButton.png", 300, 100, self.on_button_quit_clicked,WIDTH/2, HEIGHT / 2 + 100)
        self.pause_menu_active = True
        keys_status['escape'] = True

    def on_button_continue_clicked(self):
        '''
        This function is executed when continue button is clicked 
        it allows the user to continue from where they left off
        '''

        data_list = data_handeling.load("saves.dat")
        user_cancel = False
        if data_list is None:
            messagebox.showinfo("No Saves Exist", "No save files exist, please start a new game")
            return
        else:
            if self.username is None:
                user_cancel = self.ask_username(True)
            for data in data_list:
                if data['username'] == self.username:
                    if data['password'] == self.password:
                    #load the data if the username and password match
                        Main.level = data['level'] -1
                        Main.score = data['score']
                        self.position = data['charPosition']

                        self.coin_history = data['coin_history']
                        self.platforms = data['platforms']
                        game_logic.Controls.right_key,game_logic.Controls.left_key,game_logic.Controls.up_key = data['controls'][0],data['controls'][1],data['controls'][2]
                        keys_status[game_logic.Controls.right_key] = False
                        keys_status[game_logic.Controls.left_key] = False
                        keys_status[game_logic.Controls.up_key] = False
                        canvas.delete("all")
                        self.load_position = True
                        if keys_status['escape'] is True:
                            keys_status['escape'] = False
                        self.pause_menu_active = False
                        Main.next_level()
                        if self.controls_set is False and Main.level != 7:
                            Main.move_character()
                        break
                    else:
                        if user_cancel is False:
                            messagebox.showinfo("Invalid input", "Password is incorrect")
                        self.username = None
                        break
            else:
                if user_cancel is False:
                    self.username = None
                    messagebox.showinfo("Invalid input", "Username does not exist")
                    self.on_button_continue_clicked()


    def on_button_newgame_clicked(self):
        '''
        This function is executed when new game button is clicked
        it starts a fresh load of the game
        '''

        self.ask_username(False)
        if self.username and self.password is not None:
            keys_status[game_logic.Controls.right_key] = False
            keys_status[game_logic.Controls.left_key] = False
            keys_status[game_logic.Controls.up_key] = False
            self.position = [0,490]
            self.coin_history = None
            self.platforms = []
            Main.next_level()
            Main.move_character()
        else:
            self.username = None

    def on_button_controls_clicked(self):
        '''
        This function is executed when controls button is clicked
        it allows the user to change the controls of the game
        '''
        self.on_controls_menu = True
        for coin in Main.game_conditions['coin']:
            animation.AnimateCoin.delete(coin[0])
        platforms = []
        for platform,platform_cords in Main.game_conditions['platform'].items():
            if 'moving' in Main.game_conditions:
                if platform in Main.game_conditions['moving']:
                    platforms.append([platform_cords,Main.movement.platform_direction])

        controls = [game_logic.Controls.right_key,game_logic.Controls.left_key,game_logic.Controls.up_key]
        data_handeling.save\
            (canvas.coords(Main.main_character), self.username,self.password,Main.level, Main.score,Main.game_conditions['coin'],controls,platforms, "saves.dat")
        canvas.delete("all")
        levels.create_background(canvas,WIDTH,HEIGHT)
        canvas.create_text(WIDTH / 2, 50, text="Click on an action then press the key you wish to bind it to", font=("Arial", 24,"bold"),fill='#d0d0d0')

        move_right_char = animation.AnimatedCharacter\
            (canvas,menu.char_select.image_path,610,210,25,25)
        move_left_char = animation.AnimatedCharacter\
            (canvas,menu.char_select.image_path,1160,375,25,25)
        move_up_char = animation.AnimatedCharacter\
            (canvas,menu.char_select.image_path,1020,500,25,25)

        move_up_char.animate_up(443,628)
        move_left_char.animate_left(1177,607)
        move_right_char.animate_right(607,1177)

        canvas.create_line(607,225,1177,225,fill='black',width=5)
        canvas.create_line(607,390,1177,390,fill='black',width=5)
        canvas.create_line(607,628,1177,628,fill='black',width=5)

        self.controls_set = True
        self.right = game_logic.Controls(root, canvas,controls[0])
        self.right.place_button(160, HEIGHT/2-150, "images/menu/NextSquareButton.png",100, 100)
        self.left = game_logic.Controls(root, canvas,controls[1])
        self.left.place_button(160, HEIGHT/2, "images/menu/BackSquareButton.png",100, 100)
        self.up = game_logic.Controls(root, canvas,controls[2])
        self.up.place_button(160, HEIGHT/2+150, "images/menu/UpSquareButton.png",100, 100)
        self.return_button = animation.AnimatedButton\
            (root, canvas, "images/menu/ReturnSquareButton.png", 50, 50, self.return_button_clicked,50, 50)

    def return_button_clicked(self):
        '''
        This function is executed when return button is clicked
        it returns the user back to the game from the controls menu
        '''
        if game_logic.Controls.check_key\
            (self.right.control_key,self.left.control_key,self.up.control_key):
            canvas.delete("all")
            self.on_controls_menu = False
            root.bind('<KeyPress>', Keyboard.key_press)
            root.bind('<KeyRelease>', Keyboard.key_release)
            game_logic.Controls.update_keys\
                (self.right.control_key,self.left.control_key,self.up.control_key)
            data_handeling.update_controls\
                (self.username,[game_logic.Controls.right_key,game_logic.Controls.left_key,game_logic.Controls.up_key])
            self.on_button_continue_clicked()
            if Main.move_character_id:
                root.after_cancel(Main.move_character_id)
            Main.move_character()

    # this function is executed when quit button is clicked
    def on_button_quit_clicked(self):
        '''
        This function is executed when quit button is clicked
        it quits the game
        '''

        if self.username:
            data_handeling.update_high_score(self.username, Main.score)
            platforms = []
            controls = [game_logic.Controls.right_key,game_logic.Controls.left_key,game_logic.Controls.up_key]
            if Main.game_conditions != 'win':
                for platform,platform_cords in Main.game_conditions['platform'].items():
                    if 'moving' in Main.game_conditions:
                        if platform in Main.game_conditions['moving']:
                            platforms.append([platform_cords,Main.movement.platform_direction])
                data_handeling.save(canvas.coords(Main.main_character), self.username,self.password,Main.level, Main.score,Main.game_conditions['coin'],controls,platforms, "saves.dat")
            else:
                data_handeling.save([], self.username,self.password,Main.level, Main.score,None,controls,platforms, "saves.dat")
        root.destroy()

    def main_menu_clicked(self):
        '''
        This function is executed when main menu button is clicked
        it takes the user back to the main menu
        '''
        if 'coin' in Main.game_conditions:
            for coin in Main.game_conditions['coin']:
                animation.AnimateCoin.delete(coin[0])
        data_handeling.update_high_score(self.username, Main.score)
        platforms = []
        controls = [game_logic.Controls.right_key,game_logic.Controls.left_key,game_logic.Controls.up_key]
        if Main.game_conditions != 'win':
            for platform,platform_cords in Main.game_conditions['platform'].items():
                if 'moving' in Main.game_conditions:
                    if platform in Main.game_conditions['moving']:
                        platforms.append([platform_cords,Main.movement.platform_direction])
            data_handeling.save(canvas.coords(Main.main_character), self.username,self.password,Main.level, Main.score,Main.game_conditions['coin'],controls,platforms, "saves.dat")
        else:
            data_handeling.save([], self.username,self.password,Main.level, Main.score,None,controls,platforms, "saves.dat")
        canvas.delete("all")
        keys_status['escape'] = False
        self.pause_menu_active = False
        self.controls_set = False
        self.start_menu()


    def retry_clicked(self):
        '''
        This function is executed when retry button is clicked
        it takes the user back to the start of the game
        '''
        if 'coin' in Main.game_conditions:
            for coin in Main.game_conditions['coin']:
                animation.AnimateCoin.delete(coin[0])
        data_handeling.update_high_score(self.username, Main.score)
        controls = [game_logic.Controls.right_key,game_logic.Controls.left_key,game_logic.Controls.up_key]
        platforms = []
        if Main.game_conditions != 'win':
            for platform,platform_cords in Main.game_conditions['platform'].items():
                if 'moving' in Main.game_conditions:
                    if platform in Main.game_conditions['moving']:
                        platforms.append([platform_cords,Main.movement.platform_direction])
            data_handeling.save(canvas.coords(Main.main_character), self.username,self.password,Main.level, Main.score,Main.game_conditions['coin'],controls,platforms, "saves.dat")
        else:
            data_handeling.save([], self.username,self.password,Main.level, Main.score,None,controls,platforms, "saves.dat")
        canvas.delete("all")

        data_list = data_handeling.load("saves.dat")
        self.load_position = True
        keys_status['escape'] = False
        self.pause_menu_active = False
        for data in data_list:
            if data['username'] == self.username:
                Main.level = 0
                Main.score = 0
                self.position = [0,490]
                self.coin_history = None
                self.platforms = []
                canvas.delete("all")
                Main.next_level()
                if Main.move_character_id is None:
                    Main.move_character()
                break


    def resume(self):
        '''
        This function resumes the game after the pause menu is closed
        '''

        keys_status['escape'] = False
        canvas.delete(self.rect_id)
        self.button_resume_id .remove()
        self.button_menu_id.remove()
        self.controls_button.remove()
        self.button_quit_id.remove()
        self.button_retry_id.remove()
        self.pause_menu_active = False






    #this function asks the user for their username using a dialog box
    def ask_username(self,duplicate_allowed):
        '''
        This function asks the user for their username using a dialog box
        '''

        while True:
            self.username = simpledialog.askstring("Input", "Username:", parent=root)
            if self.username is None:
                return True
            elif not self.username:
                messagebox.showinfo("Invalid input", "Username cannot be empty")
            elif self.username_exists(self.username) and not duplicate_allowed:
                messagebox.showinfo("Invalid input", "Username already exists")
            elif not duplicate_allowed or self.username_exists(self.username):
                while True:
                    self.password = simpledialog.askstring("Input", "Password:", parent=root, show='*')
                    if self.password is None:
                        return True
                    elif not self.password:
                        messagebox.showinfo("Invalid input", "Password cannot be empty")
                    else:
                        return False
            else:
                self.username = None
                messagebox.showinfo("Invalid input", "Username does not exist")

    def username_exists(self,username):
        '''
        This function checks if the username exists in the saves.dat file
        '''

        data_list = data_handeling.load("saves.dat")
        if data_list is None:
            return False
        for data in data_list:
            if data['username'] == username:
                return True
        return False

    def game_won(self):
        '''
        This function is executed when the user wins the game
        it shows a message box with the score and asks the user for their username
        '''
        data_handeling.update_high_score(self.username, Main.score)
        canvas.delete("all")
        canvas.create_rectangle(0+5, 0+5, WIDTH-5, HEIGHT-5, fill="grey", outline="black", width=5)
        canvas.create_text(WIDTH / 2, HEIGHT / 2-300, text=f"Congratulations {self.username}. You have Escaped!!\nYour score is {Main.score}", fill="black", font=("Arial", 30,"bold"))
        keys_status['escape'] = True

        self.button_retry_id = animation.AnimatedButton(root, canvas, "images/menu/RetryButton.png", 300, 100, self.retry_clicked,WIDTH/2, HEIGHT / 2-100)
        self.button_quit_id = animation.AnimatedButton(root, canvas, "images/menu/QuitButton.png", 300, 100, self.on_button_quit_clicked,WIDTH/2, HEIGHT / 2 + 100)
        self.button_menu_id = animation.AnimatedButton(root, canvas, "images/menu/MenuButton.png", 300, 100, self.main_menu_clicked, WIDTH/2, HEIGHT / 2)

        player_character = animation.AnimatedCharacter(canvas,menu.char_select.image_path,195,575,100,100)
        player_character.animate_up(212,600)
        self.trophy_image = Image.open(r"images/golden_trophy.png")
        self.trophy_image = self.trophy_image.resize((200,200))
        self.trophy = ImageTk.PhotoImage(self.trophy_image)
        self.trophy_id = canvas.create_image(95, 500, image=self.trophy, anchor='nw')
        self.show_leaderboard()

class App:
    '''
    This class contains all the functions and variables related to the game
    it is the main class of the game
    '''

    def __init__(self):
        self.level = 0
        self.game_conditions = {}
        self.main_character = None
        self.movement = None
        self.score = 0
        self.god_mode = False
        self.boss_key_window = None
        self.boss_key_image = None
        self.boss_key_canvas = None
        self.move_character_id = None
    def next_level(self):
        '''
            This function pulls the conditions of the next level from the levels.py file
            and applies them to the game effectively changing the level
        '''

        canvas.delete("all")
        if self.level != 0 and menu.load_position is False:
            for coin in Main.game_conditions['coin']:
                animation.AnimateCoin.delete(coin[0])
        self.level += 1
        self.game_conditions = levels.level_selecter(self.level,canvas,WIDTH,HEIGHT,root)

        if self.game_conditions == 'win':
            menu.game_won()
            return

        canvas.create_text(WIDTH/2-50, 10, anchor="nw", tags="score",
                                text=f"Score: {self.score}", fill="#d0d0d0", font=("Helvetica", 20, "bold"))

        if menu.load_position is True and menu.coin_history is not None:
            data_handeling.load_coin(self.game_conditions['coin'],menu.coin_history)
        self.main_character = self.create_character_main()
        self.movement = game_logic.Logic(self.game_conditions,HEIGHT,WIDTH)
        if self.movement.moving_id is not None:
            root.after_cancel(self.movement.moving_id)
            self.movement.moving_id = None
        if 'moving' in self.game_conditions:
            if menu.platforms != []:
                i = 0
                moving_platform = menu.platforms
                for platform in self.game_conditions['moving']:
                    canvas.coords(platform,moving_platform[i][0])
                    self.movement.platform_direction = moving_platform[i][1]
                    i += 1
            self.movement.moving_platform(self.game_conditions,canvas,keys_status)
        menu.platforms = []           


    def move_character(self):
        '''
        This is the main function of the game, it is responsible for the movement of the character
        '''

        if keys_status['escape'] is True and menu.on_controls_menu is False:
            root.after(100,self.move_character)
            canvas.tag_lower(self.main_character)
            return

        pos_character = canvas.coords(self.main_character)
        if len(pos_character) == 0:
            return
        pos_character.append(pos_character[0]+50)
        pos_character.append(pos_character[1]+50)

        main_character_speed = 0.2

        if self.movement.drowning(pos_character,self.game_conditions):
            main_character_speed = main_character_speed/2
        if self.movement.falling(pos_character,self.game_conditions) and self.movement.jump == 0:
            canvas.move(self.main_character,0,main_character_speed*2)

        elif keys_status[game_logic.Controls.up_key] and self.movement.jump == 0:
            self.movement.jump = 500
        if self.movement.jump >0:
            canvas.move(self.main_character,0,-main_character_speed*2)
            self.movement.jump -= 1
        if (keys_status[game_logic.Controls.left_key] and self.movement.halt_left is False) :
            canvas.move(self.main_character,-main_character_speed,0)
        if keys_status[game_logic.Controls.right_key] and self.movement.halt_right is False:
            canvas.move(self.main_character,main_character_speed,0)
        if 'lose' in self.game_conditions:
            lose_conditions = self.game_conditions['lose']
            for i in lose_conditions:
                if i is None:
                    continue
                if self.movement.overlapping(pos_character,i):
                    if self.god_mode is False:
                        menu.game_over_menu()
        coins = self.game_conditions['coin']
        for coin in coins:
            if coin[0].collected is False:
                if self.movement.overlapping(pos_character,coin[1]):
                    coin[0].collected = True
                    animation.AnimateCoin.stop(coin[0])
                    self.score += 1
                    canvas.delete("score")
                    canvas.create_text(WIDTH/2-50, 10, anchor="nw", tags="score",
                                   text=f"Score: {self.score}", fill="#d0d0d0", font=("Helvetica", 20, "bold"))               
        if pos_character[2]>WIDTH:
            menu.load_position = False
            self.next_level()
        canvas.tag_raise(self.main_character)
        self.move_character_id = root.after(1,self.move_character)

    def create_character_main(self):
        '''
        This function creates the main character
        '''

        menu.char_select.character_image = Image.open(menu.char_select.image_path).resize((50,50))
        menu.char_select.character_image = ImageTk.PhotoImage(menu.char_select.character_image)
        sprite = canvas.create_image(0, HEIGHT*3/4 - 50, anchor='nw', image=menu.char_select.character_image)
        if menu.load_position is True:
            if menu.position == []:
                menu.position = [0,HEIGHT*3/4 - 50]
            canvas.coords(sprite,menu.position)
        return sprite

    def apply_cheat_effect(self,cheat_effect):
        '''
        This function applies the cheat effect to the game according to the cheat code entered
        '''
        if cheat_effect == 'god_mode':
            self.god_mode = True
            messagebox.showinfo("Cheat Activated", "God Mode Activated")
        if cheat_effect == 'next_level':
            menu.load_position = False
            self.next_level()
            messagebox.showinfo("Cheat Activated", "Next Level Activated")
        if cheat_effect == 'add_score':
            self.score += 10
            canvas.delete("score")
            canvas.create_text(WIDTH/2-50, 10, anchor="nw", tags="score",
                        text=f"Score: {self.score}", fill="#d0d0d0", font=("Helvetica", 20, "bold"))               
            messagebox.showinfo("Cheat Activated", "Score Increased by 10")
    def boss_key_pressed(self):
        '''
        This function is executed when the boss key is pressed
        it pauses the game and shows a picture of some work
        '''

        if keys_status['b'] is True:
            keys_status['escape'] = True
            if Main.level != 0 and menu.pause_menu_active is False:
                if Main.level != 7:
                    menu.pause_menu()
            root.withdraw()
            self.boss_key_window = tk.Toplevel()
            self.boss_key_window.protocol("WM_DELETE_WINDOW", menu.on_button_quit_clicked)
            self.boss_key_window.geometry(f'{WIDTH}x{HEIGHT}+{int(x)}+{int(y)}')
            self.boss_key_window.resizable(False, False)
            self.boss_key_window.title("Work")
            self.boss_key_canvas = tk.Canvas(self.boss_key_window, width = WIDTH, height = HEIGHT)
            self.boss_key_canvas = tk.Canvas(self.boss_key_window, width = WIDTH, height = HEIGHT)
            image = Image.open(r"images\boss_key.png").resize((WIDTH,HEIGHT))
            self.boss_key_image = ImageTk.PhotoImage(image)
            self.boss_key_canvas.create_image(0, 0, anchor='nw', image=self.boss_key_image)
            self.boss_key_canvas.pack()
            self.boss_key_window.bind('<KeyPress>', Keyboard.key_press)
            self.boss_key_window.bind('<KeyRelease>', Keyboard.key_release)
            self.boss_key_window.mainloop()
        elif keys_status['b'] is False:
            self.boss_key_window.destroy()
            root.deiconify()
            keys_status[game_logic.Controls.left_key],keys_status[game_logic.Controls.right_key],keys_status[game_logic.Controls.up_key] = False,False,False

class Keyboard():
    '''
    This class contains all the functions and variables related to the keyboard 
    '''
    keys_status = {'escape': False,'b':False}
    cheat_codes = {'god_mode': ('g', 'o', 'd', 'm', 'o', 'd', 'e'),\
                   'next_level': ('g','o','n', 'e', 'x', 't',),\
                     'add_score': ('a', 'd', 'd', 's', 'c', 'o', 'r', 'e')       }
    key_sequence = []

    def key_press(self,event):
        '''
        This function checks if a key is being pressed
        and stores the key pressed in a dictionary
        '''
        if event.keysym.lower() == 'b':
            self.keys_status['b'] = not self.keys_status['b']
            Main.boss_key_pressed()
        elif Main.level == 0:
            return
        elif event.keysym.lower() == 'escape':
            self.keys_status['escape'] = not self.keys_status['escape']
            if Main.level != 0 and menu.pause_menu_active is False and Main.level != 7 and menu.on_controls_menu is False:
                menu.pause_menu()
            elif Main.level != 0 and menu.pause_menu_active is True:
                menu.resume()

        else:
            self.keys_status[event.keysym.lower()] = True
            self.key_sequence.append(event.keysym.lower())
            for cheat_effect,cheat_code in self.cheat_codes.items():
                if tuple(self.key_sequence[-len(cheat_code):]) == cheat_code:
                    Main.apply_cheat_effect(cheat_effect)

    def key_release(self,event):
        '''
        This function checks if a key is being released
        and changes the value of their key in the dictionary to false
        '''

        if event.keysym.lower() == 'escape':
            pass
        elif event.keysym.lower() == 'b':
            pass
        else:
            self.keys_status[event.keysym.lower()] = False

Main = App()
Keyboard = Keyboard()
menu = Menu()
keys_status = Keyboard.keys_status


HEIGHT = 720
WIDTH = 1280
root = tk.Tk()
root.iconbitmap(r'game_logo.ico')
root.title('Escape The Cavern')
root.protocol("WM_DELETE_WINDOW", menu.on_button_quit_clicked)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (WIDTH/2)
y = (screen_height/2) - (HEIGHT/2) - 40
root.geometry(f'{WIDTH}x{HEIGHT}+{int(x)}+{int(y)}')
root.resizable(False, False)
canvas = tk.Canvas(root, bg='#e5e5e5', width=WIDTH, height=HEIGHT)
root.bind('<KeyPress>', Keyboard.key_press)
root.bind('<KeyRelease>', Keyboard.key_release)
menu.start_menu()
canvas.pack()
root.mainloop()
