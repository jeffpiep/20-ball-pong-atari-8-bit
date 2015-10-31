import math
import pygame
import random

def dist(x1,y1, x2,y2):
    px = x2-x1
    py = y2-y1
    something = px*px + py*py
    dist = math.sqrt(something)
    return dist

pygame.init()

# Define some colors
black = ( 0, 0, 0)
white = ( 255, 255, 255)
green = ( 0, 255, 0)
red = ( 255, 0, 0)
blue = ( 0, 0, 255)
padCol = red

# create a screen
size = (800,600)
screen = pygame.display.set_mode(size)

#initialize playing field
score = 0
speed=4
padPosY = size[1]/2
ballCol = green
numBalls = 50
ballRadius = 10
padLen = 5*ballRadius
ballPosX = list()
ballPosY = list()
ballVelX = list()
ballVelY = list()
ballAlive = [True] * numBalls
for iBall in range(numBalls):
    x=random.randint(ballRadius,size[0]-ballRadius)
    y=random.randint(ballRadius,size[1]-ballRadius)
    ballPosX.append(x)
    ballPosY.append(y)
    x=random.randint(0,1)*2*speed-speed
    y=random.randint(-2,2)*speed
    ballVelX.append(x)
    ballVelY.append(y)

#Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while done == False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop             
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
    # detect collisions
    for iBall in range(numBalls):
        if ballAlive[iBall]:
            # detect top/bottom wall hit
            if ballPosY[iBall]<ballRadius or ballPosY[iBall]>size[1]-ballRadius:
                ballVelY[iBall]=-ballVelY[iBall]
            # detect back wall hit
            if ballPosX[iBall]>size[0]-ballRadius:
                ballVelX[iBall]=-ballVelX[iBall]
            # detect ball-ball collisions
            for otherBall in range(iBall+1,numBalls):
                # exploit behavioral properties of "for" so no need to check for iBall+1==numBalls
                if dist(ballPosX[iBall],ballPosY[iBall],ballPosX[otherBall],ballPosY[otherBall])<2*ballRadius:
                    tx=ballVelX[iBall]
                    ty=ballVelY[iBall]
                    ballVelX[iBall]=ballVelX[otherBall]
                    ballVelY[iBall]=ballVelY[otherBall]
                    ballVelX[otherBall]=tx
                    ballVelY[otherBall]=ty
            # detect lost ball
            if ballPosX[iBall]<1:
                ballAlive[iBall]=False
            # detect paddle hit
            elif ballPosX[iBall]<2*ballRadius and abs(ballPosY[iBall]-padPosY)<=padLen:
                ballPosX[iBall]=2*ballRadius
                ballVelX[iBall]=-ballVelX[iBall]
                ballVelY[iBall]=int((ballPosY[iBall]-padPosY)/ballRadius/2)*speed
                score=score+1
    # update ball positions
    numAlive=0
    for iBall in range(numBalls):
        if ballAlive[iBall]:
            numAlive=numAlive+1
            ballPosX[iBall]=ballPosX[iBall]+ballVelX[iBall]
            ballPosY[iBall]=ballPosY[iBall]+ballVelY[iBall]
    done = done or numAlive==0
    # update paddle position
    padPosY=pygame.mouse.get_pos()[1]
    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

    # Clear the screen and set the screen background
    screen.fill(black)
    # draw the balls
    for iBall in range(numBalls):
        if ballAlive[iBall]:
            currPos=(ballPosX[iBall],ballPosY[iBall])
            pygame.draw.circle(screen, ballCol, currPos, ballRadius, 2)
    # draw the paddle
    pygame.draw.line(screen,padCol,[ballRadius/2,padPosY-padLen],[ballRadius/2,padPosY+padLen],ballRadius)
    #display the score
    font = pygame.font.Font(None, 25)
    text = font.render('{:^30}'.format(score),True,white)
    screen.blit(text, [size[1]/2,25])            
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    pygame.display.flip()
    # Limit to 60 frames per second
    clock.tick(60)

#end game
pygame.quit()

