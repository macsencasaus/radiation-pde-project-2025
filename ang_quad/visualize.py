from matplotlib import pyplot as plt
import numpy as np

class quad:
    def __init__(self, weights = [], points = []):
        
        self.weights = weights
        self.points = points
        self.xpoints = points
        self.ypoints = points
        self.zpoints = points


def extract_data(filename, quad):
    file = open(filename, "r")
    lines = file.readlines()
    
    quad.weights = []
    quad.points = []
    quad.xpoints = []
    quad.ypoints = []
    quad.zpoints = []
    
    weight_flag = False
    point_flag = False
    
    for line in lines:
        if(weight_flag and line != "\n"):
            quad.weights.append(float(line.removesuffix('\n')))
        
        if(point_flag and line != "\n"):
            x =float(line.split()[0])
            y =float(line.split()[1])
            z =  float(line.split()[2].removesuffix("\n") )
            point = [x,y,z]
            quad.points.append(point)
            quad.xpoints.append(x)
            quad.ypoints.append(y)
            quad.zpoints.append(z)
        
        if line == "\n":
            weight_flag = False
            point_flag = False
            
        if "Weight" in line:
            weight_flag = True
            point_flag = False
        
        if "Angles" in line:
            point_flag = True
            weight_flag = False



myquad = quad()


N = input("Enter Quad Number (N) : ")

extract_data("S_"+N, myquad)


max_weight = np.amax(myquad.weights)

size_list =[20*weight/max_weight for weight in myquad.weights]

fig = plt.figure()
ax1 = fig.add_subplot(projection='3d')
ax1.set_aspect('equal')

plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 14


ax1.scatter(myquad.xpoints,myquad.ypoints, myquad.zpoints, s= size_list, c = 'r')

#circle = plt.Circle((0,0), 1, color='blue', alpha = 0.2)
#ax1.add_patch(circle)
plt.show()

sum = 0
for weight in myquad.weights:
    sum += weight
    

print("Sum of weights: ", sum)
#plt.savefig("1.png",dpi = 400)

