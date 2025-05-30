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


ax1.scatter(myquad.xpoints,myquad.ypoints, myquad.zpoints, s= size_list, c = "#e6737b")

#circle = plt.Circle((0,0), 1, color='blue', alpha = 0.2)
#ax1.add_patch(circle)
# Make data

ax1.scatter(myquad.zpoints, [0 for i in range(len(myquad.xpoints))], [0 for i in range(len(myquad.xpoints))], color = "#751948")
xs = np.arange(-1.2,1.2, step=0.1)
ax1.plot(xs, [0 for i in range(len(xs))], linestyle = ':', color = 'black')


u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

# Plot the surface
ax1.plot_surface(x, y, z, alpha = 0.2, color = "#f7b679")
ax1.legend(['quadrature points','x points', 'x-axis'])
#ax1.set_xticks([])
#ax1.set_yticks([])
#ax1.set_zticks([])
#ax1.set_axis_off()
ax1.set_xticklabels([])
ax1.set_yticklabels([])
ax1.set_zticklabels([])

plt.show()


sum = 0
for weight in myquad.weights:
    sum += weight
    

print("Sum of weights: ", sum)
#plt.savefig("1.png",dpi = 400)


