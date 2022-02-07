#Silia TAIDER mar. 01/06

from math import trunc
import multiprocessing as mp
from multiprocessing import *
import time, random
from ctypes import * 

def controleur(semT, semP, T, P, go_chauffage, go_pompe):
    #print("Je suis la tâche controleur")

    

    while True:

        semT.acquire()
        semP.acquire()
        
        temp=T.value
        press=P.value

        if temp>Seuil_T:
            go_chauffage = False

        else:
            go_chauffage = True

        if press>Seuil_P:
            go_pompe = False

        else:
            go_pompe = True

        time.sleep(1)
        
        semT.release()
        semP.release()
    

def chauffage(semT, T, go_chauffage):
    #print("Je suis la tâche chauffage")

    while True:
        #semT.acquire()

        if go_chauffage :
            T.value  += chauffage_plus
            #print("La temperature a augmente: ", T.value)
        else:
            T.value -= chauffage_moins
            #print("La temperature baisse: ", T.value)

        time.sleep(1)

        #semT.release()

    
def capteur_temperature(semT,T):
    #print("Je suis la tâche temperature")

    while True:
        #semT.acquire()

        val=random.randint(1,2)
        if val==1:
            T.value+=delta_T_plus
        else:
            T.value-=delta_T_moins

        semT.release()

        #time.sleep(1)

    
def capteur_pression(semP, P):
    #print("Je suis la tâche pression")

    while True:
        #semP.acquire()

        val=random.randint(1,2)
        if val==1:
            P.value+=delta_P_plus
        else:
            P.value-=delta_P_moins

        time.sleep(1)

        #semP.release()
    
def pompe(semP, P, go_pompe):
    #print("Je suis la tâche pompe")

    while True:
        #semP.acquire()

        if go_pompe :
            P.value  += 0.2
            #print("La pression a augmente: ", P.value)
        else:
            P.value -= 0.1
            #print("La pression baisse: ", P.value)

        time.sleep(1)

        #semP.release()
    
def ecran(semT, semP):
    #print("Je suis la tâche ecran")
    while True: 

        semT.acquire()
        semP.acquire()

        print("Temperature actuelle: ", T.value)
        print("Pression actuelle: ", P.value)

        time.sleep(1)

        semT.release()
        semP.release()



if __name__ == '__main__':
    semT = mp.Semaphore(1)
    semP = mp.Semaphore(1)
    Seuil_T = 22
    Seuil_P = 117
    go_pompe=False
    go_chauffage=False
    mem_r = mp.Value('f',0, lock=False)
    mem_t = mp.Value('f',18.0, lock=False)
    mem_p = mp.Value('f',10.0, lock=False)
    R = mp.Value('f',0, lock=False)
    T = mp.Value('f',18.0, lock=False)
    P = mp.Value('f',100.0, lock=False)
    delta_T_plus=0.2
    delta_T_moins=0.1
    delta_P_plus=0.2
    delta_P_moins=0.1
    chauffage_plus=1
    chauffage_moins=1
    pompe_plus=1
    pompe_moins=1

    P1=Process(target=controleur,args=(semT, semP, T, P, go_chauffage, go_pompe,))
    P2=Process(target=chauffage,args=(semT, T, go_chauffage,))
    P3=Process(target=capteur_temperature,args=(semT, T,))
    P4=Process(target=capteur_pression,args=(semP, P,))
    P5=Process(target=pompe,args=(semP, P, go_pompe,))
    P6=Process(target=ecran,args=(semT, semP,))


    P1.start()
    P2.start()
    P3.start()
    P4.start()
    P5.start()
    P6.start()

    P1.join()
    P2.join()
    P3.join()
    P4.join()
    P5.join()
    P6.join()

