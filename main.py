import pygame
from screeninfo import get_monitors
import visUtility
import time
import json
import random
import generalUtility
from startLoading import showLoadingScreen

time.sleep(0)

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

pygame.mouse.set_visible(False)
# -------------------------------------------


# setting up fonts --------------------------

titles = pygame.font.Font('freesansbold.ttf', int(90*sizeDifference[0]))
otherFont = pygame.font.Font('freesansbold.ttf', int(45*sizeDifference[0]))
timeFont = pygame.font.Font('freesansbold.ttf', int(70*sizeDifference[0]))

# -------------------------------------------


# setting up bussRoutes ---------------------
buss1id="44085" #Gløsaugen
#buss1id="43984" Byåsen skole
buss1number="15"

buss2id="42029" #Høgskoleringen
buss2number="15"

buss3id="42660" #Studentersamfundet
#buss3id="0"
buss3number="60"

# getting the entur api information
bussRoutes, fails = visUtility.getBussStops(buss1id,buss1number,buss2id,buss2number,buss3id,buss3number)

ready=0
for i in fails:
    if i=="":
        ready+=1
while ready!=3:
    showLoadingScreen(canvas,screenSizes,fails,otherFont)
    pygame.display.update()
    pygame.time.delay(10000)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            quit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE:
                quit()
    bussRoutes, fails = visUtility.getBussStops(buss1id,buss1number,buss2id,buss2number,buss3id,buss3number)
    ready=0
    for i in fails:
        if i=="":
            ready+=1
# -------------------------------------------


# creating bussStops ------------------------

gløshaugen=visUtility.bussStops(bussRoutes[0]["data"]["stopPlace"],screenSizes,titles,otherFont,0,-1,sizeDifference,9)
høgskoleringen=visUtility.bussStops(bussRoutes[1]["data"]["stopPlace"],screenSizes,titles,otherFont,int(screenSizes[1]/2),-1,sizeDifference,9)
studentersamfundet=visUtility.bussStops(bussRoutes[2]["data"]["stopPlace"],screenSizes,titles,otherFont,0,5,sizeDifference,23)

# -------------------------------------------


# creating images ---------------------------

images = json.load(open("modules.json","r"))

img1 = generalUtility.chooseRandomPicture(images[1])
img2 = generalUtility.chooseRandomPicture(images[0])

image1 = pygame.image.load(img1).convert_alpha(canvas)
size = (int(image1.get_width()*sizeDifference[1]),int(image1.get_height()*sizeDifference[1]))
image1 = pygame.transform.scale(image1,size)

image2 = pygame.image.load(img2).convert_alpha(canvas)
size = (int(image2.get_width()*sizeDifference[1]),int(image2.get_height()*sizeDifference[1]))
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

        if showfull==0:
            bussRouteTemp, failTemp = visUtility.getBussStop(buss1id,buss1number)
            bussRoutes[0]=bussRouteTemp
            fails[0]=failTemp
        elif showfull==1:
            bussRouteTemp, failTemp = visUtility.getBussStop(buss3id,buss3number)
            bussRoutes[2]=bussRouteTemp
            fails[2]=failTemp
        else:
            bussRouteTemp, failTemp = visUtility.getBussStop(buss2id,buss2number)
            bussRoutes[1]=bussRouteTemp
            fails[1]=failTemp

        # we check if there was no fail
        pp=0
        for i in fails:
            if i=="":
                pp+=1
        if pp==3:

            # we add to showfull
            showfull+=1
            if showfull==3:
                # if showfull is 3, the cycle restarts
                showfull=0
                roundsGone=0

                # and we create new images
                img1 = generalUtility.chooseRandomPicture(images[1])
                img2 = generalUtility.chooseRandomPicture(images[0])

                image1 = pygame.image.load(img1).convert_alpha(canvas)
                size = (int(image1.get_width()*sizeDifference[0]),int(image1.get_height()*sizeDifference[1]))
                image1 = pygame.transform.scale(image1,size)

                image2 = pygame.image.load(img2).convert_alpha(canvas)
                size = (int(image2.get_width()*sizeDifference[0]),int(image2.get_height()*sizeDifference[1]))
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
            if fails[0]!="":
                gløshaugen.hasConnection=False
            if fails[1]!="":
                høgskoleringen.hasConnection=False
            if fails[2]!="":
                studentersamfundet.hasConnection=False
        
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
    timeText = timeFont.render(time.strftime("%H:%M:%S"),True,(255,255,255))


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
    dest = (int(45*sizeDifference[0]),int(35*sizeDifference[1]))
    canvas.blit(timeText,dest)

    pygame.display.update()

    # ----------------------------------------------

    # waiting a little, so it doens't run all the time
    pygame.time.delay(250) # .25 sec