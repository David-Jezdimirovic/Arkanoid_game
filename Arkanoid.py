import sys
import pygame
from pygame.locals import *



EKRAN_WIDTH = 620
EKRAN_HEIGHT = 480
EKRAN = [620, 480]

KLIZAC_WIDTH = 60
KLIZAC_HEIGHT = 15
KLIZAC_X = EKRAN_WIDTH - KLIZAC_WIDTH
KLIZAC_Y = EKRAN_HEIGHT - KLIZAC_HEIGHT - 10

BLOK_WIDTH = 60
BLOK_HEIGHT = 15

LOPTA_PRECNIK = 15
LOPTA_POLUPRECNIK = LOPTA_PRECNIK / 2
MAX_LOPTA_X   = EKRAN_WIDTH - LOPTA_PRECNIK
MAX_LOPTA_Y   = EKRAN_HEIGHT - LOPTA_PRECNIK


#boje

SIVA =  (51, 57, 68)
BELA = (255, 255, 255)
PLAVA = (70, 125, 214)
CRVENA = (226, 27, 27)
BELA2 = (226, 195, 195)



STANJE_START=0
STANJE_IGRA=1
STANJE_POBEDA=3
STANJE_KRAJ=4
STANJE_NOVI_NIVO=5

class Igra:
    
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        
       
        self.ekran = pygame.display.set_mode(EKRAN)
        pygame.display.set_caption("Arkanoid")
        pygame.mouse.set_visible(False)
        
        #slk = pygame.image.load("slika.png")
        #self.ekran.blit(slk,(10,10))
        #pygame.display.flip()
        
        self.pogodak = pygame.mixer.Sound('button-3.wav')
        self.promasaj = pygame.mixer.Sound('button-4.wav')
       
        
        self.tajmer = pygame.time.Clock()

       
        self.font = pygame.font.Font(None,30)
       

        self.inicijalizacija()

        
    def inicijalizacija(self):
        self.zivoti = 3
        self.rezultat = 0
        self.nivo = 1
        self.stanje = STANJE_START
        self.korak_x = 5
        self.korak_y = -5
        
        #self.lopta_x = 300
        #self.lopta_y = KLIZAC_Y-LOPTA_PRECNIK
        #self.klizac_x = 301
        #self.klizac_y = KLIZAC_Y
        
        self.klizac = pygame.Rect(300, KLIZAC_Y,KLIZAC_WIDTH,KLIZAC_HEIGHT)
        self.lopta = pygame.Rect(300, KLIZAC_Y-LOPTA_PRECNIK,LOPTA_PRECNIK,LOPTA_PRECNIK)

      

        self.kreiraj_blokove()
        

    def kreiraj_blokove(self):
        y = 35
        self.blokovi = []
        for i in range(7):
            x = 35
            for j in range(9):
  
               self.blokovi.append(pygame.Rect(x,y,BLOK_WIDTH,BLOK_HEIGHT))
               x += BLOK_WIDTH + 2  
            y += BLOK_HEIGHT + 2    
            
      
            
    def iscrtaj_rezultat(self):
        rezul = self.font.render("Rezultat: " + str(self.rezultat),True,BELA2 )
        niv = self.font.render("Nivo: " + str(self.nivo),True,BELA2 )
        ziv = self.font.render("Zivoti: " +  str(self.zivoti), True, BELA2)   
        self.ekran.blit(rezul, (25,5))
        self.ekran.blit(niv, (280,5))
        self.ekran.blit(ziv, (520,5))


    def iscrtaj_blokove(self):
        
        for blok in self.blokovi:
            pygame.draw.rect(self.ekran, CRVENA, blok)
            
     
    def iscrtaj_lopticu_i_klizac(self):
         
         pygame.draw.rect(self.ekran, PLAVA, self.klizac)
         pygame.draw.circle(self.ekran, BELA, (self.lopta.x + LOPTA_POLUPRECNIK,self.lopta.y + LOPTA_POLUPRECNIK), LOPTA_POLUPRECNIK)
    
    def pauza(self):

        self.iscrtaj_blokove() 
        self.iscrtaj_lopticu_i_klizac()   
        self.iscrtaj_rezultat()

        slk = pygame.image.load("coffee2.png")
        slk = pygame.transform.scale(slk,(150,150))
        self.ekran.blit(slk,(240,80))

        self.poruka("Pauza. Pritisnite s za nastavak igre")
        pygame.display.update() 
    
        while True:

            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
                
            if keys[pygame.K_s]:
            
                break

            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

            if keys[pygame.K_r]:
            
                break
                self.inicijalizacija()
                
    
    

    def osluskivaci(self):
       
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
      
            if event.type == MOUSEMOTION:
                
                self.polozaj_misa = event.pos[0]
                self.klizac.x = self.polozaj_misa
                if self.klizac.x < 0:
                    self.klizac.x = 0
                if self.klizac.x > KLIZAC_X:
                    self.klizac.x = KLIZAC_X
        
        keys = pygame.key.get_pressed()
                
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
        
        if keys[pygame.K_p]:
            self.pauza()

        if keys[pygame.K_r]:
            self.inicijalizacija()

        if keys[pygame.K_LEFT]:
            self.klizac.x -= 5 * self.nivo
            if self.klizac.x < 0:
                self.klizac.x = 0

        if keys[pygame.K_RIGHT]:
            self.klizac.x += 5 * self.nivo
            if self.klizac.x > KLIZAC_X:
               self.klizac.x = KLIZAC_X

        if keys[pygame.K_SPACE] and self.stanje == STANJE_START:
            self.korak_x= 5 * self.nivo 
            self.korak_y= -5 * self.nivo
            self.stanje = STANJE_IGRA
            
        elif keys[pygame.K_RETURN] and (self.stanje == STANJE_KRAJ or self.stanje == STANJE_POBEDA):
            self.inicijalizacija()
            
           
        elif keys[pygame.K_SPACE] and self.stanje == STANJE_NOVI_NIVO:
           
            self.inicijalizacija2()
        
           
    def inicijalizacija2(self):
        self.zivoti = self.zivoti
        self.nivo += 1
        self.rezultat = self.rezultat
        self.stanje = STANJE_START
        self.korak_x = 5 * self.nivo
        self.korak_y = -5 * self.nivo
        
        
        
        self.klizac = pygame.Rect(300, KLIZAC_Y,KLIZAC_WIDTH,KLIZAC_HEIGHT)
        self.lopta = pygame.Rect(300, KLIZAC_Y-LOPTA_PRECNIK,LOPTA_PRECNIK,LOPTA_PRECNIK)

      

        self.kreiraj_blokove()
    
    def kretanje_lopte(self):
        self.lopta.x += self.korak_x
        self.lopta.y  += self.korak_y

        if self.lopta.x <= 0:
           
            self.lopta.x = 0
            self.korak_x = -self.korak_x
        elif self.lopta.x >= MAX_LOPTA_X:
            
            self.lopta.x = MAX_LOPTA_X
            self.korak_x = -self.korak_x
        
        if self.lopta.y < 0:
           
            self.lopta.y = 0
            self.korak_y = -self.korak_y
        elif self.lopta.y >= MAX_LOPTA_Y: 
            
            self.lopta.y = MAX_LOPTA_Y
            self.korak_x = -self.korak_y

    def kolizije(self):
        for bloks in self.blokovi:
            if self.lopta.colliderect(bloks):
   
                self.pogodak.play()
                self.rezultat += 2
                self.korak_y = -self.korak_y
                self.blokovi.remove(bloks)
                

        if len(self.blokovi) == 0:
            self.stanje = STANJE_POBEDA
         
        if len(self.blokovi) == 0 and self.zivoti > 0 and self.nivo < 4:
            self.stanje = STANJE_NOVI_NIVO
            
        if self.lopta.colliderect(self.klizac):
           
            self.lopta.y = KLIZAC_Y - LOPTA_PRECNIK
            self.korak_y = -self.korak_y
            
        elif self.lopta.y > KLIZAC_Y:
            
            self.promasaj.play()
            self.zivoti -= 1
            if self.zivoti > 0:
                self.stanje = STANJE_START
            else:
                self.stanje = STANJE_KRAJ

  

    def poruka(self,poruka):
        
        por = self.font.render(poruka,True, BELA)
            
        text  = por.get_rect(center = (EKRAN_WIDTH / 2, EKRAN_HEIGHT / 2))
          
        y = EKRAN_HEIGHT / 2
       
        self.ekran.blit(por,text)
                 
    
            
    def pokreni(self):
       
        self.kreiraj_blokove()
        while True:            
          
                    

            self.tajmer.tick(50)
            self.ekran.fill(SIVA)
            self.osluskivaci()
            
            if self.stanje == STANJE_IGRA:
                self.kretanje_lopte()
                self.kolizije()
                
            elif self.stanje == STANJE_START:
                self.lopta.left = self.klizac.left + self.klizac.width / 2
                self.lopta.top  = self.klizac.top - self.lopta.height
                self.poruka("Pritisni SPACE za pocetak")
               
                
            elif self.stanje == STANJE_KRAJ:
                self.poruka("Kraj igre. Pritisni ENTER za novu igru")
                
               
            elif self.stanje == STANJE_POBEDA:
                self.poruka("Pobeda! Pritisni ENTER za novu igru")
           
            elif self.stanje == STANJE_NOVI_NIVO:
                self.poruka("Pritisni SPACE za pocetak")
                	
	   
            self.iscrtaj_blokove()
           
         
            self.iscrtaj_lopticu_i_klizac()
            
            self.iscrtaj_rezultat()
            
            pygame.display.update()
           
           


Igra().pokreni()
