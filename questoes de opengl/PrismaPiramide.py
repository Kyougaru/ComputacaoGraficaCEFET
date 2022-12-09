from GLAPP import GLAPP
from OpenGL import GL
from array import array
from optparse import OptionParser
import ctypes
import glm
import math

#Variaveis da figura
a = 0
vertices = 3
raio = 1
altura = 2
modificador = 1

#Opcoes de figura
parser = OptionParser()
parser.add_option('-p', action="store_true", dest='prisma')
parser.add_option('-x', action="store_true", dest='piramide')
(options, args) = parser.parse_args()
if options.prisma:
    modificador = 1
elif options.piramide:
    modificador = 0
else:
    raise Exception("Utilize -p para prisma ou -x para piramide")

class TriangleApp(GLAPP):

    def setup(self):
        # Window setup
        self.title("Prisma e Piramide")
        self.size(800,800)

        # OpenGL Initialization
        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        # Pipeline (shaders)
        self.pipeline = self.loadPipeline("SimplePipeline")
        GL.glUseProgram(self.pipeline)

        self.triangleArrayBufferId = None

    def drawTriangle(self):
        pontosXY = []
        position = array('f',[])
        color = array('f',[])
        angulo = (2*math.pi)/vertices
        
        if self.triangleArrayBufferId == None:
            #Fundo
            for i in range(vertices):
                x = raio * math.cos(i*angulo)
                y = raio * math.sin(i*angulo)
                
                pontosXY += [(x,y)]
                
                position.append(x)
                position.append(y)
                position.append(0)
            
            #Topo
            for x,y in pontosXY:
                position.append(modificador*x)
                position.append(modificador*y)
                position.append(altura)
            
            #Lados
            for i in range(vertices):
                position.append(pontosXY[i][0])
                position.append(pontosXY[i][1])
                position.append(0)
                
                position.append(modificador*pontosXY[i][0])
                position.append(modificador*pontosXY[i][1])
                position.append(altura)
                
                position.append(modificador*pontosXY[(i+1)%vertices][0])
                position.append(modificador*pontosXY[(i+1)%vertices][1])
                position.append(altura)
                
                position.append(pontosXY[(i+1)%vertices][0])
                position.append(pontosXY[(i+1)%vertices][1])
                position.append(0)
                
                position.append(modificador*pontosXY[(i+1)%vertices][0])
                position.append(modificador*pontosXY[(i+1)%vertices][1])
                position.append(altura)
                
                position.append(pontosXY[i][0])
                position.append(pontosXY[i][1])
                position.append(0)
                
            #Deixa tudo azul
            for i in range(len(position)):
                color.append(0.0)
                color.append(0.0)
                color.append(1.0)

            self.triangleArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.triangleArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idColorBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idColorBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(color)*color.itemsize, ctypes.c_void_p(color.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        
        global a
        a += 0.01
        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(glm.vec3(0,0,6),glm.vec3(0,0,0),glm.vec3(0,1,0))
        model = glm.rotate(a,glm.vec3(0,2,0))
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        GL.glBindVertexArray(self.triangleArrayBufferId)
        GL.glDrawArrays(GL.GL_TRIANGLES,0,24)

    def draw(self):
        # clear screen and depth buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

        # Draw a Triangle
        self.drawTriangle()

TriangleApp()