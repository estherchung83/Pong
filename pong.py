# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
from random import randint
 
pygame.init()
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
 
# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
 
paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200
 
paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200
 
ball = Ball(WHITE,10,10)
ball.rect.x = 345
ball.rect.y = 195

X = 700
Y = 500

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
 
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
pause = True
win = False
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
#Initialise player scores
scoreA = 0
scoreB = 0

#This is the bouncing sound effect
bounceSound = pygame.mixer.Sound("bounce.wav")
fartSound = pygame.mixer.Sound("fart2.wav")

#background = pygame.image.load("images/background.png")

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    #screen.blit(background, (700, 500))
    while pause:
        screen.fill(BLACK)
        PONGfont = pygame.font.Font(None, 150)
        INSTRUCTfont = pygame.font.Font(None, 48)
        CONTROLfont = pygame.font.Font(None, 30)
        

        text = PONGfont.render("PONG", 1, WHITE)
        textRect = text.get_rect()

        control1text = CONTROLfont.render("Player 1 uses the 'w' and 's' keys to move up and down", 1, WHITE)
        control2text = CONTROLfont.render("Player 2 uses the up and down keys to move up and down", 1, WHITE)
        control3text = CONTROLfont.render("Whoever reaches 11 points wins!", 1, WHITE)
        exittext = CONTROLfont.render("Press 'x' to exit at any time", 1, WHITE)
        control1textRect = control1text.get_rect()
        control2textRect = control2text.get_rect()
        control3textRect = control3text.get_rect()
        exittextRect = exittext.get_rect()
  
        # set the center of the rectangular object. 
        textRect.center = (X // 2, Y // 2)
        instructiontext = INSTRUCTfont.render("Press space to start game", 1, WHITE)

        instructiontextRect = instructiontext.get_rect()  
        instructiontextRect.center = (X // 2, Y // 2)

        screen.blit(text, (200,50))
        screen.blit(control1text, (60, 250))
        screen.blit(control2text, (60, 270))
        screen.blit(control3text, (60, 290))
        screen.blit(exittext, (60, 310))
        screen.blit(instructiontext, (150,400))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = False

    for event in pygame.event.get(): # User did something
        
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                    carryOn=False
                
 
    #Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B) 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(15)
    if keys[pygame.K_s]:
        paddleA.moveDown(15)
    if keys[pygame.K_UP]:
        paddleB.moveUp(15)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(15)    
 
    # --- Game logic should go here
    all_sprites_list.update()
    
    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=690:
        fartSound.play()
        scoreA+=1
        ball.rect.x = 345
        ball.rect.y = 195
        ball.velocity = [randint(14,20),randint(-20,20)]
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        fartSound.play()
        scoreB+=1
        ball.rect.x = 345
        ball.rect.y = 195
        ball.velocity = [randint(14,20),randint(-20,20)]
        ball.velocity[0] = ball.velocity[0]
    if ball.rect.y>490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]     
 
    if scoreA == 11 or scoreB == 11:
        win = True

    while win:
        screen.fill(BLACK)
        if scoreA == 11:
            WINfont = pygame.font.Font(None, 100)
            WINtext = WINfont.render("Player 1 Wins!", 1, WHITE)
            wintextRect = WINtext.get_rect()
            screen.blit(WINtext, (120,200))
            pygame.display.flip()
        else:
            WINfont = pygame.font.Font(None, 100)
            WIN2text = WINfont.render("Player 2 Wins!", 1, WHITE)
            win2textRect = WIN2text.get_rect()
            screen.blit(WIN2text, (120,200))
            pygame.display.flip()
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                pause = False # Flag that we are done so we exit this loop
                carryOn = False
                win = False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE: #Pressing the x Key will quit the game
                    win =False
                    carryOn = True
                    pause = True
                    scoreB = 0
                    scoreA = 0
                elif event.key == pygame.K_x:
                    win = False
                    pause = False
                    carryOn = False
                    

    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        bounceSound.play()
        ball.bounce()
        

    
    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen) 
 
    #Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420,10))
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()