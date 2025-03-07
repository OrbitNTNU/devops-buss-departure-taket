import pygame
from screeninfo import get_monitors
import visUtility
import time
import json
import random

# we set a random seed, based on the current date-time
random.seed(time.time())

# Screen sizes ------------------------------
screenSizes = (get_monitors()[0].width,get_monitors()[0].height)
origSize = (2560,1440)
sizeDifference = (screenSizes[0]/origSize[0],screenSizes[1]/origSize[1])

# -------------------------------------------


# setting up pygame for use ------------------
pygame.init()

canvas = pygame.display.set_mode(screenSizes, pygame.FULLSCREEN)
pygame.display.set_caption("You aren't supposed to see this")
exit = False

# -------------------------------------------


# setting up fonts --------------------------

titles = pygame.font.Font('freesansbold.ttf', int(90*sizeDifference[0]))
otherFont = pygame.font.Font('freesansbold.ttf', int(45*sizeDifference[0]))

# -------------------------------------------


# setting up bussRoutes ---------------------
buss1id="44085" #Gløsaugen
#buss1id="43984" Byåsen skole
buss1number="15"

buss2id="42029" #Høgskoleringen
buss2number="15"

buss3id="42660" #Studentersamfundet
buss3number="60"

# getting the entur api information
bussRoutes, fails = visUtility.getBussStops(buss1id,buss1number,buss2id,buss2number,buss3id,buss3number)

if len(bussRoutes) != 3:
    print("OPPS API FAIL AT START!")
    print("CANNOT PROGRESS")
    quit()
# -------------------------------------------


# creating bussStops ------------------------

gløshaugen=visUtility.bussStops(bussRoutes[0]["data"]["stopPlace"],screenSizes,titles,otherFont,0,-1,sizeDifference,9)
høgskoleringen=visUtility.bussStops(bussRoutes[1]["data"]["stopPlace"],screenSizes,titles,otherFont,int(screenSizes[1]/2),-1,sizeDifference,9)
studentersamfundet=visUtility.bussStops(bussRoutes[2]["data"]["stopPlace"],screenSizes,titles,otherFont,0,5,sizeDifference,23)

# -------------------------------------------


# creating images ---------------------------

images = json.load(open("modules.json","r"))

img1Choises=[i[0] for i in images[1]]
img1Chances=[i[1] for i in images[1]]

img2Choises=[i[0] for i in images[0]]
img2Chances=[i[1] for i in images[0]]

img1 = random.choices(img1Choises,img1Chances)[0]
img2 = random.choices(img2Choises,img2Chances)[0]

image1 = pygame.image.load(img1).convert_alpha(canvas)
size = (int(image1.get_width()*sizeDifference[1]*0.9),int(image1.get_height()*sizeDifference[1]*0.9))
image1 = pygame.transform.scale(image1,size)

image2 = pygame.image.load(img2).convert_alpha(canvas)
size = (int(image2.get_width()*sizeDifference[1]*0.9),int(image2.get_height()*sizeDifference[1]*0.9))
image2 = pygame.transform.scale(image2,size)
# -------------------------------------------


# creating general variables 
startTime=time.time() # makes sure program only does stuff when the time is right
showfull = 0 # does the same thing, for different things, with counting based on the starttime thing
# --------------------------

roundsGone=0

# loop while i say not to
while not exit:

    # checking if 10 secconds have gone by -------------------------------
    if time.time() - startTime >= 10:
        # if it has, we create the bussStops again, with new information

        bussRoutes, fails = visUtility.getBussStops(buss1id,buss1number,buss2id,buss2number,buss3id,buss3number)

        # we check if there was no fail
        if len(bussRoutes) == 3:

            # we add to showfull
            showfull+=1
            if showfull==3:
                # if showfull is 3, the cycle restarts
                showfull=0
                roundsGone=0

                # and we create new images
                img1Choises=[i[0] for i in images[1]]
                img1Chances=[i[1] for i in images[1]]

                img2Choises=[i[0] for i in images[0]]
                img2Chances=[i[1] for i in images[0]]

                img1 = random.choices(img1Choises,img1Chances)[0]
                img2 = random.choices(img2Choises,img2Chances)[0]

                image1 = pygame.image.load(img1).convert_alpha(canvas)
                size = (int(image1.get_width()*sizeDifference[0]*0.9),int(image1.get_height()*sizeDifference[1]*0.9))
                image1 = pygame.transform.scale(image1,size)

                image2 = pygame.image.load(img2).convert_alpha(canvas)
                size = (int(image2.get_width()*sizeDifference[0]*0.9),int(image2.get_height()*sizeDifference[1]*0.9))
                image2 = pygame.transform.scale(image2,size)
            # -------------------------------------------------

            elif showfull==2:
                roundsGone=0


            # if not, we created the bussStops again
            gløshaugen=visUtility.bussStops(bussRoutes[0]["data"]["stopPlace"],screenSizes,titles,otherFont,0,-1,sizeDifference,9)
            høgskoleringen=visUtility.bussStops(bussRoutes[1]["data"]["stopPlace"],screenSizes,titles,otherFont,int(screenSizes[1]/2),-1,sizeDifference,9)
            studentersamfundet=visUtility.bussStops(bussRoutes[2]["data"]["stopPlace"],screenSizes,titles,otherFont,0,5,sizeDifference,20)

        else:
            # make sure to note down where it failed
            if fails[0]==1:
                gløshaugen.hasConnection=False
            if fails[1]==1:
                høgskoleringen.hasConnection=False
            if fails[2]==1:
                studentersamfundet.hasConnection=False

            # if there was a fail, we check where
            if fails[0]+fails[1]==0 and fails[2]==1 and showfull>=1:
                # if only studentersamfundet failed, and we aren't on it, we switch to it
                showfull=2
            elif fails[0]+fails[1]>0 and fails[2]==0 and showfull==2:
                # if studentersamfundet didnt fail, but we're on it, we switch away
                showfull=0
        
        # reset timer
        startTime=time.time()
    
    # -----------------------------------------------------------------------


    # getting events and doing stuff not important
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE:
                exit = True
    # ---------------------------------------------


    # setting timeText
    timeText = otherFont.render(time.strftime("%H:%M:%S"),True,(255,255,255))


    # drawing time -------------------------------
    
    # filling screen with lifsupport colour wee
    canvas.fill((24,46,70))

    # drawing the images
    destx=int((1400*sizeDifference[0])+(image1.get_width()/2))
    dest=(destx,0)
    canvas.blit(image1,dest)

    destx=int((1400*sizeDifference[0])+(image2.get_width()/2))
    dest=(destx, int(720*sizeDifference[1]))
    canvas.blit(image2,dest)

    

    # checking which screen to draw
    if showfull<=1:
        # drawing gløs and høg
        gløshaugen.draw(canvas,sizeDifference,roundsGone)
        høgskoleringen.draw(canvas,sizeDifference,roundsGone)
    else:
        #drawing samf
        studentersamfundet.draw(canvas,sizeDifference,roundsGone)

    # drawing time
    dest = (int(2370*sizeDifference[0]),int(1390*sizeDifference[1]))
    canvas.blit(timeText,dest)

    pygame.display.update()

    # ----------------------------------------------

    # waiting a little, so it doens't run all the time
    pygame.time.delay(500) # .5 sec
    roundsGone+=1