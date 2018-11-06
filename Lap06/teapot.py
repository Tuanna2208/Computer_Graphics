from math import *

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print ("OpenGL wrapper for python not found")

last_time = 0


def load():
    vertices =[]
    faces = []
    with open("teapot.obj") as f:
        for line in f.readlines():
            x = list(map(lambda x:x.strip(), line.strip().split()))
            if len(x)<2:
                continue
            if x[0]=="v":
                vertices.append(tuple(map(float,x[1:])))
            else:
                faces.append(tuple(map(int,x[1:])))
    return vertices,faces
    


class Teapot:

    def __init__(self, radius,vertices,faces):

        self.radius = radius

        self.lats = 100

        self.longs = 100
        self.rotate = 0
        self.user_theta = 90
        self.user_height = -10

        self.direction = [0.0, 2.0, -1.0, 1.0]

        self.intensity = [0.7, 0.7, 0.7, 1.0]

        self.ambient_intensity = [0.3, 0.3, 0.3, 1.0]

        self.surface = GL_SMOOTH
        self.vertices = vertices
        self.faces = faces

    def init(self):

        glClearColor(0.0, 0.0, 0.0, 0.0)

        self.compute_location()

        glEnable(GL_DEPTH_TEST)

        glEnable(GL_LIGHTING)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient_intensity)

        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_POSITION, self.direction)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.intensity)

        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    def compute_location(self):
        x = 2 * cos(self.user_theta)
        y = 2 * sin(self.user_theta)
        z = self.user_height
        d = sqrt(x * x + y * y + z * z)
        
        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()
        glFrustum(-d * 0.5, d * 0.5, -d * 0.5, d * 0.5, d - 4.0, d + 4.0)

        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor3f(1.0, 1.0, 1.0)

        glShadeModel(self.surface)
        self.draw()
        glutSwapBuffers()

    def draw(self):
        self.rotate+=2.0
        glPushMatrix()
        glRotatef(self.rotate,1,1,1)
        for f in self.faces:
            glBegin(GL_POLYGON)
            for v in f:
                glVertex3f(*self.vertices[v-1])
            glEnd()
        glPopMatrix()

    def special(self, key, x, y):

        if key == GLUT_KEY_UP:
            self.user_height += 0.2
        if key == GLUT_KEY_DOWN:
            self.user_height -= 0.2

        if key == GLUT_KEY_LEFT:
            self.user_theta += 0.1
        if key == GLUT_KEY_RIGHT:
            self.user_theta -= 0.1

        if key == GLUT_KEY_F1:
            if self.surface == GL_FLAT:
                self.surface = GL_SMOOTH
            else:
                self.surface = GL_FLAT

        self.compute_location()
        glutPostRedisplay()

    def mouse(self,button,state,x,y):

        if button==4:
            self.user_height += 0.2
        elif button==3:
            self.user_height -= 0.2
        elif button==0:
            if state==0:
                self.user_theta += 0.05
        self.compute_location()
        glutPostRedisplay()
        
    def idle(self):
        global last_time
        time = glutGet(GLUT_ELAPSED_TIME)

        if last_time == 0 or time >= last_time + 40:
            last_time = time
            glutPostRedisplay()

    def visible(self, vis):
        if vis == GLUT_VISIBLE:
            glutIdleFunc(self.idle)
        else:
            glutIdleFunc(None)


def main():

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowSize(640, 480)
    glutInitWindowPosition(50, 100)

    glutCreateWindow('Teapot')

    vertices,faces = load()
    s = Teapot(5.0,vertices,faces)

    s.init()

    glutDisplayFunc(s.display)
    glutMouseFunc(s.mouse)  
    
    glutVisibilityFunc(s.visible)

    glutSpecialFunc(s.special)
    
    glutMainLoop()


if __name__ == '__main__':
    main()