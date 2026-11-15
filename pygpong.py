from pygame import *
import sys

def quitall():
    quit()
    sys.exit()

def colliderect(r1, r2):
        return r1.rect.colliderect(r2)

def initialize(screensize, screencolor):
    init()
    global backcolor
    global mw
    global clock
    backcolor = screencolor  
    mw = display.set_mode(screensize)  
    mw.fill(backcolor)
    clock = time.Clock()

def key_pressed(key_id):
    keys = key.get_pressed()
    return keys[key_id]

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, px, py, size_x, size_y, p_speed):
        sprite.Sprite.__init__(self)
        # Safe asset loader: creates a colored block if the image file is missing
        try:
            self.image = transform.scale(image.load(player_image), (size_x, size_y))
        except:
            self.image = Surface((size_x, size_y))
            self.image.fill((255, 255, 255)) # Default white box if image fails
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py
        
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))
    
    def changexy(self, x, y):
        self.rect.x += x
        self.rect.y += y

# 1. Setup the window
initialize((700, 500), (115, 125, 240))

# 2. Create game objects
p1 = GameSprite("glasspaddle2.png", 20, 200, 30, 120, 5) 
p2 = GameSprite("glasspaddle2.png", 650, 200, 30, 120, 5)
ball = GameSprite("ball.png", 335, 235, 30, 30, 5)

# 3. Safe Music Load
try:
    mixer.music.load("bg_pong.mp3")
    mixer.music.play(loops=-1, start=0.0, fade_ms=0)
    mixer.music.set_volume(0.75)
except:
    pass 

b_speedx = 3
b_speedy = 3
# 4. Game Loop
running = True
while running:
    # Handle window close event
    for event_item in event.get():
        if event_item.type == QUIT:
            running = False
    
    if sprite.collide_rect(ball,p1) or sprite.collide_rect(ball,p2):
        b_speedx *= -1    
    
    if ball.rect.top <= 0:
        ball.rect.top = 20
        b_speedy *= -1
    elif ball.rect.bottom >= 500:
        ball.rect.bottom = 480
        b_speedy *= -1  

    # Keyboard movement inputs
    if key_pressed(K_w):
        p1.changexy(0, -p1.speed)
    if key_pressed(K_s):
        p1.changexy(0, p1.speed)
    if key_pressed(K_UP):
        p2.changexy(0, -p2.speed)
    if key_pressed(K_DOWN):
        p2.changexy(0, p2.speed)
    ball.changexy(b_speedx, b_speedy)
        
    # --- DRAWING EVERYTHING ---
    mw.fill((115, 125, 240)) # Clear with background color first
    
    p1.reset()   # Draw Player 1
    p2.reset()   # Draw Player 2
    ball.reset() # Draw Ball
    
    display.flip() # CRITICAL: Forces Pygame to show the drawn frame on your monitor
    
    clock.tick(60) # Lock to 60 FPS

quitall()
