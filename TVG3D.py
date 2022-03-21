from graphics import *
import numpy as np
import math
from time import sleep

""" This program was originally made by James Futhey (james@jamesfuthey.com), also known as kidGodzilla (https://github.com/kidGodzilla) over on Github.
    Changes include translation, scaling, and shearing matrices, along with rotation about an arbitrary axis. The program no longer simulates an object that rotates indefinitely;
    the object now moves and rotates smoothly when transformed (with translation and rotation, respectively). Shearing and scaling do not feature animations.
    This version is made by:
    Daffa Muhammad Romero   20/456363/TK/50493 - daffaromero on Github (https://github.com/daffaromero)
    Laili Rofi'ah           20/463604/TK/51596
    Baihaqi                 20/
    Farhan                  20/
    Ruth                    20/
"""

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
 
    def rotateX(self, angle):
        """ Rotates the point about the X-axis by the given angle in degrees. """
        rad = np.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        Rx = np.array([ [1, 0, 0, 0],
                        [0, cosa, -sina, 0],
                        [0, sina, cosa, 0],
                        [0, 0, 0, 1] ])
        coord = np.array([self.x, self.y, self.z, 1])
        res = Rx @ coord
        return Point3D(res[0], res[1], res[2])
 
    def rotateY(self, angle):
        """ Rotates the point about the Y-axis by the given angle in degrees. """
        rad = np.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        Ry = np.array([ [cosa, 0, sina, 0],
                        [0, 1, 0, 0],
                        [-sina, 0, cosa, 0],
                        [0, 0, 0, 1] ])
        coord = np.array([self.x, self.y, self.z, 1])
        res = Ry @ coord
        return Point3D(res[0], res[1], res[2])
 
    def rotateZ(self, angle):
        """ Rotates the point about the Z-axis by the given angle in degrees. """
        rad = np.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        Rz = np.array([ [cosa, -sina, 0, 0],
                        [sina, cosa, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1] ])
        coord = np.array([self.x, self.y, self.z, 1])
        res = Rz @ coord
        return Point3D(res[0], res[1], res[2])
    
    def rotateArbitrary(self, pt1, pt2, angle):
        xVect = pt2[0] - pt1[0]
        yVect = pt2[1] - pt1[1]
        zVect = pt2[2] - pt1[2]
        beta, miu = 0,0
        if zVect == 0:
            if xVect > 0: 
                beta = 90
            else:
                beta = 270
        else:
            beta = math.atan(xVect/ zVect) * 180 / math.pi
        if xVect **2 + zVect**2 == 0:
            if yVect > 0:
                miu = 90
            else:
                miu = 270
        else:
            miu = math.atan (yVect / math.sqrt(xVect **2 + zVect**2)) * 180 / math.pi
        step1 = self.trans(0 - pt1[0], 0 - pt1[1], 0 - pt1[2])
        step2 = step1.rotateY(-beta)
        step3 = step2.rotateX(miu)
        step4 = step3.rotateZ(angle)
        step5 = step4.rotateX(-miu)
        step6 = step5.rotateY(beta)
        res = step6.trans(pt1[0] - 0, pt1[1] - 0, pt1[2] - 0)

        return res
    
    def trans(self, x, y, z):
        """ Moves the point by a given amount in the Cartesian plane. """
        T = np.array([[1, 0, 0, x],
                        [0, 1, 0, y],
                        [0, 0, 1, z],
                        [0, 0, 0, 1]])
        coord = np.array([self.x, self.y, self.z, 1])
        res = T @ coord
        return Point3D(res[0], res[1], res[2])
    
    def scale(self, x, y, z):
        """ Scales an object by given scale factors. """
        S = np.array([[x, 0, 0, 0],
                        [0, y, 0, 0],
                        [0, 0, z, 0],
                        [0, 0, 0, 1]])
        coord = np.array([self.x, self.y, self.z, 1])
        res = S @ coord
        return Point3D(res[0], res[1], res[2])
    
    def shear(self, Shx, Shy, Shz):
        """ Displaces a point in a given direction. Skews the object. """
        Shxy = np.array([[1, 0, Shx, 0],
                         [0, 1, Shy, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
        Shyz = np.array([[1, 0, 0, 0],
                         [0, Shy, 0, 0],
                         [0, Shz, 1, 0],
                         [0, 0, 0, 1]])
        Shxz = np.array([[Shx, 0, 0, 0],
                         [0, 1, 0, 0],
                         [Shz, 0, 1, 0],
                         [0, 0, 0, 1]])
        coord = np.array([self.x, self.y, self.z, 1])
        res = [0]*4
        if Shz == 0:
            res = Shxy @ coord
        elif Shx == 0:
            res = Shyz @ coord
        elif Shy == 0:
            res = Shxz @ coord
        return Point3D(res[0], res[1], res[2])        
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)

def frontEnd():
    coords = []
    optimus = int(input("""
Choose your desired transformation.
        
    0. View object
    1. Translation
    2. Scaling
    3. Rotation about x, y, or z axis
    4. Rotation about arbitrary axis
    5. Shear
        
Input a number (0-5): """))
    
    if optimus == 0:
        coords = [0]
    
    elif optimus == 1:
        Tx = int(input("Translate by x amount: "))
        Ty = int(input("Translate by y amount: "))
        Tz = int(input("Translate by z amount: "))
        coords = [Tx, Ty, Tz]
        
    elif optimus == 2:
        Sx = float(input("Scale factor (X): "))
        Sy = float(input("Scale factor (Y): "))
        Sz = float(input("Scale factor (X): "))
        coords = [Sx, Sy, Sz]

    elif optimus == 3:
        Rx = float(input("Degrees of rotation about x-axis: "))
        Ry = float(input("Degrees of rotation about y-axis: "))
        Rz = float(input("Degrees of rotation about z-axis: "))
        coords = [Rx, Ry, Rz]
        
    elif optimus == 4:
        xo = int(input("X (1st point): "))
        yo = int(input("Y (1st point): "))
        zo = int(input("Z (1st point): "))
        print("")
        xp = int(input("X (2nd point): "))
        yp = int(input("Y (2nd point): "))
        zp = int(input("Z (2nd point): "))
        angle = int(input("Degrees of rotation: "))
        coords = [[int(xo), int(yo), int(zo)], [int(xp), int(yp), int(zp)], [angle,0,0]] 

    elif optimus == 5:
        Shx = float(input("Shear parallel to x-axis: "))
        Shy = float(input("Shear parallel to y-axis: "))
        Shz = float(input("Shear parallel to z-axis: "))
        if(Shx == 0 and Shy == 0 and Shz == 0):
            coords = [0]
        if(Shx != 0 and Shy != 0 and Shz != 0):
            print("Invalid input. Shearing in 3D space takes parameters from two axes (a plane).")
            quit()
        coords = [Shx, Shy, Shz]
    
    return optimus, coords

def main(optimus, coords, points):
    p = 0
    width, height = 1280, 800
    
    #Connecting lines to form a wireframe model of object.
    faces = [[0,1,2,3],[1,5,6,2],[5,4,7,6],[4,0,3,7],[0,4,5,1],[3,2,6,7]]
    
    #Arrays to hold graphics.py primitives.
    edges = []
    vertices = []
    tr_vertices = []

    if optimus == 0:
        for i in range(len(points)):
            vertices.append(points[i])
            
    if optimus == 1:
        Tx = coords[0]
        Ty = coords[1]
        Tz = coords[2]
        for i in range(len(points)):
            vertices.append(points[i].trans(Tx, Ty, Tz))
            
    elif optimus == 2:
        factorX = coords[0]
        factorY = coords[1]
        factorZ = coords[2]
        for i in range(len(points)):
            vertices.append(points[i].scale(factorX, factorY, factorZ))
            
    elif optimus == 3:
        angleX = coords[0]
        angleY = coords[1]
        angleZ = coords[2]
        for i in range(len(points)):
            vertices.append(points[i].rotateX(angleX).rotateY(angleY).rotateZ(angleZ))

    elif optimus == 4:
        pt1 = [coords[0][0], coords[0][1], coords[0][2]]
        pt2 = [coords[1][0], coords[1][1], coords[1][2]]
        for i in range(len(points)):
            vertices.append(points[i].rotateArbitrary(pt1, pt2, coords[2][0]))

    elif optimus == 5:
        Shx = coords[0]
        Shy = coords[1]
        Shz = coords[2]
        for i in range(len(points)):
            vertices.append(points[i].shear(Shx, Shy, Shz))

    for i in range(len(vertices)):
        tr_vertices.append(vertices[i].project(640, 400, 500, 20))

    #Creating a graphics.py window
    win = GraphWin('Object', width, height)
    win.setBackground(color_rgb(255, 255, 255))

    for i in faces:
        edges.append(Line(Point(tr_vertices[i[0]].x, tr_vertices[i[0]].y), Point(tr_vertices[i[1]].x, tr_vertices[i[1]].y)))
        edges.append(Line(Point(tr_vertices[i[0]].x, tr_vertices[i[0]].y), Point(tr_vertices[i[3]].x, tr_vertices[i[3]].y)))
        edges.append(Line(Point(tr_vertices[i[1]].x, tr_vertices[i[1]].y), Point(tr_vertices[i[2]].x, tr_vertices[i[2]].y)))
        edges.append(Line(Point(tr_vertices[i[2]].x, tr_vertices[i[2]].y), Point(tr_vertices[i[3]].x, tr_vertices[i[3]].y)))

    for i in edges:
        i.draw(win)

    repeat = int(input("Transform again?\nType 1 for YES | Type 0 for NO.\nInput: "))
    if repeat == 1:
        op, val = frontEnd()
        win.close()
        main(op, val, vertices)
    elif repeat == 0:
        quit()
    else:
        quit()
        
    win.getMouse()
    win.close()

points = [Point3D(2,3,2),
          Point3D(4,3,2),
          Point3D(4,5,2),
          Point3D(2,5,2),
          Point3D(4,5,6),
          Point3D(6,5,6),
          Point3D(6,7,6),
          Point3D(4,7,6)]
op, val = frontEnd()
main(op, val, points)