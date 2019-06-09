import sys

def RGBtoHEXA(l):
    
    x = l[0]
    y = l[1]
    z = l[2]
    
    # Color as hexadecimal
    r = hex(int(x)).split('x')[-1]
    g = hex(int(y)).split('x')[-1]
    b = hex(int(z)).split('x')[-1]
    
    if len(r) < 2:
        r = '0' + r
    if len(g) < 2:
        g = '0' + g
    if len(b) < 2:
        b = '0' + b
    
    return '#' + r + g + b

def short(l, length):
    """ Deletes some random elements of a list to make it shorter according to
    a given length"""
    
    a = len(l)/length
    
    if a > 1:
        o = []
        o.append(l[0])
        b = a - int(a)
        while True:
            b += a
            if int(b) >= len(l):
                break
            else:
                o.append(l[int(b)])
        return o
    else:
        return l
            

def distSq(el2, el1):
    """Computes the euclidean distance between two given tuples of same dimension"""
    
    sum_ = 0
    for i in range(len(el1)):
        sum_ += (el1[i] - el2[i])**2
    return sum_

def EpsilonFinder(X, minpts):
    """Finds an appropriate epsilon following a given minpts using
    the "knee" technique. The knee is computed via multiples approximations
    by straight lines"""
    
    avg_dist = []
    
    from sklearn.neighbors import NearestNeighbors
    NN = NearestNeighbors(n_neighbors=minpts).fit(X)
    
    # Now we have the distances of the k-Nearest-Neighbors
    kNN = NN.kneighbors(n_neighbors=minpts)
    kNN = kNN[0]
    
    from numpy import average
    
    for i in range(len(X)):
        avg_dist.append(average(kNN[i]))
            
    avg_dist.sort()
    
    # On supprime toutes les valeurs inférieures ou égales à 0 et supérieures ou égales à 255*sqrt(3)
    avg_dist = list(filter(lambda x: x >= 0.01 and x <= 441.5, avg_dist))
    
    # Now we reduce our list to 300 elements.
    avg_dist = short(avg_dist, 300)
    
    ###### We figure out the knee of the curve by finding two straight lines which
    # can approximate the previous curve.
    print('Starting to compute the knee! Almost there.')
    from numpy import linspace
    
    min_g = 999999
    (a3,a4) = (0,0)
    
    for xm in linspace(2, len(avg_dist)-2, len(avg_dist)-3): 
        sum_g = 0
        xm = int(xm)
        # First straight line: y = a1*x + y0
        x0, x1 = 0, int(xm/2)
        y0, y1 = (avg_dist[x0], avg_dist[x1])
        
        # FIRST MMCO
        p = 2 # Precision of the MMCO
        
        mini = 99999
        a1 = 0
        for a in linspace(0,p*(y1-y0)/(x1-x0),50):
            som = 0
            for k in range(xm): # We don't compute it for k = xm
                som += (avg_dist[k] - (a*k+y0))**2
            if som < mini:
                mini = som
                a1 = a
        
        sum_g += mini
        
        # Second one: y = a2*x + y3 - a2*x3
        x3 = len(avg_dist)-1
        x2 = int((x3-xm)/2 + xm)
        y2, y3 = (avg_dist[x2], avg_dist[x3])
        
        # SECOND MMCO
        p = 3 # Precision of the MMCO
        
        mini = 99999
        a2 = 0
        for a in linspace(0,p*(y3-y2)/(x3-x2),50):
            som = 0
            for k in range(xm, len(avg_dist)):
                som += (avg_dist[k] - (a*k+y3-a*x3))**2
            if som < mini:
                mini = som
                a2 = a
                
        sum_g += mini
        
        if sum_g < min_g:
            min_g = sum_g
            (a3,a4) = (a1,a2)
    
    
    (a1,a2) = (a3,a4)
    
    # We have our equation, now we trace them on their intervals
    # We look for the point of encounter of the two straight lines
    
    xe = (y3-a2*x3 - y0)/(a1-a2)
    
    epsilon = a1*xe + y0
    
    # PLOTTING THE KNEE FOUND
    # =============================================================================
    import matplotlib
    matplotlib.use('Agg') #Useful to save the graph as an image later
    import matplotlib.pyplot as plt
    xe = int(xe)
    
    line1 = []
    inter1 = []
    for i in range(xe+2):
        line1.append(a1*i + y0)
        inter1.append(i)
    
    line2 = []
    inter2 = []
    for i in range(xe, len(avg_dist)):
        line2.append(a2*i + y3-a2*x3)
        inter2.append(i)
    
    fig = plt.figure(1)
    fig.set_size_inches(10,7)
    
    plt.plot(avg_dist) + plt.plot(inter1, line1) + plt.plot(inter2, line2)
    
    name = 'Knee.png'
    plt.savefig(name)
    plt.close(1)
    # =============================================================================
    
    return epsilon

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, ' %', status))
    sys.stdout.flush() # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)

def RGBtoHSB(tuple):
    # Wikipedia conversion formulas
    r = tuple[0]/255
    g = tuple[1]/255
    b = tuple[2]/255
    Cmax = max(r, g, b)
    Cmin = min(r, g, b)
    delta = Cmax - Cmin

    hue = 0
    sat = 0
    value = Cmax

    if Cmax == r and delta != 0:
        hue = 60*((g-b)/delta % 6)
    elif Cmax == g and delta != 0:
        hue = 60*((b-r)/delta + 2)
    elif Cmax == b and delta != 0:
        hue = 60*((r-g)/delta + 4)

    if Cmax != 0:
        sat = delta/Cmax

    return (hue, sat, value)

def dist(p, q):
    """Returns the distance squared between two given tuples"""
    return (p[0] - q[0])**2 +  (p[1] - q[1])**2 + (p[2] - q[2])**2

def entry(message, answers):
    var = True
    while var:
        b = input(message)
        for i in range(len(answers)):
            if b == answers[i]:
                var = False
    return b