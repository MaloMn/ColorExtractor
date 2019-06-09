import sys

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