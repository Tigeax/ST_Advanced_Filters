"""
Hanze University of Applied Sciences
Electrical and Electronic Engineering - Major Sensor Technolgyy
Advanced Filters
Assignment #4 - Quaternions
By Jesse Braaksma
14/05/2021
"""

import csv
import numpy as np
from numpy import sin, cos



def to_unit_vector(v):
    ''' Convert a vector v to a unit vector '''

    mag = np.linalg.norm(v) # Vector magnitude
    unitVector = v / mag # Defide all components of the vector by it's magnitude
    
    return unitVector



def rotate_point_around_vector(p, U, angle):
    ''' Rotate a point in a 3d space by the angle about vector U '''

    # Convert point to a quaternion
    px, py, pz = p
    t = Quaternion(0.0, px, py, pz)

    # Convert the vector to a unit vector
    U = to_unit_vector(U)

    # Create the rotation quaternion from the vector to rotate about and the angle
    x, y, z = U

    qw = cos(angle/2)
    qx = x * sin(angle/2)
    qy = y * sin(angle/2)
    qz = z * sin(angle/2)

    q = Quaternion(qw, qx, qy, qz)

    # Preform the rotation
    qhat = q * t * q.conj

    # Convert back to a 3D point
    phat = qhat.to_vector()

    return phat



class Quaternion:
    ''' Custom class to represent a Quaternion '''

    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z


    def __str__(self):
        return f"({self.w}, {self.x}, {self.y}, {self.z})"


    def __iter__(self):
        return iter((self.w, self.x, self.y, self.z))


    @property
    def conj(self):
        ''' Return a new Quaternion with it's values as the conjugate of this quaternion '''
        return Quaternion(self.w, -self.x, -self.y, -self.z)


    def to_vector(self):
        "Parse the quaternion as a vector and return it as a tulpe of 3 values (x, y, z). This assumes that the Quaternion is a pure Quaternion"
        return (self.x, self.y, self.z)


    def __mul__(self, q2):
        ''' Multiply a Quaternion with a Quaternion (this is called when the * operator is used) '''

        # If the multiplication is not with an Quaternion then raise an error
        if not isinstance(q2, Quaternion):
            raise NotImplemented

        w1, x1, y1, z1 = self
        w2, x2, y2, z2 = q2

        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
        z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2

        return Quaternion(w, x, y, z) # return a new Quaternion with the values of the result of the multiplication





with open('4-quaternions/data.csv', 'r') as csvFile:
    data = csv.DictReader(csvFile)

    for row in data:
        px = float(row['px'])
        py = float(row['py'])
        pz = float(row['pz'])
        p = (px, py, pz)

        Ux = float(row['Ux'])
        Uy = float(row['Uy'])
        Uz = float(row['Uz'])
        U = (Ux, Uy, Uz)

        angle = int(row['a'])

        resultVector = rotate_point_around_vector(p, U, angle)
        roundedResult = (round(resultVector[0], 3), round(resultVector[1], 3), round(resultVector[2], 3))


        print(f"p={p} | U={U} | a={angle} | result={roundedResult}")

