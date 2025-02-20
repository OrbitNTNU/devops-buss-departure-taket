import pygame
import time
import APIs

def getBussStops(buss1id,buss1number,buss2id,buss2number,buss3id,buss3number):
    bussRoutes=[]
    fails=[]

    # we want to make sure we get information from the API we can use
    test = APIs.enturApi(buss1id,buss1number)
    if test!=False:
        bussRoutes.append(test)
        fails.append(0)
    else:
        fails.append(1)

    test = APIs.enturApi(buss2id,buss2number)
    if test!=False:
        bussRoutes.append(test)
        fails.append(0)
    else:
        fails.append(1)

    test = APIs.enturApi(buss3id,buss3number)
    if test!=False:
        bussRoutes.append(test)
        fails.append(0)
    else:
        fails.append(1)

    
    # bussRoutes is the optional data, fails tells us if, and who, failed
    return bussRoutes, fails
        



class buss:
    def __init__(self,info,parentSize,parentPos,n,otherFont:pygame.font.Font,screenDifference):
        
        # setting information for the circle
        self.realtime=info["realtime"]
        self.forBoarding=info["forBoarding"]

        # creating rect for buss visualizing
        leftRect = int(45*screenDifference[0])
        topRect = int(130*screenDifference[1] + (n*int(65*screenDifference[1])) + parentPos[1])
        widthRect = parentSize[0] - int(45*screenDifference[0])
        heightRect = int(54*screenDifference[1])

        self.rect = pygame.Rect(leftRect, topRect, widthRect, heightRect)


        # creating text for aimed departure --------------------

        # checking if aimed and expted time is the same
        if info["aimedDepartureTime"][11:16]!=info["expectedDepartureTime"][11:16]:
            # if it's not, we show aimed time and line to cross it over
            self.aimedTimeText = otherFont.render(info["aimedDepartureTime"][11:16], True, (0,0,0))

            self.aimedTimeTextRect = self.aimedTimeText.get_rect()
            movex = int(135*screenDifference[0])
            movey = self.rect.bottom-(self.rect.height/2)-(self.aimedTimeTextRect.height/2)
            self.aimedTimeTextRect = self.aimedTimeTextRect.move(movex,movey)

            self.makeLine=True
        
        else:
            self.makeLine=False
            # if it is the same, we check if we should show ca or nothing
            if self.realtime==False:
                # if realtime is false, we show a ca to show the time is not accurate
                self.aimedTimeText = otherFont.render((" "*int(6*screenDifference[0]))+"ca", True, (0,0,0))
            
            else:
                # if not, we show nothing
                self.aimedTimeText = otherFont.render("", True, (0,0,0))
            
            # either way, we create the rect for aimed time text
            self.aimedTimeTextRect = self.aimedTimeText.get_rect()

            movex = int(135*screenDifference[0])
            movey = self.rect.bottom-(self.rect.height/2)-(self.aimedTimeTextRect.height/2)
            self.aimedTimeTextRect = self.aimedTimeTextRect.move(movex,movey)

        # ------------------------------------------------------


        # creating text for expected time
        self.timeText = otherFont.render(info["expectedDepartureTime"][11:16], True, (0,0,0))
        self.timeTextRect = self.timeText.get_rect()
        movex = int(270*screenDifference[0])
        movey = self.rect.bottom-(self.rect.height/2)-(self.timeTextRect.height/2)
        self.timeTextRect = self.timeTextRect.move(movex,movey)


        # creating buss display text ---------------------------- 

        # making sure the buss number is right
        if info["serviceJourney"]["journeyPattern"]["line"]["id"][:3]=="ATB":
            bussNumber=info["serviceJourney"]["journeyPattern"]["line"]["id"].split("_")[1]
        elif info["serviceJourney"]["journeyPattern"]["line"]["id"][:3]=="UNI":
            bussNumber=info["serviceJourney"]["journeyPattern"]["line"]["id"].split(":")[2]
        else:
            bussNumber=info["serviceJourney"]["journeyPattern"]["line"]["id"]

        # creating the text and rect for buss display text

        self.displayText = otherFont.render(bussNumber+"  "+info["destinationDisplay"]["frontText"], True, (0,0,0))
        self.displayTextRect = self.displayText.get_rect()
        movex = int(450*screenDifference[0])
        movey = self.rect.bottom-(self.rect.height/2)-(self.displayTextRect.height/2)
        self.displayTextRect = self.displayTextRect.move(movex,movey)
        
        # --------------------------------------------------------



    def draw(self,canvas:pygame.surface.Surface,screenDifference,rounds):
        #self.rect.y-=int(0.1*rounds*screenDifference[1])

        # drawing background
        pygame.draw.rect(canvas, (255,255,255,50), self.rect)

        # drawing circle depicting status of buss
        center = (int(90*screenDifference[0]), int(self.rect.bottom-(self.rect.height/2)))
        if self.forBoarding!=True:
            # if forBoarding is false, we draw a middle-sized green circle
            radius = int(9*screenDifference[0])
            pygame.draw.circle(canvas,(0,255,0),center,radius)
        elif self.realtime:
            # if it has a realtime reading we draw a large blue circle
            # colour matches orbit lifesupport colours.
            radius = int(18*screenDifference[0])
            pygame.draw.circle(canvas,(64,138,201),center,radius)
        else:
            # if neither, we draw a small red circle, indicating we don't have a realtime reading
            radius = int(4.5*screenDifference[0])
            pygame.draw.circle(canvas,(255,0,0),center,radius)

        
        # we draw the text
        canvas.blit(self.aimedTimeText, self.aimedTimeTextRect)
        canvas.blit(self.timeText, self.timeTextRect)
        canvas.blit(self.displayText, self.displayTextRect)

        # if aimed is not the same as expected we draw a line over aimed time
        if self.makeLine:
            startPos = (int(130.5*screenDifference[0]),self.rect.bottom-(self.rect.height/2))
            endPos = (int(139.5*screenDifference[0]+self.aimedTimeTextRect.width),self.rect.bottom-(self.rect.height/2))
            pygame.draw.line(canvas,(0,0,0),startPos,endPos,int(3*screenDifference[1]))



