import pygame
import sys
import json
from cryptography.fernet import Fernet
import bcrypt         
from encryption import *

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
correct_password = "hello world"
correct = False
o = -1

# Logging out box
log_out_icon = pygame.image.load('logout_icon.png')
log_out_box = pygame.Rect(screen_width-50, 0, 50,50)
log_out_icon = pygame.transform.scale(log_out_icon, (50,50))

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

# Render the boxes with passwords. Note: dict needs to have a 'website' key
def render_password(screen, dict, top_y):
    # Render the box and lines
    w_height = text_font.get_height()
    info_box_h = (w_height+10)*len(dict.keys()) + 2*linewidth
    info_box = pygame.Rect(10,10+top_y,screen_width*3/4, info_box_h)
    pygame.draw.rect(screen, black, info_box, width=linewidth)
    pygame.draw.rect(screen, white, info_box)
    pygame.draw.line(screen, black, (10, 10+w_height+10+top_y),(9+screen_width*3/4, 10+w_height+10+top_y), width=linewidth)

    # Render the website at the top
    website = title_font.render(dict['website'], True, black)
    screen.blit(website, (15, 15+top_y)) 

    # Render all the other keys/values
    c = 5
    for k, v in dict.items():
        if k!='website':
            text = text_font.render(k+": "+v, True, black)

            screen.blit(text, (15, 20+w_height+c+top_y))
            c+=w_height+10
    
    return info_box_h 
    
# The second window with all the passwords
def window2(screen):
    global max_top
    # To allow for scrolling
    top_y = -top

    for i in o:
        box_height = render_password(screen, i, top_y)
        top_y += box_height +10
    
    max_top = top_y+top-screen_height+10

    # Display the logging out button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    selected = mouse_y<50 and mouse_x>screen_width-50
    bg_color = white if selected else light_grey
    pygame.draw.rect(screen, bg_color, log_out_box)
    pygame.draw.rect(screen, black, log_out_box, linewidth)
    screen.blit(log_out_icon, (screen_width-50, 0))

# Input for window1
def input_window1(event):
    global password_input_active, attempt_password, correct, o
    if event.type == pygame.MOUSEBUTTONDOWN:
      if input_box.collidepoint(event.pos):
          password_input_active = True
      else:
          password_input_active = False
    if event.type == pygame.KEYDOWN:
      if password_input_active:
          if event.key == pygame.K_RETURN:
              password_input_active = False
              o = decrypting(attempt_password, salt)
              if o!=-1:
                  correct = True
                  attempt_password = ""
          elif event.key == pygame.K_BACKSPACE:
              attempt_password = attempt_password[:-1]
          else:
              attempt_password += event.unicode

# Input for window2
def input_window2(event):
    global top, correct, o
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
            top-=50
            top = max(0, top)
        elif event.button == 5:
            top+=50
            top = min(max_top, top)
        elif event.button == 1:
            if log_out_box.collidepoint(event.pos):
                correct = False
                o = []

  
# Event loop
c = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not correct:
            input_window1(event)
        else:
            input_window2(event)

    # Resetting old screen
    screen.fill(dark_grey)

    # Drawing window
    if not correct:
        window1(screen)
    else:
        window2(screen)

    # Setting time between frames
    clock.tick(15)

    pygame.display.update()