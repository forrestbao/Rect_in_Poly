# Copyright 2021 Forrest Sheng Bao
# MIT license



import matplotlib.patches
import matplotlib.pyplot
import numpy 
import math

#%% 
def generate_panel_arrays(nx, ny, panel_size, offset_x):
    """Generate a rectangular array of nx-by-ny panels of panel_size 
    """
    (dx, dy) = panel_size

    # Assuming offset on x axis only
    Array = [(i*panel_size[0] + offset_x*j%dx, j*panel_size[1]) 
             for i in range(nx)
             for j in range(ny)
    ] # bottom-left of each panel
    return Array 

def plot_rectangle(x, y, dx, dy, color='r', facecolor='none'):
    """Plot a rectangle of size dx by dy and bottom-lefted at (x, y)
    """
    # fig = plt.figure()
    Xs = [x, x,    x+dx, x+dx, x]
    Ys = [y, y+dy, y+dy, y,    y]
    if facecolor == 'none': # i have no clue why facecolor='none' did not work for fill()
        matplotlib.pyplot.plot(Xs, Ys, color)
    else:
        matplotlib.pyplot.fill(Xs, Ys, facecolor=facecolor, edgecolor=color)

def plot_rectangles(Array, panel_size, color='r', facecolor='none'):
    """Plot each rectangles in Array
    """

    (dx, dy) = panel_size
    for (x, y) in Array:
        plot_rectangle(x,y, dx, dy, color=color, facecolor=facecolor)

def plot_polygon(Points):
    """Plot a polygon
    """
    Xs, Ys = zip(*Points)
    matplotlib.pyplot.plot(Xs, Ys, 'b')
    matplotlib.pyplot.plot([Xs[-1], Xs[0]], [Ys[-1], Ys[0]], 'b') # close the loop

def contains_rectangle(x, y, panel_size, polygon):
    """Check whether a rectangle is inside of a polygon
    If all points of it are in, then it is in. 
    """
    (dx, dy) = panel_size
    bbpath = matplotlib.path.Path(polygon) 
    result = bbpath.contains_points([(x,y),(x+dx,y), (x,y+dy), (x+dx,y+dy)])
    return numpy.all(result)

def contains_rectangles(Array, panel_size, polygon):
    """Check whether an array of rectangles are inside of a polygon
    Return those who are in. 
    All rectangles are of the same size. 
    """
    okay_panels  = [(x,y) for (x,y) in Array if contains_rectangle(x,y, panel_size, polygon)]
    return okay_panels

def rotate(x,y, angle):
    """Transform coordinate (x,y) by angle
    angle is in radians not in degrees. 
    """
    new_x = x*math.cos(angle) - y * math.sin(angle)
    new_y = x*math.sin(angle) + y * math.cos(angle)
    return new_x, new_y

def solve(polygon, panel_size, angle_resolution=15):
    """Search for different rotations and offsets to find the solution that maximize the panel number 
    """
    counter = 1 
    max_panel = 0 
    best_polygon, best_panels, best_array, best_angle, best_offset = None, None, None, None, None
    for angle in range(0, 360, angle_resolution):
        for offset_x in range(0, panel_size[0]):

            # rotate the polygon
            rad_angle = angle/180*math.pi
            polygon = numpy.array([rotate(x,y,rad_angle) for (x,y) in polygon])
            # adjust rotated polygon to be positive in both axes
            min_x = polygon[:,0].min()
            min_y = polygon[:,1].min()
            polygon[:,0] -= (min_x -1)
            polygon[:,1] -= (min_y -1)
            max_x = polygon[:,0].max()      
            max_y = polygon[:,1].max()

            # generate the array 
            n_x = int(max_x // panel_size[0] + 1)
            n_y = int(max_y // panel_size[1] + 1)
            Array = generate_panel_arrays(n_x, n_y, panel_size, offset_x)

            okay_panels = contains_rectangles(Array, panel_size, polygon)
            if len(okay_panels) > max_panel : 
                print ("Maximal number of panels is", max_panel)
                print ("When angle is {} and offset is {}".format(best_angle, best_offset))
                max_panel = len(okay_panels)
                best_angle, best_offset = angle, offset_x
                best_polygon =  polygon
                best_panels = okay_panels
                best_array = Array 

            plot_polygon(polygon)
            plot_rectangles(Array, panel_size)
            plot_rectangles(okay_panels, panel_size, color='lime', facecolor='lime')
            matplotlib.pyplot.savefig(str(angle)+"_"+str(offset_x)+'.png')
            matplotlib.pyplot.close()

    print ("Maximal number of panels is", max_panel, end = ";")
    print ("When angle is {} and offset is {}".format(best_angle, best_offset))

    # Visualize best result 
    plot_polygon(best_polygon)
    plot_rectangles(best_array, panel_size)
    plot_rectangles(best_panels, panel_size, color='k', facecolor='lime')

    return max_panel, best_angle, best_offset

#%% 
if __name__ == "__main__":
    panel_size = (3,1)
    offset_x = 1
    Array = generate_panel_arrays(7,10, panel_size, offset_x)

    polygon = [(1,1), (5,3), (10,2), (8,8), (4,6), (2,5)]
    # plot_polygon(polygon)
    # plot_rectangles(Array, panel_size)
    # okay_panels = contains_rectangles(Array, panel_size, polygon)
    # plot_rectangles(okay_panels, panel_size, color='lime', facecolor='lime')


    solve(polygon, panel_size)  
    # plot_rectangle(10,8, 2, 5)

    
# %%

 