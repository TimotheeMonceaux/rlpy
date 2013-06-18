######################################################
# Developed by Alborz Geramiard Oct 26th 2012 at MIT #
######################################################

from __future__ import division # This will cause "/" to always return float!
from operator import *
from numpy  import *
#import matplotlib
#matplotlib.use("WXAgg") # do this before pylab so you don'tget the default back end. < Maybe faster but I dont have the package yet
from matplotlib import pylab as pl
from matplotlib import mpl
from matplotlib import rc
import matplotlib.colors as col
import matplotlib.cm as cm
from scipy import stats
from scipy import misc
from time import *
from hashlib import sha1
import datetime
# Tips:
# array.astype(float) => convert elements
# matlibplot initializes the maping from the values to 
# colors on the first time creating unless bounds are set manually. 
# Hence you may update color values later but dont see any updates!  
# in specifying dimensions for reshape you can put -1 so it will be automatically infered
# [2,2,2] = [2]*3
# [1,2,2,1,2,2,1,2,2] = ([1]+[2]*2)*3
# [[1,2],[1,2],[1,2]] = array([[1,2],]*3)
# apply function foo to all elements of array A: vectorize(foo)(A) (The operation may be unstable! Care!
# Set a property of a class:  vars(self)['prop'] = 2

def prod(x):
    #Returns the multiplications of the elements of a set
    return reduce(mul,x)
def randSet(x):
    #Returns a random element of a list uniformly.
    i = random.random_integers(0,size(x)-1)
    return x[i]
def closestDiscretization(x, buckets, limits):
    #Return the closest point to x based on the discretization defined by the number of buckets and limits
    width = limits[1]-limits[0]
    return round(float(x-limits[0])*buckets/width) / buckets * width + limits[0]
def deltaT(start_time):
    return time()-start_time
def hhmmss(t):
    #Return a string of hhmmss
    return str(datetime.timedelta(seconds=round(t)))
def className(obj):
    # return the name of a class
    return obj.__class__.__name__
def scale(x,m,M):
    # given an array return the scaled version of the array.
    # positive numbers are scaled [0,M] -> [0,1]
    # negative numbers are scaled [m,0] -> [-1,0]
    pos_ind = where(x>0)
    #x(pos_ind) = x(pos_ind)
def createColorMaps():
    #Make Grid World ColorMap
    mycmap = col.ListedColormap(['w', '.75','b','g','r','k'], 'GridWorld')
    #Make Blocks World ColorMap
    cm.register_cmap(cmap=mycmap)
    mycmap = col.ListedColormap(['w','b','g','r','m',(1,1,0),'k'], 'BlocksWorld')
    cm.register_cmap(cmap=mycmap)
    mycmap = col.ListedColormap(['.6','k'], 'Actions')
    cm.register_cmap(cmap=mycmap)
    mycmap = make_colormap({0:'r', 1: 'w', 2.:'g'})  # red to blue
    cm.register_cmap(cmap=mycmap,name='ValueFunction')
#    Some useful Colormaps
#    red_yellow_blue = make_colormap({0.:'r', 0.5:'#ffff00', 1.:'b'})
#    blue_yellow_red = make_colormap({0.:'b', 0.5:'#ffff00', 1.:'r'})
#    yellow_red_blue = make_colormap({0.:'#ffff00', 0.5:'r', 1.:'b'})
#    white_red = make_colormap({0.:'w', 1.:'r'})
#    white_blue = make_colormap({0.:'w', 1.:'b'})
#    
#    schlieren_grays = schlieren_colormap('k')
#    schlieren_reds = schlieren_colormap('r')
#    schlieren_blues = schlieren_colormap('b')
#    schlieren_greens = schlieren_colormap('g')
def make_colormap(colors):
    """
    Define a new color map based on values specified in the dictionary
    colors, where colors[z] is the color that value z should be mapped to,
    with linear interpolation between the given values of z.

    The z values (dictionary keys) are real numbers and the values
    colors[z] can be either an RGB list, e.g. [1,0,0] for red, or an
    html hex string, e.g. "#ff0000" for red.
    """

    from matplotlib.colors import LinearSegmentedColormap, ColorConverter
    from numpy import sort
    
    z = sort(colors.keys())
    n = len(z)
    z1 = min(z)
    zn = max(z)
    x0 = (z - z1) / (zn - z1)
    
    CC = ColorConverter()
    R = []
    G = []
    B = []
    for i in range(n):
        #i'th color at level z[i]:
        Ci = colors[z[i]]      
        if type(Ci) == str:
            # a hex string of form '#ff0000' for example (for red)
            RGB = CC.to_rgb(Ci)
        else:
            # assume it's an RGB triple already:
            RGB = Ci
        R.append(RGB[0])
        G.append(RGB[1])
        B.append(RGB[2])

    cmap_dict = {}
    cmap_dict['red'] = [(x0[i],R[i],R[i]) for i in range(len(R))]
    cmap_dict['green'] = [(x0[i],G[i],G[i]) for i in range(len(G))]
    cmap_dict['blue'] = [(x0[i],B[i],B[i]) for i in range(len(B))]
    mymap = LinearSegmentedColormap('mymap',cmap_dict)
    return mymap
def showcolors(cmap):
    from pylab import colorbar, clf, axes, linspace, pcolor, \
         meshgrid, show, axis, title
    #from scitools.easyviz.matplotlib_ import colorbar, clf, axes, linspace,\
                 #pcolor, meshgrid, show, colormap
    clf()
    x = linspace(0,1,21)
    X,Y = meshgrid(x,x)
    pcolor(X,Y,0.5*(X+Y), cmap=cmap, edgecolors='k')
    axis('equal')
    colorbar()
    title('Plot of x+y using colormap')
