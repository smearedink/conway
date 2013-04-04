import numpy as np

def rle_read(fname):
#fname = "2011-01-26-c5-spaceships.rle"

    f = open(fname, 'r')

    content = f.readlines()
    if len(content) == 1:
        content = content[0].split("\r")

    f.close()

    lines = []
    for line in content:
        if line:
            if line.replace(" ", "")[0] != "#":
                lines.append(line.replace("\n", "").replace("\r", ""))

    xy = lines[0].replace(" ", "")

    xi = xy.find("x=")+2
    comma = xy.find(",")
    x = int(xy[xi:comma])
    xy = xy[(comma+1):]
    yi = xy.find("y=")+2
    comma = xy.find(",")
    if comma > 0:
        y = int(xy[yi:comma])
    else:
        y = int(xy[yi:])

    shape = np.zeros((x, y), dtype=bool)

    code = ''
    stillcode = True
    linenum = 1
    while stillcode:
        code += lines[linenum]
        if code[-1] == "!":
            stillcode = False
        linenum += 1

    code_spl = code.split("$")

    ypos = 0
    skiplines = 0
    for ypos in range(len(code_spl)):
        line = code_spl[ypos]
        current_xpos = 0
        while line:
            bi = line.find("b")
            oi = line.find("o")
            if bi >= 0 or oi >=0:
                ii = min(bi, oi)
                if ii < 0: ii = max(bi, oi)
                if ii == 0: length = 1
                else: length = int(line[:ii])
                if line[ii] == "b":
                    current_xpos += length
                elif line[ii] == "o":
                    shape[:,(ypos+skiplines)][current_xpos:(current_xpos+length)] = 1
                    current_xpos += length
                line = line[(ii+1):]
            else:
                if line[-1] != "!":
                    skiplines += int(line) - 1
                else:
                    if len(line) > 1:
                        skiplines += int(line[:-1]) - 1
                line = ''

    return shape
