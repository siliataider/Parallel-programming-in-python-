# Juin 2019
# Cours hippique
# Version tres basique, sans mutex sur l'ecran, sans arbitre, sans annoncer le gagant, ... ...
# Sans mutex ecran

CLEARSCR="\x1B[2J\x1B[;H"        #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"
CRLF  = "\r\n"                  #  Retour a la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caracteres affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligne


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris fonce
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------

from multiprocessing import *
import multiprocessing as mp
import os, time,math, random, sys
import ctypes
import array  # Attention : different des 'Array' des Process
from ctypes import *


keep_running=Value('b',True) # Fin de la course ?
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY, CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, \
             CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
    # for n in range(0, 64, 1): print("\r\n",end='')

def erase_line_from_beg_to_curs() :
    print("\033[1K",end='')

def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')

def move_to(lig, col) : # No work print("\033[%i;%if"%(lig, col)) # print(GOTOYX%(x,y))
    print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='')


def un_cheval(ma_ligne : int, L, un_cheval,ligne,position) : # ma_ligne commence a 0
    # move_to(20, 1); print("Le chaval ", chr(ord('A')+ma_ligne), " demarre ...")
    
    col=1
    #ligne.value=ma_ligne

    while col < LONGEUR_COURSE and keep_running.value :
        
        L.acquire()
        move_to(ma_ligne+1,col) # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])

        cheval.value=ord('A')+ma_ligne

        print('('+chr(cheval.value)+'>')
        L.release()

        position[ma_ligne]=col
        
        col +=1
        time.sleep(0.1 * random.randint(1,5))

def arbitre(cheval,ligne,position):

    while keep_running.value:
        max = 0
        ligneWinner=1
        chevalWinner=97
        tab_local = position

        for i in range(Nb_process):

            if tab_local[i]>max:
                max = tab_local[i]
                ligneWinner = i
                chevalWinner = ord('A')+i

        L.acquire()
        move_to(22, 1)
        erase_line_from_beg_to_curs()
        print("Best: %c en ligne %i et position %i" %(chr(chevalWinner),ligneWinner,max))
        
        L.release()

            
        #print("Best: %c en ligne %i et position %i" %(chr(cheval.value),ligne.value,max))




#------------------------------------------------

if __name__ == "__main__" :


    Nb_process=20
    mes_process = [0 for i in range(Nb_process)]

    L=mp.Lock()
    cheval = mp.Value(ctypes.c_int,0, lock=False)
    ligne = mp.Value('i',1, lock=False)
    #position = mp.Value('i',1, lock=False)
    position=array.array("i",[0 for i in range(Nb_process)])

    LONGEUR_COURSE = 100
    effacer_ecran()
    curseur_invisible()

    for i in range(Nb_process):  # Lancer     Nb_process  processus
        mes_process[i] = Process(target=un_cheval, args= (i,L,cheval,ligne,position,))
        mes_process[i].start()

    move_to(Nb_process+10, 1)
    print("tous lances")

    P_arbitre=Process(target=arbitre, args=(cheval,ligne,position,))

    P_arbitre.start()



    for i in range(Nb_process): mes_process[i].join()

    move_to(24, 1)
    curseur_visible()

    P_arbitre.join()
    print("Fini")