def schlieren_colormap(color=[0,0,0]):
    """
    For Schlieren plots:
    """
    from numpy import linspace, array
    if color=='k': color = [0,0,0]
    if color=='r': color = [1,0,0]
    if color=='b': color = [0,0,1]
    if color=='g': color = [0,0.5,0]
    if color=='y': color = [1,1,0]
    color = array([1,1,1]) - array(color)
    s  = linspace(0,1,20)
    colors = {}
    for key in s:
        colors[key] = array([1,1,1]) - key**10 * color
    schlieren_colors = make_colormap(colors)
    return schlieren_colors
def make_amrcolors(nlevels=4):
    """
    Make lists of colors useful for distinguishing different grids when 
    plotting AMR results.

    INPUT::
       nlevels: maximum number of AMR levels expected.
    OUTPUT::
       (linecolors, bgcolors) 
       linecolors = list of nlevels colors for grid lines, contour lines
       bgcolors = list of nlevels pale colors for grid background
    """

    # For 4 or less levels:
    linecolors = ['k', 'b', 'r', 'g']
    # Set bgcolors to white, then light shades of blue, red, green:
    bgcolors = ['#ffffff','#ddddff','#ffdddd','#ddffdd']
    # Set bgcolors to light shades of yellow, blue, red, green:
    #bgcolors = ['#ffffdd','#ddddff','#ffdddd','#ddffdd']

    if nlevels > 4:
        linecolors = 4*linecolors  # now has length 16
        bgcolors = 4*bgcolors
    if nlevels <= 16:
        linecolors = linecolors[:nlevels]
        bgcolors = bgcolors[:nlevels]
    else:
        print "*** Warning, suggest nlevels <= 16"

    return (linecolors, bgcolors)
def linearMap(x,a,b,A=0,B=1):
    # This function takes scalar X in range [a1,b1] and maps it to [A1,B1]
    # values oout of a and b are clipped to boundaries 
    if a == b:
        res = B
    else:
        res = (x-a)/(b-a)*(B-A)+A
    if res < A: res = A
    if res > B: res = B
    return res
def isSparse(x):
    return isinstance(x,sparse.lil_matrix) or isinstance(x,sparse.csr_matrix)        
def generalDot(x,y):
    if isSparse(x):
        #active_indecies = x.nonzero()[0].flatten()
        return x.multiply(y).sum()
    else:
        return dot(x,y)
def normpdf(x, mu, sigma):
    return stats.norm.pdf(x,mu,sigma)
def factorial(x):
    return misc.factorial(x)
def nchoosek(n,k):
    return misc.comb(n,k)
def findElem(x,A):
    if x in A:
        return A.index(x)
    else:
        return []    
def findElemArray1D(x,A):
    res = where(A==x)
    if len(res[0]):
        return res[0].flatten()
    else:
        return []
def findElemArray2D(x,A):
    # Find the index of element x in array A
    res = where(A==x)
    if len(res[0]):
        return res[0].flatten(), res[1].flatten()
    else:
        return [], []
def findRow(r,X):
    # return the indices of X that are equal to X.
    # row and X must have the same number of columns
    #return nonzero(any(logical_and.reduce([X[:, i] == r[i] for i in range(len(r))])))
    #return any(logical_and(X[:, 0] == r[0], X[:, 1] == r[1]))
    ind = nonzero(logical_and.reduce([X[:, i] == r[i] for i in range(len(r))]))
    return ind[0] 
def perms(X):
    # Returns all permutations
    # X = [2 3]
    # res = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]
    # X = [[1,3],[2,3]]
    # res = [[1,2],[1,3],[3,2],[3,3]
    # Outputs are in numpy array format
    allPerms, _ = perms_r(X, perm_sample= array([],'uint8') , allPerms = None,ind = 0)
    return allPerms
######################################################
def perms_r(X, perm_sample= array([],'uint8') , allPerms = None,ind = 0):
    if allPerms is None:
        #Get memory
        if isinstance(X[0], list):
            size        = prod([len(x) for x in X])
        else:
            size        = prod(X)
        allPerms    = zeros((size,len(X)),'uint8')
    if len(X) == 0:
        allPerms[ind,:] = perm_sample
        perm_sample = array([],'uint8')
        ind = ind + 1;
    else:
        if isinstance(X[0], list):
            for x in X[0]:
                allPerms, ind = perms_r(X[1:],hstack((perm_sample, [x])), allPerms, ind)
        else:
            for x in arange(X[0]):
                allPerms, ind = perms_r(X[1:],hstack((perm_sample, [x])), allPerms, ind)
    return allPerms, ind
######################################################
def vec2id(x,limits):
    #returns a unique id by calculating the enumerated number corresponding to a vector given the limits on each dimenson of the vector
    # I use a recursive calculation to save time by looping once backward on the array = O(n)
    _id = 0
    for d in arange(len(x)-1,-1,-1):
        _id *= limits[d]
        _id += x[d]
    return _id
######################################################
def id2vec(_id,limits):
    #returns the vector corresponding to an id given the limits (invers of vec2id)
    prods = cumprod(limits)
    s = [0] * len(limits)
    for d in arange(len(prods)-1,0,-1):
        s[d] = int(_id / prods[d-1])
        _id %= prods[d-1]
    s[0] = _id
    return s

createColorMaps()
FONTSIZE = 12
rc('font',**{'family':'serif','sans-serif':['Helvetica']})
mpl.rcParams['font.size'] = 12.
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['axes.labelsize'] = 12.
mpl.rcParams['xtick.labelsize'] = 12.
mpl.rcParams['ytick.labelsize'] = 12.

