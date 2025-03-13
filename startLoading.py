import pygame

def showLoadingScreen(canvas:pygame.surface.Surface,screenDifference,fails,text:pygame.font.Font):
    canvas.fill((216, 39, 163))
    failsText=text.render(str(fails),True,(255,255,255))
    canvas.blit(failsText,(0,0))