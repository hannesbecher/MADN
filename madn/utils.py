
# Conversion between board and player coordinates

def bf2pf(f: str, pl: int) -> int:
    """Convert board field (str) to player field (int)."""
    
    assert isinstance(f, str), "1st arg must be a of type str."
    assert isinstance(pl, int), "2nd arg must be a of type int."
    
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
        else: raise ValueError("Argument pl must be between 1 and 4")
        return (fInt + offs) % 40
    elif f.startswith("g"):
        return int(f[2]) + 40
    


def bfl2pfl(bfl, pl):
    """
    Board field list to player field list. Runs bf2pf() iteratively.
    """
    return [bf2pf(i, pl) for i in bfl]

def pf2bf(pf, pl):
    """Player field (int) to board field (str."""
    
    assert isinstance(pf, int), "1st arg must be a of type int."
    assert isinstance(pl, int), "2nd arg must be a of type int."
    assert pf >= 0 and pf < 45, "Argument pf must be 0 of more and less then 45."
    
    if pl == 1:
        offs = 0
    elif pl == 2:
        offs = 10
    elif pl == 3:
        offs = 20
    elif pl == 4:
        offs = 30
    else: raise ValueError("pl must be between 1 and 4")
    
    # ordinary field
    if pf < 40:
        return "f%02d" % ((pf + offs) % 40)
    # goal field
    else:
        #print("Converting goal field!")
        return "g%d%d" % (pl, pf - 40)
 
   
# not used?
def pfl2bfl(pfl, pl):
    """
    Player field list to board field list
    """
    return [pf2bf(i, pl) for i in pfl]




            
