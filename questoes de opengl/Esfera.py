import math

#Variavel da construcao
raio = 1

def esfera(i,j,N):
    theta = i * 2*math.pi / N
    phi = j * math.pi / N - math.pi / 2
    
    x = raio * math.cos(theta) * math.cos(phi)
    y = raio * math.sin(phi)
    z = raio * math.sin(theta) * math.cos(phi)
    
    return x,y,z