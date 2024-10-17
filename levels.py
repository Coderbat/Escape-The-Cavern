'''
This file contains the functions that create the levels
'''
from PIL import Image, ImageTk
import animation
PLATFORM_COLOUR = '#cccccc'
WATER_COLOUR = '#6daef6'
LAVA_COLOUR = '#C2490D'
coin_size = (140,60)

def create_background(canvas,width,height):
    '''
    This function creates the background for the levels
    '''
    background_image = Image.open(r"images/gray-painted-background.jpg")
    background_image = background_image.resize((width, height))
    background = ImageTk.PhotoImage(background_image)
    canvas.create_image(0, 0, image=background, anchor='nw')
    canvas.background = background

def get_coin_coords(coin,canvas):
    '''
    This function returns the coordinates of the coin
    '''
    coin_coords = canvas.coords(coin.image_on_canvas)
    coin_coords = [coin_coords[0]-10,coin_coords[1],coin_coords[0]+10,coin_coords[1]+20]
    return coin_coords

def level_selecter(level,canvas,width,height,root):
    '''
    This function selects the level and returns the game conditions
    '''
    game_conditions = None
    if level == 1:
        game_conditions = level_1(canvas,width,height,root)
    elif level == 2:
        game_conditions = level_2(canvas,width,height,root)
    elif level == 3:
        game_conditions = level_3(canvas,width,height,root)
    elif level == 4:
        game_conditions = level_4(canvas,width,height,root)
    elif level == 5:
        game_conditions = level_5(canvas,width,height,root)
    elif level == 6:
        game_conditions = level_6(canvas,width,height,root)
    elif level == 7:
        game_conditions = 'win'
    return game_conditions

