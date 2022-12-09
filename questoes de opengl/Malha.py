#Variavel da construcao
coordsIniciais = -1
coordsFinais = 1

def circular(i,j,N):
    x,y = malha(i,j,N)
    return x,y,x**2+y**2
    
def hiperbolico(i,j,N):
    x,y = malha(i,j,N)
    return x,y,x**2-y**2

def malha(i,j,N):
    d = (coordsFinais - coordsIniciais)/N
    x = coordsIniciais + i * d
    y = coordsIniciais + j * d
    return x,y