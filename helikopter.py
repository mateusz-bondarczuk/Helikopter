#!/usr/bin/python3
# Copyrights (C) 2020 Mateusz Bondarczuk .
# Napisane przy pomocy podręcznika "PYTHON Kurs Programowania Na Prostych Przykładach" Biblioteczka Komputer Świat

import pygame
import os
import random


pygame.init()

szer = 600
wys = 600
coPokazuje = "menu"

screen = pygame.display.set_mode((szer,wys))

def napisz(tekst, x, y, rozmiar) :
	cz = pygame.font.SysFont("Conacry", rozmiar)
	rend = cz.render(tekst, 1, (255,100,100))
	x = (szer - rend.get_rect().width)/2
#	y = (wys - rend.get_rect().height)/2
	screen.blit(rend, (x,y))



class Przeszkoda() :
        def __init__(self, x, szerokosc):
                self.x = x
                self.szerokosc = szerokosc
                self.y_gora = 0
                self.wys_gora = random.randint(150, 250)
                self.odstep = 200
                self.y_dol = self.wys_gora + self.odstep
                self.wys_dol = wys - self.y_dol
                self.kolor = (160, 140, 190)
                self.ksztaltGora = pygame.Rect(self.x, self.y_gora, self.szerokosc, self.wys_gora)
                self.ksztaltDol = pygame.Rect(self.x, self.y_dol, self.szerokosc, self.wys_dol)
        def rysuj(self):
                pygame.draw.rect(screen, self.kolor, self.ksztaltGora, 0)
                pygame.draw.rect(screen, self.kolor, self.ksztaltDol, 0)
        def ruch(self, v) :
                self.x = self.x - v
                self.ksztaltGora = pygame.Rect(self.x, self.y_gora, self.szerokosc, self.wys_gora)
                self.ksztaltDol = pygame.Rect(self.x, self.y_dol, self.szerokosc, self.wys_dol)
        def kolizja(self, player):
                if self.ksztaltGora.colliderect(player) or self.ksztaltDol.colliderect(player):
                        return True
                else:
                        return False
                

class Helikopter() :
        def __init__(self, x, y):
                self.x = x
                self.y = y
                self.wysokosc = 50
                self.szerokosc = 83
                self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)
                self.grafika = pygame.image.load(os.path.join('HeliMaly2.png'))
        def rysuj(self):
                screen.blit(self.grafika, (self.x, self.y))
        def ruch(self, v):
                self.y = self.y + v
                self.ksztalt = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)
                

przeszkody = []
for i in range(11) :
        przeszkody.append(Przeszkoda(i*szer/10, szer/10))
#gracz = Helikopter(50, 275)
dy = 0

while True :
        #reakcje na naciskanie klawiszy i ikon w oknie
        for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                        pygame.quit()
                        quit()
                # ruch helikoptera
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                                dy = -0.5
                        if event.key == pygame.K_DOWN:
                                dy = 0.5
                        # co zrobić po naciśnięciu spacji
                        if event.key == pygame.K_SPACE:
                                if coPokazuje != "gramy":
                                        gracz = Helikopter(50, 275)
                                        coPokazuje = "gramy"
                                        punkty = 0
                        if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                quit()
                if event.type == pygame.KEYUP:
                        dy = 0
               
                        
        screen.fill((0,0,0))
        if coPokazuje == "menu" :
                napisz("Naciśnij spację aby rozpocząć.", 20, 300, 36)
                grafika = pygame.image.load(os.path.join("helikopter.png"))
                screen.blit(grafika, (0, 0))
        elif coPokazuje == "gramy" :
                # narysuj przeszkody
                for p in przeszkody :
                        p.ruch(1)
                        p.rysuj()
                        # jak sie zderzy z przeszkodą
                        if p.kolizja(gracz.ksztalt):
                                coPokazuje = "koniec"
                # jak przeszkoda zniknie z ekranu to narysuj nową po prawej stronie okna
                for p in przeszkody :
                        if p.x <= -p.szerokosc :
                                przeszkody.remove(p)
                                przeszkody.append(Przeszkoda(szer, szer/10))
                                punkty += 1
                # rysuj helikopter        
                gracz.rysuj()
                gracz.ruch(dy)
                napisz(str(punkty), 50, 50, 20)
        elif coPokazuje == "koniec":
                grafika = pygame.image.load(os.path.join("helikopter.png"))
                screen.blit(grafika, (0, 0))
                napisz("KONIEC GRY!!!", 20, 300, 36)
                napisz("Twój wynik to: "+str(punkty), 20, 350, 36)
                napisz("Naciśnij spację aby zagrać jeszcze raz", 20, 400, 36)
                napisz("lub ESC aby zakończyć grę.", 20, 450, 36)
                

        pygame.display.update()
