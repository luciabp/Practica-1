
import random
from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import Array

NPROD = 4
NCONS = 1
N = 2

def lower(lista):
    
    aux = [0]*len(lista)
    
    maximo = max(lista)
    for i in range(0,len(lista)):
        if lista[i] == -1: #si toma el valor -1 hacemos que no lo devuelva como el mínimo
            aux[i] = maximo + 1
        else:
            aux[i] = lista[i]
            
    minimo = aux[0] 
    index = 0 
    #Buscamos el mas pequeño y que no sea -1 
    for i in range(1, len(aux)):
        if aux[i] < minimo and aux[i] != -1:
            minimo = aux[i]
            index = i
            
    return minimo, index

  
    
def productor(lista, buffer, index):
    
     v = 0
     
     for k in range(N): 
         v += random.randint(0,6)
         print('Productor:', index, 'Iteracion:', k, 'Valor:', v)
         lista[2*index].acquire() 
         buffer[index] = v
         lista[2*index+1].release() 
     
     v = -1
     lista[2*index].acquire() 
     buffer[index] = v
     lista[2*index+1].release() 
     


def consumidor(lista, buffer):  
    
    numeros = []
    
    for i in range(NPROD):
        lista[2*i+1].acquire() 
        
    while list(buffer)!=[-1]*NPROD:
        
        v, index = lower(buffer)
        print('Se introduce:', v, 'Productor', index)
        numeros.append(v)
        print (f"numeros: {numeros}")
        lista[2*index].release() # signal empty
        lista[2*index + 1].acquire() # wait nonEmpty
    
    print ('Valor final de la lista:', numeros)
    
    

def main():
     buffer = Array('i', NPROD)
    
     lista_sem = []
     for i in range(NPROD):
         lista_sem.append(BoundedSemaphore(1))
         lista_sem.append(Semaphore(0)) 
     
     lp = []#lista procesos
     
     for index in range(NPROD):
         lp.append(Process(target=productor, args=(lista_sem, buffer, index)))
     lp.append(Process(target=consumidor, args=(lista_sem, buffer)))    
     
     for p in lp:
         p.start()
     for p in lp:
         p.join()



if __name__ == "__main__":
 main()    
           

        