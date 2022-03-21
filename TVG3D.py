from graphics import *
import numpy as np
import math
from time import sleep

""" This program was originally made by James Futhey (james@jamesfuthey.com), also known as kidGodzilla (https://github.com/kidGodzilla) over on Github.
    Changes include translation, scaling, and shearing matrices, along with rotation about an arbitrary axis. The program no longer simulates an object that rotates indefinitely;
    the object now moves and rotates smoothly when transformed (with translation and rotation, respectively). Shearing and scaling do not feature animations.
    This version is made by:
    Daffa Muhammad Romero   20/456363/TK/50493
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
        Rx = np.array([[1, 0, 0, 0],
                        [0, cosa, -sina, 0],
                        [0, sina, cosa, 0],
                        [0, 0, 0, 1]])
        coord = np.array([self.x, self.y, self.z, 1])
        res = Rx @ coord
        return Point3D(res[0], res[1], res[2])
 
    def rotateY(self, angle):
        """ Rotates the point about the Y-axis by the given angle in degrees. """
        rad = np.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        Ry = np.array([[cosa, 0, sina, 0],
                        [0, 1, 0, 0],
                        [-sina, 0, cosa, 0],
                        [0, 0, 0, 1]])
        coord = np.array([self.x, self.y, self.z, 1])
        res = Ry @ coord
        return Point3D(res[0], res[1], res[2])
 
    def rotateZ(self, angle):
        """ Rotates the point about the Z-axis by the given angle in degrees. """
        rad = np.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        Rz = np.array([[cosa, -sina, 0, 0],
                        [sina, cosa, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        coord = np.array([self.x, self.y, self.z, 1])
        res = Rz @ coord
        return Point3D(res[0], res[1], res[2])
    
    def rotateArbitrary(self, pt1, pt2, angle):
        xa = pt2[0] - pt1[0]
        ya = pt2[1] - pt1[1]
        za = pt2[2] - pt1[2]
        za2 = math.sqrt(xa**2 +za**2)
        ang1 = 0
        ang2 = 0
        
        if za != 0:
            ang1 = math.atan(xa/ya)
        else:
            if xa > 0: 
                ang1 = 90
            else:
                ang1 = 270
        
        if za2 != 0:
            ang2 = math.atan(ya/za2)
        else:
            if ya > 0:
                ang2 = 90
            else:
                ang2 = 270
        step1 = self.trans(-pt1[0], -pt1[1], -pt1[2])
        step2 = step1.rotateY(-ang1)
        step3 = step2.rotateX(ang2)
        step4 = step3.rotateZ(angle)
        step5 = step4.rotateX(-ang2)
        step6 = step5.rotateY(ang1)
        res = step6.trans(pt1[0], pt1[1], pt1[2])
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
    faces = [[0,1,2,3],[1,5,6,2],[5,4,7,6],[4,0,3,7],[0,4,5,1],[3,2,6,7]]
    width, height = 1280, 800
    lines = []
    operatedPoints = []
    transformedPoints = []

    if optimus == 0:
        for i in range(len(points)):
            operatedPoints.append(points[i])
    if optimus == 1:
        Tx, Ty, Tz = coords[0], coords[1], coords[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].trans(Tx, Ty, Tz))
            
    elif optimus == 2:
        angleX, angleY, angleZ = coords[0], coords[1], coords[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].rotateX(angleX).rotateY(angleY).rotateZ(angleZ))

    elif optimus == 3:
        Shx, Shy, Shz = coords[0], coords[1], coords[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].shear(Shx, Shy, Shz))

    elif optimus == 4:
        pt1 = [coords[0][0], coords[0][1], coords[0][2]]
        pt2 = [coords[1][0], coords[1][1], coords[1][2]]
        for i in range(len(points)):
            operatedPoints.append(points[i].rotateArbitrary(pt1, pt2, coords[2][0]))

    elif optimus == 5:
        factorX, factorY, factorZ = coords[0], coords[1], coords[2]
        for i in range(len(points)):
            operatedPoints.append(points[i].scale(factorX, factorY, factorZ))
    
    #tidak dilakukan apa apa
    
    #Melakukan proyeksi koordinat yang telah di transformasi pada bidang 2 dimensi
    for i in range(len(operatedPoints)):
        transformedPoints.append(operatedPoints[i].project(640, 400, 500, 20))

    win = GraphWin('Test', width, height)
    win.setBackground(color_rgb(255, 255, 255))

    #Menentukan nilai garis pembentuk balok
    for i in faces:
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y)))
        lines.append(Line(Point(transformedPoints[i[0]].x, transformedPoints[i[0]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
        lines.append(Line(Point(transformedPoints[i[1]].x, transformedPoints[i[1]].y), Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y)))
        lines.append(Line(Point(transformedPoints[i[2]].x, transformedPoints[i[2]].y), Point(transformedPoints[i[3]].x, transformedPoints[i[3]].y)))
    #Menggambar garis pembentuk balok
    for i in lines:
        i.draw(win)

    #Menampilkan titik koordinat di x y z
    for i in range(len(transformedPoints)):
        p = Text(Point(transformedPoints[i].x, transformedPoints[i].y), "{:.2f}, {:.2f}, {:.2f}".format(operatedPoints[i].x, operatedPoints[i].y, operatedPoints[i].z))
        p.setSize(8)
        p.setTextColor('Red')
        p.draw(win) 


    ask = int(input("Do you want to do another operation?\nInput 1 for yes, another to exit (number only).\nInput: "))
    if ask==1:
        op, val = question()
        win.close()
        main(op,val, operatedPoints)
    else:
        sys.exit()  
    win.getMouse()
    win.close()

#Nilai ini bertujuan agar fungsi utama tahu operasi apa yang dilakukan dan besaran nilai transformasinya
points = [Point3D(2,5,2),
            Point3D(4,5,2),
            Point3D(4,3,2),
            Point3D(2,3,2),
            Point3D(4,7,6),
            Point3D(6,7,6),
            Point3D(6,5,6),
            Point3D(4,5,6)
        ]
op, val = frontEnd()
main(op, val, points)