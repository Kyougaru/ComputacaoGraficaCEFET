from GLAPP import GLAPP
from OpenGL import GL
from array import array
import ctypes
import glm
import math

def solido():

    v = array('f',[])
    t = array('f',[])
    n = array('f',[])
    
    def esfera(i,j):
        theta = i * 2*math.pi / N
        phi = j * math.pi / N - math.pi / 2
        
        x = raio * math.cos(theta) * math.cos(phi)
        y = raio * math.sin(phi)
        z = raio * math.sin(theta) * math.cos(phi)
        
        return x,y,z

    def ft(i,j):
        return i/N, j/N

    def normal(v,i,j):
        parc1 = esfera(i,j+0.1)
        parc2 = esfera(i+0.1,j)
        v1 = glm.vec3(parc1[0]-v[0],parc1[1]-v[1],parc1[2]-v[2])
        v2 = glm.vec3(parc2[0]-v[0],parc2[1]-v[1],parc2[2]-v[2])
        n = glm.normalize(glm.cross(v1,v2))
        return n.x, n.y, n.z

    def adiciona(lista,vertice):
        for v in vertice:
            lista.append(v)

    for i in range(N):
        for j in range(N):
            vA = esfera(i,j)
            tA = ft(i,j)
            nA = normal(vA,i,j)
            vB = esfera(i,j+1)
            tB = ft(i,j+1)
            nB = normal(vB,i,j+1)
            vC = esfera(i+1,j+1)
            tC = ft(i+1,j+1)
            nC = normal(vC,i+1,j+1)
            vD = esfera(i+1,j)
            tD = ft(i+1,j)
            nD = normal(vD,i+1,j)
            adiciona(v,vA)
            adiciona(t,tA)
            adiciona(n,nA)
            adiciona(v,vB)
            adiciona(t,tB)
            adiciona(n,nB)
            adiciona(v,vD)
            adiciona(t,tD)
            adiciona(n,nB)
            adiciona(v,vB)
            adiciona(t,tB)
            adiciona(n,nB)
            adiciona(v,vC)
            adiciona(t,tC)
            adiciona(n,nC)
            adiciona(v,vD)
            adiciona(t,tD)
            adiciona(n,nD)
    return v, t, n

#Variaveis da construcao
N = 50
raio = 1
a = 0

v, t, n = solido()

class EsferaTexturizada(GLAPP):

    def setup(self):
        # Window setup
        self.title("Esfera")
        self.size(800,800)

        # OpenGL Initialization
        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        # Pipeline (shaders)
        self.pipeline = self.loadPipeline("SimpleTexture")
        GL.glUseProgram(self.pipeline)
        GL.glBindAttribLocation(self.pipeline,0,"position")
        GL.glBindAttribLocation(self.pipeline,1,"textureCoord")
        GL.glBindAttribLocation(self.pipeline,2,"normal")
        
        # Texture
        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.loadTexture("./textures/mapa.png")
        GL.glUniform1i(GL.glGetUniformLocation(self.pipeline, "textureSlot"),0)

        self.squareArrayBufferId = None

    def drawSolid(self):

        if self.squareArrayBufferId == None:
            position = v
            textureCoord = t
            normal = n
            self.squareArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.squareArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            GL.glEnableVertexAttribArray(2)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idTextureBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idTextureBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(textureCoord)*textureCoord.itemsize, ctypes.c_void_p(textureCoord.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,2,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(normal)*normal.itemsize, ctypes.c_void_p(normal.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(2,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

        global a
        a += 0.01
        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(glm.vec3(0,0,6),glm.vec3(0,0,0),glm.vec3(0,1,0))
        model = glm.rotate(a,glm.vec3(0,1,0))
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        GL.glBindVertexArray(self.squareArrayBufferId)
        GL.glDrawArrays(GL.GL_TRIANGLES,0,len(v)//3)

    def draw(self):
        # clear screen and depth buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

        # Desenha o solido
        self.drawSolid()

EsferaTexturizada()