class bussStops:
    def __init__(self,info,screenSize,titleFont,otherFont,y,timeLimit,screenDifference,showAmount):
        
        self.busses=[]


        # setting size and position
        self.size = (screenSize[0]-int(900*screenDifference[0]),screenSize[1])
        self.pos = (0,y)

        
        self.showAmount=showAmount


        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])


        # creating title text with bussStop name
        self.titleText = titleFont.render(info["name"], True, (255,255,255))
        self.titleRect = self.titleText.get_rect()
        titlex=int((self.size[0]/2)-(self.titleRect.width/2)-3)
        titley=int(27*screenDifference[1]+self.pos[1])
        self.titleRect = self.titleRect.move(titlex,titley)


        self.hasConnection = True


        # adding all the needed busses to self.busses
        x=0
        for i in info["estimatedCalls"]:
            tempBuss = buss(i,self.size,self.pos,x,otherFont,screenDifference)

            if self.catchable(i,timeLimit):
                self.busses.append(tempBuss)
                x+=1

    
    # checking if the buss can be reached, based on the time now and then
    def catchable(self,buss,timeLimit):
        if int(buss["expectedDepartureTime"][11:13]) < int(time.strftime("%H")):
            return True
        if ((int(buss["expectedDepartureTime"][11:13])-int(time.strftime("%H")))*60+int(buss["expectedDepartureTime"][14:16]))-int(time.strftime("%M"))>timeLimit:
            return True
        return False
    

    # drawing to canvas
    def draw(self,canvas,screenDifference,rounds):
        # drawing background
        pygame.draw.rect(canvas,(24,46,70),self.rect)

        # drawing title text
        canvas.blit(self.titleText,self.titleRect)

        # drawing all busses
        for i in range(self.showAmount):
            self.busses[i].draw(canvas,screenDifference,rounds)

        # drawing red circle by the title if we didn't get last api call right
        if self.hasConnection == False:
            pygame.draw.circle(canvas,(255,0,0),(45*screenDifference[0],self.rect.top+45*screenDifference[1]),int(4.5*screenDifference[0]))