def level_1(canvas_lvl1,width,height,root):
    '''
    This function creates the objects for the first level
    '''

    game_condition = {}
    create_background(canvas_lvl1,width,height)
    canvas_lvl1.create_rectangle(0,height*3/4,width,height,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    spike_image = Image.open(r"images/long_metal_spike.png")
    arrow_image = Image.open(r"images/Arrow_Lvl1.png")
    arrow = ImageTk.PhotoImage(arrow_image)
    image_width, image_height = spike_image.size
    spike_image = spike_image.resize((int(image_width//2), int(image_height//4)))
    spike = ImageTk.PhotoImage(spike_image)
    spike_var1 = canvas_lvl1.create_image(width/2, height*3/4, image=spike, anchor='sw')
    canvas_lvl1.create_image(width/2 + image_width//2, height*3/4, image=spike, anchor='sw')
    canvas_lvl1.image = spike
    anchor_coords1 = canvas_lvl1.coords(spike_var1)
    canvas_lvl1.create_text(width/2, height/2-40, text="Touching the spike will end the game", font=("Comic Sans MS", 20), fill="black")
    canvas_lvl1.create_image(width/2+50, height/2 + 60, image=arrow)
    canvas_lvl1.arrow = arrow
    platform = canvas_lvl1.create_rectangle(width/2 + 100,height*3/4 - 100,width/2 +200,height*3/4 - 50,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords = canvas_lvl1.coords(platform)
    pos_spike1 = [anchor_coords1[0]+10, platform_coords[3] +10, platform_coords[2] - 50, anchor_coords1[1]]
    platform_coords = canvas_lvl1.coords(platform)
    coin1 = animation.AnimateCoin(root,width/2,height/2,100,canvas_lvl1,coin_size)
    coin1_coords = get_coin_coords(coin1,canvas_lvl1)
    coin2 = animation.AnimateCoin(root,width/3,height/2,100,canvas_lvl1,coin_size)
    coin2_coords = get_coin_coords(coin2,canvas_lvl1)
    game_condition['lose'] = [pos_spike1]
    game_condition['platform'] = {platform: platform_coords}
    game_condition['coin'] = [[coin1,coin1_coords],[coin2,coin2_coords]]
    return game_condition


def level_2(canvas_lvl2,width,height,root):
    '''
    This function creates the objects for the second level
    '''

    game_condition = {}
    create_background(canvas_lvl2,width,height)
    arrow_image = Image.open(r"images/Arrow_Lvl1.png")
    arrow = ImageTk.PhotoImage(arrow_image)
    arrow_image2 = Image.open(r"images/Arrow_Lvl2.png")
    arrow2 = ImageTk.PhotoImage(arrow_image2)
    canvas_lvl2.create_rectangle(0,height*3/4,width,height,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    water = canvas_lvl2.create_rectangle(width/4,height*3/4-1,width/2,height*3/4 +60,fill=WATER_COLOUR,outline = WATER_COLOUR)
    water_coords = canvas_lvl2.coords(water)
    water_start = canvas_lvl2.create_rectangle(width/4-1,height*3/4+2,width/4,height*3/4 +60,fill=WATER_COLOUR,outline = WATER_COLOUR)
    water_start_coords = canvas_lvl2.coords(water_start)
    water_end = canvas_lvl2.create_rectangle(width/2,height*3/4+2,width/2+1,height*3/4 +60,fill=WATER_COLOUR,outline = WATER_COLOUR)
    water_end_coords = canvas_lvl2.coords(water_end)
    canvas_lvl2.create_line(318,height*3/4,318,height*3/4+60,fill="black",width=2)
    canvas_lvl2.create_line(318,height*3/4+60,642,height*3/4+60,fill="black",width=2)
    canvas_lvl2.create_line(642,height*3/4+60,642,height*3/4,fill="black",width=2)
    canvas_lvl2.create_image(width/4+100, height*3/4-200, image=arrow2)
    canvas_lvl2.arrow2 = arrow2
    canvas_lvl2.create_text(width/4+120,height*3/4-250,text="Water slows you down",font=("Comic Sans MS", 20),fill="black")
    lava = canvas_lvl2.create_rectangle(width/2 + 100,height*3/4-1,width/2 + 500,height*3/4 +60,fill=LAVA_COLOUR,outline = LAVA_COLOUR)
    lava_coords = canvas_lvl2.coords(lava)
    canvas_lvl2.create_line(lava_coords[0],lava_coords[1],lava_coords[0],lava_coords[3],fill="black",width=2)
    canvas_lvl2.create_line(lava_coords[0],lava_coords[3],lava_coords[2],lava_coords[3],fill="black",width=2)
    canvas_lvl2.create_line(lava_coords[2],lava_coords[3],lava_coords[2],lava_coords[1],fill="black",width=2)
    canvas_lvl2.create_text(width/2+200,height*3/4-200,text="Falling into the lava ends the game",font=("Comic Sans MS", 20),fill="black")
    canvas_lvl2.create_image(width/2+300, height*3/4-100, image=arrow)
    canvas_lvl2.arrow = arrow
    platform1 = canvas_lvl2.create_rectangle(width/2 + 200,height*3/4 - 100,width/2 +300,height*3/4 - 50,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords1 = canvas_lvl2.coords(platform1)
    coin1 = animation.AnimateCoin(root,400,570,100,canvas_lvl2,(140,60))
    coin1_coords = get_coin_coords(coin1,canvas_lvl2)
    coin2 = animation.AnimateCoin(root,531,570,100,canvas_lvl2,(140,60))
    coin2_coords = get_coin_coords(coin2,canvas_lvl2)
    coin3 = animation.AnimateCoin(root,890,411,100,canvas_lvl2,(140,60))
    coin3_coords = get_coin_coords(coin3,canvas_lvl2)
    game_condition['platform'] = {platform1:platform_coords1}
    game_condition['lose'] = [lava_coords]
    game_condition['water'] = [water_coords]
    game_condition['water_start'] = {tuple(water_coords):water_start_coords}
    game_condition['water_end'] = {tuple(water_coords):water_end_coords}
    game_condition['coin'] = [[coin1,coin1_coords],[coin2,coin2_coords],[coin3,coin3_coords]]
    return game_condition

def level_3(canvas_lvl3,width,height,root):
    '''
    This function creates the objects for the third level
    '''
    game_condition = {}
    create_background(canvas_lvl3,width,height)
    canvas_lvl3.create_rectangle(0,height*3/4,width,height,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform1 = canvas_lvl3.create_rectangle(206,405,280,435,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords1 = canvas_lvl3.coords(platform1)
    platform2 = canvas_lvl3.create_rectangle(400,347,470,367,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords2 = canvas_lvl3.coords(platform2)
    lava = canvas_lvl3.create_rectangle(280,height*3/4-1,width/2 + 500,height*3/4 +60,fill=LAVA_COLOUR,outline = LAVA_COLOUR)
    lava_coords = canvas_lvl3.coords(lava)
    canvas_lvl3.create_line(lava_coords[0],lava_coords[1],lava_coords[0],lava_coords[3],fill="black",width=2)
    canvas_lvl3.create_line(lava_coords[0],lava_coords[3],lava_coords[2],lava_coords[3],fill="black",width=2)
    canvas_lvl3.create_line(lava_coords[2],lava_coords[3],lava_coords[2],lava_coords[1],fill="black",width=2)
    coin1 = animation.AnimateCoin(root,width/2,198,100,canvas_lvl3,(140,60))
    coin1_coords = get_coin_coords(coin1,canvas_lvl3)
    coin2 = animation.AnimateCoin(root,1003,198,100,canvas_lvl3,(140,60))
    coin2_coords = get_coin_coords(coin2,canvas_lvl3)
    coin3 = animation.AnimateCoin(root,420,198,100,canvas_lvl3,(140,60))
    coin3_coords = get_coin_coords(coin3,canvas_lvl3)
    coin4 = animation.AnimateCoin(root,817,198,100,canvas_lvl3,(140,60))
    coin4_coords = get_coin_coords(coin4,canvas_lvl3)   
    game_condition['coin'] = [[coin1,coin1_coords],[coin2,coin2_coords],[coin3,coin3_coords],[coin4,coin4_coords]]
    game_condition['lose'] = [lava_coords]
    game_condition['platform'] = {platform1:platform_coords1,platform2:platform_coords2}
    game_condition['moving'] = {platform2:[280,width]}
    return game_condition
def level_4(canvas_lvl4,width,height,root):
    '''
    This function creates the objects for the fourth level
    '''
    game_condition = {}
    create_background(canvas_lvl4,width,height)
    canvas_lvl4.create_rectangle(0,height*3/4,width,height,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform1 = canvas_lvl4.create_rectangle(200,430,270,450,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords1 = canvas_lvl4.coords(platform1)
    platform2 = canvas_lvl4.create_rectangle(330,330,400,350,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords2 = canvas_lvl4.coords(platform2)
    platform3 = canvas_lvl4.create_rectangle(460,200,530,220,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords3 = canvas_lvl4.coords(platform3)
    platform4 = canvas_lvl4.create_rectangle(570,100,700,120,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords4 = canvas_lvl4.coords(platform4)
    platform5 = canvas_lvl4.create_rectangle(width - 250,430,width,450,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords5 = canvas_lvl4.coords(platform5)
    lava = canvas_lvl4.create_rectangle(width/2-100,height*3/4-1,width,height*3/4 +60,fill=LAVA_COLOUR,outline = LAVA_COLOUR)
    lava_coords = canvas_lvl4.coords(lava)
    canvas_lvl4.create_line(lava_coords[0],lava_coords[1],lava_coords[0],lava_coords[3],fill="black",width=2)
    canvas_lvl4.create_line(lava_coords[0],lava_coords[3],lava_coords[2],lava_coords[3],fill="black",width=2)
    canvas_lvl4.create_line(1276,lava_coords[3],1276,lava_coords[1],fill="black",width=2)
    coin1 = animation.AnimateCoin(root,956,257,100,canvas_lvl4,(140,60))
    coin1_coords = get_coin_coords(coin1,canvas_lvl4)
    coin2 = animation.AnimateCoin(root,886,158,100,canvas_lvl4,(140,60))
    coin2_coords = get_coin_coords(coin2,canvas_lvl4)
    coin3 = animation.AnimateCoin(root,1024,356,100,canvas_lvl4,(140,60))
    coin3_coords = get_coin_coords(coin3,canvas_lvl4)
    coin4 = animation.AnimateCoin(root,819,63,100,canvas_lvl4,(140,60))
    coin4_coords = get_coin_coords(coin4,canvas_lvl4)
    game_condition['coin'] = [[coin1,coin1_coords],[coin2,coin2_coords],[coin3,coin3_coords],[coin4,coin4_coords]]
    game_condition['platform'] = {platform1:platform_coords1,platform2:platform_coords2,platform3:platform_coords3,platform4:platform_coords4,platform5:platform_coords5}
    game_condition['lose'] = [lava_coords]
    return game_condition

def level_5(canvas_lvl5,width,height,root):
    '''
    This function creates the objects for the fifth level
    '''
    game_condition = {}
    water1 = canvas_lvl5.create_rectangle(0,0,width,height,fill=WATER_COLOUR,outline = WATER_COLOUR)
    water_coords1 = canvas_lvl5.coords(water1)
    water_start1 = canvas_lvl5.create_rectangle(0,0,1,1,fill=WATER_COLOUR,outline = WATER_COLOUR)
    water_start_coords1 = canvas_lvl5.coords(water_start1)
    water_end1 = canvas_lvl5.create_rectangle(0,0,1,1,fill=WATER_COLOUR,outline = WATER_COLOUR)
    water_end_coords1 = canvas_lvl5.coords(water_end1)
    underwater_image = Image.open(r"images/underwater.png")
    underwater = ImageTk.PhotoImage(underwater_image)
    canvas_lvl5.underwater = underwater
    canvas_lvl5.create_image(0,0, image=underwater,anchor = 'nw')
    platform1 = canvas_lvl5.create_rectangle(0,height*3/4,198,height*3/4+20,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords1 = canvas_lvl5.coords(platform1)
    platform2 = canvas_lvl5.create_rectangle(261,498,342,520,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords2 = canvas_lvl5.coords(platform2)
    platform3 = canvas_lvl5.create_rectangle(411,431,480,450,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords3 = canvas_lvl5.coords(platform3)
    platform4 = canvas_lvl5.create_rectangle(561,404,700,424,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords4 = canvas_lvl5.coords(platform4)
    platform5 = canvas_lvl5.create_rectangle(739,323,820,343,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords5 = canvas_lvl5.coords(platform5)
    platform6 = canvas_lvl5.create_rectangle(957,498,1100,520,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords6 = canvas_lvl5.coords(platform6)
    platform7 = canvas_lvl5.create_rectangle(1179,498,width,520,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform7_coords = canvas_lvl5.coords(platform7)
    spike_image = Image.open(r"images/long_metal_spike.png")
    image_width, image_height = spike_image.size
    spike_image = spike_image.resize((int(image_width//2), int(image_height//4)))
    spike = ImageTk.PhotoImage(spike_image)
    canvas_lvl5.spike = spike
    start = 0
    while True:
        canvas_lvl5.create_image(start + image_width//2, height, image=spike, anchor='se')
        start += image_width//2
        if start > width:
            break
    coin1 = animation.AnimateCoin(root,width/2,height/2,100,canvas_lvl5,(140,60))
    coin1_coords = get_coin_coords(coin1,canvas_lvl5)
    coin2 = animation.AnimateCoin(root,782,282,100,canvas_lvl5,(140,60))
    coin2_coords = get_coin_coords(coin2,canvas_lvl5)
    coin3 = animation.AnimateCoin(root,958,404,100,canvas_lvl5,(140,60))
    coin3_coords = get_coin_coords(coin3,canvas_lvl5)
    coin4 = animation.AnimateCoin(root,914,333,100,canvas_lvl5,(140,60))
    coin4_coords = get_coin_coords(coin4,canvas_lvl5)
    game_condition['platform'] = {platform1:platform_coords1,platform2:platform_coords2,platform3:platform_coords3,platform4:platform_coords4,platform5:platform_coords5,platform6:platform_coords6,platform7:platform7_coords}
    game_condition['coin'] = [[coin1,coin1_coords],[coin2,coin2_coords],[coin3,coin3_coords],[coin4,coin4_coords]]
    game_condition['water'] = [water_coords1]
    game_condition['water_start'] = {tuple(water_coords1):water_start_coords1}
    game_condition['water_end'] = {tuple(water_coords1):water_end_coords1}
    game_condition['lose'] = [[0,height-40,width,height]]
    return game_condition

def level_6(canvas_lvl6,width,height,root):
    '''
    This function creates the objects for the sixth level
    '''
    game_condition = {}
    water1 = canvas_lvl6.create_rectangle(0,0,width,height,fill=WATER_COLOUR,outline = WATER_COLOUR)
    water_coords1 = canvas_lvl6.coords(water1)
    water_start1 = canvas_lvl6.create_rectangle(0,0,1,1,fill=WATER_COLOUR,outline = WATER_COLOUR)
    water_start_coords1 = canvas_lvl6.coords(water_start1)
    water_end1 = canvas_lvl6.create_rectangle(0,0,1,1,fill=WATER_COLOUR,outline = WATER_COLOUR)
    water_end_coords1 = canvas_lvl6.coords(water_end1)
    underwater_image = Image.open(r"images/underwater.png")
    underwater = ImageTk.PhotoImage(underwater_image)
    canvas_lvl6.underwater = underwater
    canvas_lvl6.create_image(0,0, image=underwater,anchor = 'nw')
    platform1 = canvas_lvl6.create_rectangle(0,height*3/4,198,height*3/4+20,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords1 = canvas_lvl6.coords(platform1)
    platform2 = canvas_lvl6.create_rectangle(261,588,342,610,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords2 = canvas_lvl6.coords(platform2)
    platform3 = canvas_lvl6.create_rectangle(411,521,480,540,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords3 = canvas_lvl6.coords(platform3)
    platform4 = canvas_lvl6.create_rectangle(761,521,830,540,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords4 = canvas_lvl6.coords(platform4)
    platform5 = canvas_lvl6.create_rectangle(width - 100,521,width,540,fill=PLATFORM_COLOUR,outline = "black",width = 2)
    platform_coords5 = canvas_lvl6.coords(platform5)
    spike_image = Image.open(r"images/long_metal_spike.png")
    image_width, image_height = spike_image.size
    spike_image = spike_image.resize((int(image_width//2), int(image_height//4)))
    spike = ImageTk.PhotoImage(spike_image)
    canvas_lvl6.spike = spike
    start = 0
    while True:
        canvas_lvl6.create_image(start + image_width//2, height, image=spike, anchor='se')
        start += image_width//2
        if start > width:
            break
    coin1 = animation.AnimateCoin(root,614,507,100,canvas_lvl6,(140,60))
    coin1_coords = get_coin_coords(coin1,canvas_lvl6)
    coin2 = animation.AnimateCoin(root,449,463,100,canvas_lvl6,(140,60))
    coin2_coords = get_coin_coords(coin2,canvas_lvl6)
    coin3 = animation.AnimateCoin(root,797,465,100,canvas_lvl6,(140,60))
    coin3_coords = get_coin_coords(coin3,canvas_lvl6)
    coin4 = animation.AnimateCoin(root,1018,507,100,canvas_lvl6,(140,60))
    coin4_coords = get_coin_coords(coin4,canvas_lvl6)
    coin5 = animation.AnimateCoin(root,1219,470,100,canvas_lvl6,(140,60))
    coin5_coords = get_coin_coords(coin5,canvas_lvl6)
    game_condition['water'] = [water_coords1]
    game_condition['water_start'] = {tuple(water_coords1):water_start_coords1}
    game_condition['water_end'] = {tuple(water_coords1):water_end_coords1}
    game_condition['platform'] = {platform1:platform_coords1,platform2:platform_coords2,platform3:platform_coords3,platform4:platform_coords4,platform5:platform_coords5}
    game_condition['moving'] = {platform2:[0,width]}
    game_condition['coin'] = [[coin1,coin1_coords],[coin2,coin2_coords],[coin3,coin3_coords],[coin4,coin4_coords],[coin5,coin5_coords]]
    game_condition['lose'] = [[0,height-40,width,height]]
    return game_condition
    