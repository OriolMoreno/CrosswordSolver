# -*- coding: utf-8 -*-
import numpy as np

"""
-------------------------------------
POSSIBLE MILLORA AL LLEGIR DICCIONARI
-------------------------------------

from collections import defaultdict

x = ['foo','bar','help','this','guy']

len_dict = defaultdict(list)

for word in x:
    len_dict[len(word)].append(word)
"""
#CONSTANTS
H=0                 #Horitzontal
V=1                 #Vertical
#per accedir de manera més clara al array de paraules utilitzarem les següents variables:
X=0         #coord x
Y=1         #coord y
SIZE=2      #mida paraula
DIR=3       #orientacio paraula

#Classe per emmagatzemar paraules al tauler (opció 2)
class paraulaTauler:
    def __init__(self, dir, mida, coord, confl = [], paraula=''):
        self.dir = dir
        self.mida = mida
        self.coord = coord
        self.confl = confl
        self.paraula = paraula
    def printParaula(self):
        print(self.dir,self.mida,self.coord,self.confl,self.paraula)

class crossWord:

    """
    OPCIO 1: llista nxm amb valors individuals
    """
    #llegeix el fitxer que conté el crossword i guarda la informació en una matriu n x m (soluciona lectura de caracters \n, \t)
    def llegirTauler1(self, fileName):
        taulerArray=[]
        text_file = open(fileName, 'r')
        lines = text_file.read().split('\n')
        for index, i in enumerate(lines):
            taulerArray.append(i.split('\t'))
            for index2, casella in enumerate(taulerArray[index]):
                if(taulerArray[index][index2] == '#'):
                   taulerArray[index][index2] = int(-1)
                else:
                   taulerArray[index][index2] = int(0) 
        
        
        tauler = np.asarray(taulerArray, dtype=int)
        return tauler

    """
    OPCIO 2: llista de paraules que hi ha al tauler utilitzant la classe paraulaTauler
    """
    def llegirTauler(self, fileName):
        taulerArray=self.tauler
        #tauler=[]
        #files
        contParaula=1
        for fila,f in enumerate(taulerArray):
            #print(taulerArray)
            col=0
            mida=0
            colIni= col #primera casella de cada fila
            
            while(col<taulerArray.shape[1]):                                                #comprovem que no hem arribat al final de la fila
                if(f[col] == -1):                                              #si ens trobem coixinet
                    #if(col+1<taulerArray.shape[1]):                                         #comprovem que el coixinet no sigui la ultima casella
                        if(mida > 1):
                                                                                        #si la paraula fins ara te mes duna lletra, l'afegim a la llista de paraules creant una nova instancia
                            self.paraules=np.append(self.paraules,[[fila,colIni,mida,H]], axis=0)
                            
                            contParaula+=1
                            self.colisions.append([])
                        elif (mida == 1):
                            taulerArray[fila][col-1] = 0
                            
                        colIni=col+1                                   #actualitzem novves coordenades i mida nova paraula
                        mida = 0
                else:
                    if(col+1>=taulerArray.shape[1]):
                        mida+=1                                       #no hi ha coixinet i hem arribat al final de la fila
                        if(mida > 1):                                           #tornem a comprovar si cumpleix amb els requisits de la mida
                            self.paraules=np.append(self.paraules,[[fila,colIni,mida,H]], axis=0)
                            
                            self.colisions.append([])
                            #print('kpasa2',coord)
                            mida=0
                            if(taulerArray[fila][col] == 0):                #Si equesta casella està buida, hi assignem la paraula actual
                                taulerArray[fila][col] = contParaula
                            contParaula+=1
                    else:
                        mida += 1                                               #passem a la seguent columna i actualitzem mida
                        if(taulerArray[fila][col] == 0):                #Si equesta casella està buida, hi assignem la paraula actual
                            taulerArray[fila][col] = contParaula
                col += 1
                
        for fila,f in enumerate(taulerArray.T):
            #print(taulerArray)
            col=0
            mida=0
            colIni=col
             #primera casella de cada fila
            while(col<taulerArray.shape[0]):                                                #comprovem que no hem arribat al final de la fila
                if(f[col] == -1):                                              #si ens trobem coixinet                                        #comprovem que el coixinet no sigui la ultima casella
                    if(mida > 1):
                        self.paraules=np.append(self.paraules,[[colIni,fila,mida,V]], axis=0)
                        contParaula+=1
                        self.colisions.append([])
                    colIni=col+1
                    mida = 0
                else:

                        
                    if(col+1>=taulerArray.shape[0]):

                        if (taulerArray[col][fila] == 0):  # Si aquesta casella està buida, hi assignem la paraula actual
                            taulerArray[col][fila] = contParaula
                        elif (f[col - 1] != -1): # (mida > 1) or ((mida <= 1) and (f[col - 1] == -1)):
                            self.colisions[contParaula].append((int(taulerArray[col][fila]), col - colIni))  # Desem a la llista de colisions una tupla amb l'index de la paraula amb qui colisiona i la posició
                            self.colisions[int(taulerArray[col][fila])].append(((contParaula), fila - self.paraules[int(taulerArray[col][fila])][Y]))
                        #print(self.colisions)

                        mida+=1                                       # no hi ha coixinet i hem arribat al final de la fila
                        if(mida > 1):                                           # tornem a comprovar si cumpleix amb els requisits de la mida
                            self.paraules=np.append(self.paraules,[[colIni,fila,mida,V]], axis=0)
                            contParaula+=1
                            self.colisions.append([])
                            #print('kpasa4',coord)
                            mida=0
                    else:
                        if (taulerArray[col][fila] == 0):  # Si aquesta casella està buida, hi assignem la paraula actual
                            taulerArray[col][fila] = contParaula
                        elif (mida >= 1) or ((col == 0) and (f[col+1] != -1)) or ((mida < 1) and ((f[col - 1] == -1) and (f[col+1] != -1))):
                            self.colisions[contParaula].append((int(taulerArray[col][fila]), col - colIni))  # Desem a la llista de colisions una tupla amb l'index de la paraula amb qui colisiona i la posició

                            self.colisions[int(taulerArray[col][fila])].append(((contParaula), fila - self.paraules[int(taulerArray[col][fila])][Y]))
                        #print(self.colisions)
                        mida += 1                                               # passem a la seguent columna i actualitzem mida

                #print(mida, col)
                col += 1

        #return tauler

    def llegirDiccionari(self, fileName):
        #file = open(fileName,'r')
        #llista = file.readlines()
        llista = [linia.rstrip() for linia in open(fileName,'r')] # elimina les \n finals a cada paraula
        diccionari={}
        for paraula in llista:                                  # organitzem les paraules per longitud en un diccionari
            if len(paraula) in diccionari:
                diccionari[len(paraula)].append(paraula)
            else:
                diccionari[len(paraula)]=[paraula]
        return diccionari

    def printTauler(self):
        for p in self.paraules:
            p.printParaula()


    """
        Per mes endevant
        def arcConsistency(self, rest = [], pAsig = np.zeros((1,1), dtype=object)):
        #LVNA: forats de paraules
        #LVA: paraules oplertes
        
        if pAsig.shape[0] == self.paraules.shape[0]:
            return pAsig
        else:
            for emptyWord in self.paraules:
        
        
        
        
        """

    def checkColisio(self, head, paraula):
        #for colisio in self.colisions[rest]:
            #if colisio[0] == head:
                #if paraula[colisio[1]] == rest[1]:
                    #pass

        return True

    # LVNA = np.arange(1, self.paraules.shape[0])


    def backtracking(self, LVA, LVNA):
        if len(LVA) == self.paraules.shape[0] - 1:
            return LVA
        else:
            head = LVNA[0]
            for conjunt in self.diccionari.values():
                for paraula in conjunt:
                    if len(paraula) == self.paraules[head, SIZE]:
                        if self.checkColisio(head, paraula):
                            LVA.append([head, paraula])
                            LVA = self.backtracking(LVA, LVNA[1:])
                            if len(LVA) == self.paraules.shape[0] - 1:
                                return LVA
                    else:
                        break
        return "Error"
    
        
    def __init__(self, dic, tauler):
        self.paraules = np.zeros((1,4), dtype=int)
        self.colisions = [[],[]]
        self.diccionari = self.llegirDiccionari(dic)
        self.tauler = self.llegirTauler1(tauler)
        self.llegirTauler(tauler)
        




hola = crossWord('diccionari_CB.txt','crossword_CB.txt')
print(hola.diccionari)
#hola.printTauler()

print(hola.paraules)
print(hola.tauler)
print(hola.colisions)

LVNA = np.arange(1, hola.paraules.shape[0])
lva=[]
lva = hola.backtracking(lva, LVNA)      #np.zeros((1,2), dtype = object)
print(lva)


        
        
"""
paraules = np.zeros((2,4), dtype=int)
paraules2 = np.zeros((1,4), dtype=int)
paraules3 = np.zeros((1,4), dtype=int)
paraules = np.append(paraules, paraules2, axis=0)
paraules = np.append(paraules, np.array([[2,3,2,1]]), axis=0)
paraules[:,2]=1
print(paraules)
"""






#print(llegirDiccionari('diccionari_CB.txt'))
#llegirTauler('crossword_CB.txt')