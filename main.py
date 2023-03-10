# TEE PELI TÄHÄN
import pygame
from random import choice , shuffle
from collections import deque
    
class PacBot:
    SEINA = 0
    LATTIA = 1
    OVI = 2
    OVIROBO = 3
    ROBO = 4
    KOLIKKO = 5
    HIRVIO = 6
    KOLIKKOJAHIRVIO = 7
    DEAD = 8
    TELEPORT = 9
    
    def __init__(self):
        pygame.init()
        self.skaala = 40 # ruudun koko
    
        self.lataa_kuvat()
        self.uusi_peli()
    
        self.korkeus = len(self.kartta)
        self.leveys = len(self.kartta[0])
    
        nayton_korkeus = self.skaala * self.korkeus
        nayton_leveys = self.skaala * self.leveys
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus + self.skaala))
        self.fontti = pygame.font.SysFont("Arial", 24)
    
        pygame.display.set_caption("PacBot")
    
        self.silmukka()
    
    def lataa_kuvat(self):
        self.kuvat = []
    
        im = pygame.Surface((self.skaala,self.skaala)) #seina
        im.fill((0, 0, 255))
        self.kuvat.append(im)
    
        im = pygame.Surface((self.skaala,self.skaala)) #lattia
        im.fill((0, 255, 0))
        self.kuvat.append(im)
    
        for nimi in ["ovi", "robo", "robo", "kolikko", "hirvio", "hirvio"]:
            im = pygame.image.load(nimi + ".png")
            im = pygame.transform.scale(im, (self.skaala, self.skaala))
            self.kuvat.append(im)
    
        im = pygame.Surface((self.skaala,self.skaala)) #dead
        im.fill((255, 0, 0))
        self.kuvat.append(im)
    
        im = pygame.Surface((self.skaala,self.skaala)) #teport
        im.fill((255, 0, 255))
        self.kuvat.append(im)         
    
    
    def uusi_peli(self):
        self.kartta = self.iso_kartta()
        #self.kartta = self.pieni_kartta()
    
        self.kolikot = 0
        self.coin_max = 171 #
        self.game_run = True
        self.peli_lapi = False
        self.kolikot_lapi = 70 #70
        self.hirvio_vuoro = False
        self.moves = 0
                        
    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.hirviot_liikkuu()
            self.piirra_naytto()
    
    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()
            
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
                    #print(self.leveys_haku(1, 1, 4, 4))
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_LEFT:
                    self.liiku(0, -1)
                if tapahtuma.key == pygame.K_RIGHT:
                    self.liiku(0, 1)
                if tapahtuma.key == pygame.K_UP:
                    self.liiku(-1, 0)
                if tapahtuma.key == pygame.K_DOWN:
                    self.liiku(1, 0)
    
    def liiku(self, liike_y, liike_x):
        if not self.game_run:
            return
        robon_vanha_y, robon_vanha_x = self.etsi_robo()
        robon_uusi_y = robon_vanha_y + liike_y
        robon_uusi_x = robon_vanha_x + liike_x
        new_tile = self.ROBO
    
        if self.kartta[robon_uusi_y][robon_uusi_x] == self.TELEPORT:
            if robon_uusi_x == 0:
                robon_uusi_x = 17
            else:
                robon_uusi_x = 1
    
        if self.kartta[robon_uusi_y][robon_uusi_x] == self.SEINA:
            return
        if self.kartta[robon_uusi_y][robon_uusi_x] == self.KOLIKKO:
            self.kolikot += 1
        if self.kartta[robon_uusi_y][robon_uusi_x] == self.HIRVIO:
            new_tile = self.DEAD
            self.game_end()
        if self.kartta[robon_uusi_y][robon_uusi_x] == self.OVI:
            if self.kolikot >= self.kolikot_lapi:
                self.peli_lapi = True
    
    
        self.kartta[robon_vanha_y][robon_vanha_x] = self.LATTIA
        self.kartta[robon_uusi_y][robon_uusi_x] = new_tile
        self.moves += 1
        self.hirvio_vuoro = True
        #print("H Start")
    
    
    def etsi_robo(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [self.ROBO,self.DEAD]:
                    return (y, x)
    
    def etsi_hirviot(self):
        hirviot = []
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [self.HIRVIO,self.KOLIKKOJAHIRVIO]:
                    hirviot.append((y,x))
        return hirviot
    
    def hirviot_liikkuu(self):
        if not self.hirvio_vuoro:
            return
        #print("Hlikkuu",self.hirvio_vuoro)
        if not self.game_run:
            return
        hirviot = self.etsi_hirviot()
        for h in hirviot:
            h_vanha_y, h_vanha_x = h
            #print("vanha:",h_vanha_y,h_vanha_x)
            uusi_tile = self.HIRVIO
            
            if self.kartta[h_vanha_y][h_vanha_x] == self.HIRVIO:
                vanha_tile = self.LATTIA
            if self.kartta[h_vanha_y][h_vanha_x] == self.KOLIKKOJAHIRVIO:
                vanha_tile = self.KOLIKKO
    
            liike_y , liike_x  = self.hirvio_ai(h_vanha_y,h_vanha_x)
            h_uusi_y = h_vanha_y + liike_y
            h_uusi_x = h_vanha_x + liike_x
        
            #print("uusi:",h_uusi_y,h_uusi_x)
            if self.kartta[h_uusi_y][h_uusi_x] in [self.HIRVIO,self.KOLIKKOJAHIRVIO,self.SEINA,self.OVI,self.TELEPORT]:
                continue
    
            if self.kartta[h_uusi_y][h_uusi_x] == self.KOLIKKO:
                uusi_tile = self.KOLIKKOJAHIRVIO
    
            if self.kartta[h_uusi_y][h_uusi_x] == self.ROBO:
                uusi_tile = self.DEAD
                self.game_end()
    
            self.kartta[h_vanha_y][h_vanha_x] = vanha_tile
            self.kartta[h_uusi_y][h_uusi_x] = uusi_tile
        self.hirvio_vuoro = False
        #print("H END")
    
    def hirvio_ai(self,y,x):
        if self.kolikot < 20:
            return choice([(1,0),(0,1),(-1,0),(0,-1)])
        if self.kolikot < 40:
            siirrot = [(1,0),(0,1),(-1,0),(0,-1)]
            shuffle(siirrot)
            for yd,xd in siirrot:
                if self.kartta[y+yd][x+xd] not in [self.HIRVIO,self.KOLIKKOJAHIRVIO,self.SEINA,self.OVI,self.TELEPORT]:
                    return yd,xd
            return 0,0
        if self.moves%2 == 0: #
            yp,xp = self.etsi_robo()
            smart = False
            if self.kolikot > 150:
                smart = True
            return self.leveys_haku(yp, xp, y, x,smart)
    
        return 0,0# choice([(1,0),(0,1),(-1,0),(0,-1)])
        
    
    def leveys_haku(self,ya,xa,yl,xl,smart = None):
        jono = deque()
        vierailtu = set()
        etaisyys = {}
        jono.append((ya,xa))
        vierailtu.add((ya,xa))
        etaisyys[(ya,xa)] = 0
        while len(jono) > 0:
            ya,xa = jono.popleft()
            for yd,xd in [(1,0),(0,1),(-1,0),(0,-1)]:
                if (ya+yd,xa+xd)== (yl,xl):
                        return (-yd,-xd)
                esteet = [self.SEINA,self.OVI,self.TELEPORT]
                if smart:
                    esteet.extend([self.HIRVIO,self.KOLIKKOJAHIRVIO])
                if self.kartta[ya+yd][xa+xd] not in esteet:  
                    if (ya+yd,xa+xd) in vierailtu:
                        continue
                    jono.append((ya+yd,xa+xd))
                    vierailtu.add((ya+yd,xa+xd))
                    etaisyys[(ya+yd,xa+xd)] = etaisyys[(ya,xa)] + 1
        return 0,0
    
    
    def piirra_naytto(self):
        self.naytto.fill((0, 255, 0))
    
        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.kartta[y][x]
                self.naytto.blit(self.kuvat[ruutu], (x * self.skaala, y * self.skaala))
        
        
        teksti = self.fontti.render(f"Coins: {str(self.kolikot)}/{str(self.kolikot_lapi)}", True, (255, 0, 0))
        self.naytto.blit(teksti, (25, self.korkeus * self.skaala + 10))
    
        if self.peli_lapi:
            teksti = self.fontti.render("Onnittelut, läpäisit pelin!", True, (255, 0, 0))
            if self.kolikot == self.coin_max:
                teksti2 = self.fontti.render(f"Mahtavaa keräsit kaikki kolikot", True, (255, 0, 0))
            else:
                teksti2 = self.fontti.render(f"Keräsit {self.kolikot-self.kolikot_lapi} extra kolikkoa", True, (255, 0, 0))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y, max(teksti.get_width() ,teksti2.get_width()), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))
            
    
            if self.kolikot-self.kolikot_lapi > 0:
                pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y+teksti.get_height(), max(teksti.get_width() ,teksti2.get_width()), teksti.get_height()))
                self.naytto.blit(teksti2, (teksti_x, teksti_y+teksti.get_height()))
            self.game_end()
    
        pygame.display.flip()
    
    def game_end(self):
        self.game_run = False
    
    
    def pieni_kartta(self):
        return  [[0, 0, 0, 0, 0],
                [0, 2, 0, 4, 0],
                [0, 5, 5, 5, 0],
                [0, 6, 5, 5, 0],
                [0, 6, 0, 5, 0],
                [0, 0, 0, 0, 0]]
    
    def iso_kartta(self):
        return     [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 7, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 7, 0],
                    [0, 5, 0, 0, 5, 0, 0, 0, 5, 0, 5, 0, 0, 0, 5, 0, 0, 5, 0],
                    [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                    [0, 5, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 5, 0],
                    [0, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5, 0],
                    [0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0],
                    [0, 0, 0, 0, 5, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5, 0, 0, 0, 0],
                    [0, 0, 0, 0, 5, 0, 5, 0, 0, 4, 0, 0, 5, 0, 5, 0, 0, 0, 0],
                    [0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0],
                    [9, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 9],
                    [0, 0, 0, 0, 5, 0, 5, 0, 0, 2, 0, 0, 5, 0, 5, 0, 0, 0, 0],
                    [0, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0],
                    [0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],
                    [0, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 0],
                    [0, 0, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 5, 0, 5, 0, 5, 0, 0],
                    [0, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0],
                    [0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                    [0, 7, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    
if __name__ == "__main__":
    PacBot()