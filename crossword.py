# -*- coding: utf-8 -*-
import numpy as np
import io
import time

#CONSTANTS
H=0                 #Horitzontal
V=1                 #Vertical
#per accedir de manera més clara al array de paraules utilitzarem les següents variables:
X=0         #coord x
Y=1         #coord y
SIZE=2      #mida paraula
DIR=3       #orientacio paraula


class crossWord:
    count = 0
    #llegeix el fitxer que conté el crossword i guarda la informació en una matriu n x m (soluciona lectura de caracters \n, \t)
    def llegirTauler1(self, fileName):
        taulerArray=[]
        a=[]
        text_file = open(fileName, 'r')
        lines = text_file.read().split('\n')
        for index, i in enumerate(lines):
            taulerArray.append(i.split('\t'))
            a.append(i.split('\t'))
            for index2, casella in enumerate(taulerArray[index]):
                if(taulerArray[index][index2] == '#'):
                   taulerArray[index][index2] = int(-1)
                else:
                   taulerArray[index][index2] = int(0)

        if taulerArray[-1] == [0]:
            taulerArray.remove([0])

        tauler = np.asarray(taulerArray, dtype=int)
        a = np.asarray(a, dtype=str)
        return tauler, a

    def llegirTauler(self, fileName):
        taulerArray=self.tauler

        contParaula=1
        for fila,f in enumerate(taulerArray):

            col=0
            mida=0
            colIni= col #primera casella de cada fila

            while(col<taulerArray.shape[1]):                                                #comprovem que no hem arribat al final de la fila
                if(f[col] == -1):                                              #si ens trobem coixinet
                    if(mida > 1):                                               #si la paraula fins ara te mes duna lletra, l'afegim a la llista de paraules creant una nova instancia                                                                                  
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
                            self.colisions[contParaula].append((int(taulerArray[col][fila]), col - colIni, fila - self.paraules[int(taulerArray[col][fila])][Y]))  # Desem a la llista de colisions una tupla amb l'index de la paraula amb qui colisiona, la posició de la paraula en concret i la posicio de l'altre paraula
                            self.colisions[int(taulerArray[col][fila])].append(((contParaula), fila - self.paraules[int(taulerArray[col][fila])][Y], col - colIni))

                        mida+=1                                       # no hi ha coixinet i hem arribat al final de la fila
                        if(mida > 1):                                           # tornem a comprovar si cumpleix amb els requisits de la mida
                            self.paraules=np.append(self.paraules,[[colIni,fila,mida,V]], axis=0)
                            contParaula+=1
                            self.colisions.append([])
                            mida=0
                    else:
                        if (taulerArray[col][fila] == 0):  # Si aquesta casella està buida, hi assignem la paraula actual
                            taulerArray[col][fila] = contParaula
                        elif (mida >= 1) or ((col == 0) and (f[col+1] != -1)) or ((mida < 1) and ((f[col - 1] == -1) and (f[col+1] != -1))):
                            self.colisions[contParaula].append((int(taulerArray[col][fila]), col - colIni, fila - self.paraules[int(taulerArray[col][fila])][Y]))  # Desem a la llista de colisions una tupla amb l'index de la paraula amb qui colisiona i la posició
                            self.colisions[int(taulerArray[col][fila])].append(((contParaula), fila - self.paraules[int(taulerArray[col][fila])][Y], col - colIni))
                        mida += 1                                               # passem a la seguent columna i actualitzem mida

                col += 1




    def llegirDiccionari(self, fileName):
        llista = [linia.rstrip() for linia in io.open(fileName,'r',errors='replace')] # elimina les \n finals a cada paraula
        diccionari={}
        for paraula in llista:                                  # organitzem les paraules per longitud en un diccionari
            if len(paraula) in diccionari:
                diccionari[len(paraula)].append(list(paraula))
            else:
                diccionari[len(paraula)]=[list(paraula)]
        """if(fileName == 'diccionari_A.txt'):
            for i in diccionari:
                diccionari[i] = diccionari[i][::100, :]
        """
        return diccionari




    def checkColisio(self, head, paraula, LVA):
        colisionsCorrectes = 0
        for colisio in self.colisions[head]:
            if LVA is None:
                break
            #colisio[0] es el numero de la paraula amb la que colisiona
            if LVA[colisio[0]] is not None:   #Si hi ha colisio comprovar la lletra de les dues paraules
                lletraParaula1 = paraula[colisio[1]]
                paraula2 = LVA[colisio[0]]
                colisioParaula2 = colisio[2]
                lletraParaula2 = paraula2[colisioParaula2]
                if lletraParaula1 == lletraParaula2:
                    colisionsCorrectes += 1
                else:
                    return False
            else:
                colisionsCorrectes += 1
        if colisionsCorrectes == len(self.colisions[head]):
            return True
        return False



    def backtracking(self, LVA, LVNA):
        if None not in LVA:
            return LVA
        else:
            head = LVNA[0]
            for paraula in self.diccionari[self.paraules[head][SIZE]]:  #iterem només a les paraules del diccionari que tenen la mateixa mida que la variable que volem omplir
                if self.checkColisio(head, paraula, LVA):
                    LVA[head] = paraula
                    resultat = self.backtracking(LVA, LVNA[1:])
                    if LVA is None:
                        pass
                    elif None not in LVA:
                        return resultat

        return None

    def updateDomain(self, head, paraula, D):
        for colisio in self.colisions[head]:
            D[colisio[0]] = D[colisio[0]][D[colisio[0]][:, colisio[2]] == paraula[colisio[1]], :]       #D[k] = D[k][D[k][:, c] == 'A', :]
        return D
            


    def backtrackingFC(self, LVA, LVNA, D):
        if all(v is not None for v in LVA):
            return LVA
        else:
            head = LVNA[0]
            if D[head].size != 0:
                for paraula in D[head]:
                    if self.checkColisio(head, paraula, LVA):
                        LVA[head] = paraula
                        DPrev = D[:]
                        D = self.updateDomain(head, paraula, D)
                        resultat = self.backtrackingFC(LVA, LVNA[1:], D)
                        D=DPrev[:]
                        if LVA is None:
                            pass
                        elif (all(v is not None for v in LVA)):
                            return resultat

        return None

    def generaDomain(self):
        D = []
        D.append(np.zeros((1,1), dtype= str))
        for paraula in self.paraules[1:]:
            D.append(np.asarray(self.diccionari[paraula[SIZE]]))
        return D

    def calcula(self, algorisme):

        b = np.zeros((self.paraules.shape[0], self.paraules.shape[1] + 1), dtype= int)
        b[:, :-1] = self.paraules
        b[:,4] = np.arange(0,self.paraules.shape[0])
        b = np.flip(sorted(b, key=lambda a_entry: a_entry[2]), axis=0)[:-1]

        LVNA = b[:,4]
        D = self.generaDomain()

        lva = [None] * (self.paraules.shape[0])
        lva[0] = "empty"
        if algorisme:
            lva = self.backtracking(lva, LVNA)
        else:
            lva = self.backtrackingFC(lva, LVNA, D)


        for index, paraula in enumerate(lva[1:]):

            if self.paraules[index][DIR]==H:
                x = self.paraules[index+1][X]
                y = self.paraules[index+1][Y]
                for lletra in paraula:
                    self.taulerResultats[x][y] = lletra
                    y+=1
            elif self.paraules[index][DIR]==V:
                x = self.paraules[index+1][X]
                y = self.paraules[index+1][Y]
                for lletra in paraula:
                    self.taulerResultats[x][y] = lletra
                    x+=1
        print("\nSOLUCIÓ GUARDADA EN crossword_Resolt.txt \n")
        np.savetxt('crossword_Resolt.txt', self.taulerResultats, delimiter='\t', fmt='%s') #escriu el resultat a un fitxer



    def __init__(self, dic, tauler):
        self.paraules = np.zeros((1,4), dtype=int)
        self.colisions = [[],[]]
        self.diccionari = self.llegirDiccionari(dic)
        self.tauler, self.taulerResultats = self.llegirTauler1(tauler)
        self.llegirTauler(tauler)



def main():
    solucio = crossWord('diccionari_CB.txt','crossword_CB.txt')

    print("Resolució mitjançant BackTracking (1) o ForwardChecking (0) ?")
    alg = input()
    while (alg != '1') and (alg != '0'):
        print("Tria una opció correcta: ")
        alg=input()
        
    if alg == 1:
        msg = "BackTracking"
    else:
        msg = "ForwardChecking"
    
    start_time = time.time()
    solucio.calcula(alg)
    print(solucio.taulerResultats)
    print("")
    print("Temps transcorregut en segons utilitzant " + msg + ": ")
    print(time.time() - start_time)
    
    
if __name__ == "__main__":
    main()






