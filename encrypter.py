import pygame
import sys
import json
from cryptography.fernet import Fernet
import bcrypt         
from encryption import decrypting, encrypting

# Defining constants
black = (0, 0, 0)
light_grey = (200,200,200)
dark_grey = (100,100,100)
white = (255, 255, 255)

# Initializing pygame
pygame.init()
clock = pygame.time.Clock()

# Creating the screen
top = 0
max_top = 0
screen_height = 500
screen_width = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Encrypter")

# Initializing fonts
password_font = pygame.font.SysFont('ebrima', 35)
input_font = pygame.font.SysFont('ebrima', 25)
title_font = pygame.font.SysFont('ebrima', 20, bold=True)
text_font = pygame.font.SysFont('ebrima', 20)
password = password_font.render('Password', True, black)
text_font_height = text_font.get_height()

# Password boxes coordinates and the boxes
pass_w, pass_h = password.get_size()
linewidth = 2
boxes_y = screen_height/2-pass_h/2
input_box_x = screen_width/2
password_box_x = screen_width/2-pass_w-3*linewidth
input_box = pygame.Rect(input_box_x- 2*linewidth, boxes_y-2*linewidth, screen_width/4+4*linewidth, pass_h+4*linewidth)
password_box = pygame.Rect(password_box_x - 2*linewidth, boxes_y - 2*linewidth, pass_w + 4*linewidth, pass_h + 4*linewidth)
password_input_active = False

# Password related variables and code
attempt_password = ""
window = 1
o = -1
password_add = [""]

# Trash button
trash_button_icon = pygame.image.load('trash_button.png')
trash_button_icon = pygame.transform.scale(trash_button_icon, (50,50))
trash_button_box = pygame.Rect(screen_width-50, 0, 50,50)
trash_button_box_2s = []
trash_button_icon_2 = pygame.transform.scale(trash_button_icon, (text_font_height,text_font_height))

# Check button
check_button_icon = pygame.image.load('check_button.png')
check_button_icon = pygame.transform.scale(check_button_icon, (50,50))
check_button_box = pygame.Rect(screen_width-50, screen_height-50, 50,50)

# Logging out box
log_out_icon = pygame.image.load('logout_icon.png')
log_out_box = pygame.Rect(screen_width-50, 0, 50,50)
log_out_icon = pygame.transform.scale(log_out_icon, (50,50))

# Add button
add_button_box = pygame.Rect(screen_width-50, screen_height-50, 50,50)

# The first window which is where you enter the password
def window1(screen):
    # Drawing rectangles around password text and input
    c_input_box = white if password_input_active else light_grey
    pygame.draw.rect(screen, c_input_box , input_box)
    pygame.draw.rect(screen, light_grey, password_box)
    pygame.draw.rect(screen, black, input_box, width=linewidth)
    pygame.draw.rect(screen, black, password_box, width=linewidth)

    # Writting password text and entered password
    screen.blit(password, (password_box_x, boxes_y))
    input = input_font.render(attempt_password, True, black)
    c = 0
    while input.get_width()>screen_width/4: # Fitting text in the box
        c+=1
        input = input_font.render(attempt_password[c:], True, black)
    screen.blit(input, (input_box_x, screen_height/2-input.get_height()/2)) 

# From the list of strings which represents the new password get a dict
def from_lstring_to_dict(password_add_ls):
    d = {"website":password_add_ls[0]}
    if len(password_add_ls)>1:
        for kv in password_add_ls[1:]:
            kvs = kv.split(":")
            v = "" if len(kvs)==1 else ":".join(kvs[1:])
            d[kvs[0]] = v
    return d

# Render the boxes with passwords. Note: dict needs to have a 'website' key
def render_password(screen, dict, top_y, window=3):
    global o
    # Render the box and lines
    info_box_h = (text_font_height+10)*len(dict.keys()) + 2*linewidth
    info_box = pygame.Rect(10,10+top_y,screen_width*3/4, info_box_h)
    pygame.draw.rect(screen, black, info_box, width=linewidth)
    pygame.draw.rect(screen, white, info_box)
    pygame.draw.line(screen, black, (10, 10+text_font_height+10+top_y),(9+screen_width*3/4, 10+text_font_height+10+top_y), width=linewidth)

    # Render the trash button
    if window==2:
        trash_button_box_2 = pygame.Rect(10+screen_width*3/4-text_font_height, top_y+10, text_font_height, text_font_height+12)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        selected = trash_button_box_2.collidepoint((mouse_x, mouse_y))
        bg_color = white if selected else light_grey
        pygame.draw.rect(screen, bg_color, trash_button_box_2)
        pygame.draw.rect(screen, black, trash_button_box_2, linewidth)
        screen.blit(trash_button_icon_2, (10+screen_width*3/4-text_font_height, 15+top_y))
        if pygame.mouse.get_pressed()[0] and selected:
            o.remove(dict)

    # Render the website at the top
    website = title_font.render(dict['website'], True, black)
    screen.blit(website, (15, 15+top_y)) 

    # Render all the other keys/values
    c = 5
    for k, v in dict.items():
        if k!='website':
            text = text_font.render(k+": "+v, True, black)

            screen.blit(text, (15, 20+text_font_height+c+top_y))
            c+=text_font_height+10
    
    return info_box_h 
    
