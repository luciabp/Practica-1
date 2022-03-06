
import random
from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import Array


NPROD = 5
NCONS = 1
K = 2
N = 3

#Nos devuelve el elemento mas pequeño y quien lo ha producido
def lower(lista):
    minimo = lista[0]
    indice = 0

    auxiliar = [lista[K*i] for i in range(NPROD)]

    for i in range(0,len(auxiliar)):
        if auxiliar[i]!=-1:
            minimo = auxiliar[i]
            indice = i
            break
        
    for i in range(0,len(auxiliar)):
        if(auxiliar[i]<minimo and auxiliar[i]!=-1):
            minimo = auxiliar[i]
            indice = i
    return(minimo,indice)
    
    
# Esta funcion sirve para cuando todo es -1 en el buffer entonces se deja de consumir
def comprobar_menos_uno(buffer):

        return [buffer[i] for i in range(0,len(buffer))]!=[-1]*((NPROD*K))


def add_data(buffer, mutex, cuantos_elementos, pid, data):
    mutex.acquire() 
    try:
        buffer[K*pid + cuantos_elementos[pid]] = data
        cuantos_elementos[pid]+=1
        print('add', list(buffer))
    finally:
        mutex.release() 


def get_data(buffer, mutex, cuantos_elementos, numeros):
    
    mutex.acquire()
    try:
        data, pid = lower(buffer)
        numeros.append(data)
        for i in range(cuantos_elementos[pid] - 1):
            buffer[pid*K + i] = buffer[pid*K + (i+1)]
        cuantos_elementos[pid] -= 1
        
    finally:
        mutex.release() 
    return data, pid



def productor(lista_sem, mutex, buffer, index, cuantos_elementos):
    
     v = 0
     
     for k in range(N):
         v += random.randint(0,5)
         print('Productor:', index, 'Iteracion:', k, 'Valor:', v)
         lista_sem[2*index].acquire() # wait empty
         add_data(buffer, mutex, cuantos_elementos, index, v)
         lista_sem[2*index+1].release() # signal nonEmpty
     
     v = -1
     lista_sem[2*index].acquire() 
     add_data(buffer, mutex, cuantos_elementos, index, v)
     lista_sem[2*index+1].release() 
     


def consumidor(lista_sem, mutex, buffer, cuantos_elementos):  
    
    numeros = []
    for i in range(NPROD):
        lista_sem[2*i+1].acquire() 
        
    while comprobar_menos_uno(buffer):

        data, pid = get_data(buffer, mutex, cuantos_elementos, numeros)

        lista_sem[2*pid].release() # 
        lista_sem[2*pid + 1].acquire() 
        print("Vamos añadiendo a la lista",numeros)
    print('\n')
    print ('Valor final de la lista:', numeros)
    

def main():
     buffer = Array('i', NPROD*K)
     
     cuantos_elementos = Array('i', NPROD)
    
     lista_sem = []
     for i in range(NPROD):
         lista_sem.append(BoundedSemaphore(K))
         lista_sem.append(Semaphore(0)) 
     
     mutex = Lock() 
     
    
     lp = []´
     
     for index in range(NPROD):
         lp.append(Process(target=productor, args=(lista_sem, mutex, buffer, index, cuantos_elementos)))
     lp.append(Process(target=consumidor, args=(lista_sem, mutex, buffer, cuantos_elementos)))    
     
     for p in lp:
         p.start()
     for p in lp:
         p.join()

if __name__ == "__main__":
 main() 