

def bf2pf(f, pl):
    """Board field to player field."""
    if f.startswith("f"):
        fInt = int(f[1:3])
        if pl == 1:
            return fInt
        elif pl == 2:
            offs = 30
        elif pl == 3:
            offs = 20
        elif pl == 4:
            offs = 10
        else: raise ValueError("pl has to be between 1 and 4")
        return (fInt + offs) % 40
    elif f.startswith("g"):
        return int(f[2]) + 40
    


def bfl2pfl(bfl, pl):
    """
    Board field list to player field list
    """
    return [bf2pf(i, pl) for i in bfl]

def pf2bf(pf, pl):
    """Player field to board field."""
    
    if pl == 1:
        offs = 0
    elif pl == 2:
        offs = 10
    elif pl == 3:
        offs = 20
    elif pl == 4:
        offs = 30
    else: raise ValueError("pl has to be between 1 and 4")
    
    if pf < 40:
        return "f%02d" % ((pf + offs) % 40)
    elif pf < 44:
        #print("Converting goal field!")
        return "g%d%d" % (pl, pf - 40)
    else: raise ValueError("pf has to be < 45")
   
# not used?
def pfl2bfl(pfl, pl):
    """
    Player field list to board field list
    """
    return [pf2bf(i, pl) for i in pfl]




            