# The second window with all the passwords
def window2(screen):
    global max_top
    # To allow for scrolling
    top_y = -top

    for i in o:
        box_height = render_password(screen, i, top_y, window=2)
        top_y += box_height +10
    
    max_top = top_y+top-screen_height+10

    # Display the logging out button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    selected = mouse_y<50 and mouse_x>screen_width-50
    bg_color = white if selected else light_grey
    pygame.draw.rect(screen, bg_color, log_out_box)
    pygame.draw.rect(screen, black, log_out_box, linewidth)
    screen.blit(log_out_icon, (screen_width-50, 0))

    # display the add button
    selected = mouse_y>screen_height-50 and mouse_x>screen_width-50
    bg_color = white if selected else light_grey
    pygame.draw.rect(screen, bg_color, add_button_box)
    pygame.draw.rect(screen, black, add_button_box, linewidth)
    pygame.draw.line(screen, black, (screen_width-45, screen_height-25), (screen_width-5, screen_height-25), width=2)
    pygame.draw.line(screen, black, (screen_width-25, screen_height-45), (screen_width-25, screen_height-5), width=2)

# Window 3, when the user is adding a set of passwords, usernames, etc...
def window3(screen):
    # Display the trash button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    selected = mouse_y<50 and mouse_x>screen_width-50
    bg_color = white if selected else light_grey
    pygame.draw.rect(screen, bg_color, trash_button_box)
    pygame.draw.rect(screen, black, trash_button_box, linewidth)
    screen.blit(trash_button_icon, (screen_width-50, 0))

    # Display the check button
    selected = mouse_y>screen_height-50 and mouse_x>screen_width-50
    bg_color = white if selected else light_grey
    pygame.draw.rect(screen, bg_color, check_button_box)
    pygame.draw.rect(screen, black, check_button_box, linewidth)
    screen.blit(check_button_icon, (screen_width-50, screen_height-50))

    # Render the box and lines
    info_box_h = text_font_height+10 + 2*linewidth
    info_box = pygame.Rect(10,10,screen_width*3/4, info_box_h)
    pygame.draw.rect(screen, black, info_box, width=linewidth)
    pygame.draw.rect(screen, white, info_box)
    pygame.draw.line(screen, black, (10, 10+text_font_height+10),(9+screen_width*3/4, 10+text_font_height+10), width=linewidth)

    # Render the new password
    d = from_lstring_to_dict(password_add)
    render_password(screen, d, 0)

# Input for window1
def input_window1(event):
    global password_input_active, attempt_password, window, o
    if event.type == pygame.MOUSEBUTTONDOWN:
      if input_box.collidepoint(event.pos):
          password_input_active = True
      else:
          password_input_active = False
    if event.type == pygame.KEYDOWN:
      if password_input_active:
          if event.key == pygame.K_RETURN:
              password_input_active = False
              o = decrypting(attempt_password)
              if o!=-1:
                  window = 2
          elif event.key == pygame.K_BACKSPACE:
              attempt_password = attempt_password[:-1]
          else:
              attempt_password += event.unicode

# Input for window2
def input_window2(event):
    global top, window, o, attempt_password
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
            top-=50
            top = max(0, top)
        elif event.button == 5:
            top+=50
            top = min(max_top, top)
        elif event.button == 1:
            if log_out_box.collidepoint(event.pos):
                window = 1
                attempt_password = ""
                o = -1
            if add_button_box.collidepoint(event.pos):
                window=3

# Input for window3
def input_window3(event):
    global window, password_add, top
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            password_add.append("")
        elif event.key == pygame.K_BACKSPACE:
            if password_add[-1]!="":
                password_add[-1] = password_add[-1][:-1]
            else:
                if len(password_add)>1:
                    del password_add[-1]
        else:
            password_add[-1] +=event.unicode
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if trash_button_box.collidepoint(event.pos):
                password_add = [""]
                if o!=-1:
                    window = 2
                else:
                    window = 1
            elif check_button_box.collidepoint(event.pos):
                if o!=-1:
                    d_add = from_lstring_to_dict(password_add)
                    o.append(d_add)
                    window = 2
                    password_add = [""]
                    top = max_top
                else:
                    window = 1

# Event loop
c = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if o!=-1:
                encrypting(attempt_password, d=o)
            pygame.quit()
            sys.exit()
        if window==1:
            input_window1(event)
        elif window==2:
            input_window2(event)
        else:
            input_window3(event)

    # Resetting old screen
    screen.fill(dark_grey)

    # Drawing window
    if window==1:
        window1(screen)
    elif window==2:
        window2(screen)
    else:
        window3(screen)

    # Setting time between frames
    clock.tick(15)

    pygame.display.update()