import os

def choseCol(c):
    """Select ANSI prefix for writing to the terminal in colour."""
    if c == "white":
        return "\033[0m"
    elif c == "cyan":
        return "\033[36m"
    elif c == "green":
        return "\033[32m"
    elif c == "red":
        return "\033[31m"
    elif c == "yellow":
        return "\033[33m"
    else:
        raise ValueError("Color not recognised!")


def clearScreen():
    os.system("clear")


def ps():
    """Print space on board"""
    print(" ", end="")
    
def pg(c): #ega
    """Print large field"""
    print(choseCol(c) + "O", end="")
    
def pt(c): #eta
    """Print small field"""
    print(choseCol(c) + "o", end="")
    
def nl():
    """Print new line"""
    print("\033[0m")

def printBoard(board):
    nl()
    pg(board.fields["s11"]["piece"].colour)
    pg(board.fields["s12"]["piece"].colour)
    ps()
    ps()
    pt(board.fields["f08"]["piece"].colour)
    pt(board.fields["f09"]["piece"].colour)
    pg(board.fields["f10"]["piece"].colour)
    ps()
    ps()
    pg(board.fields["s21"]["piece"].colour)
    pg(board.fields["s22"]["piece"].colour)
    nl()
    
    pg(board.fields["s13"]["piece"].colour)
    pg(board.fields["s14"]["piece"].colour)
    ps()
    ps()
    pt(board.fields["f07"]["piece"].colour)
    pg(board.fields["g20"]["piece"].colour)
    pt(board.fields["f11"]["piece"].colour)
    ps()
    ps()
    pg(board.fields["s23"]["piece"].colour)
    pg(board.fields["s24"]["piece"].colour)
    nl()
    
    ps()
    ps()
    ps()
    ps()
    pt(board.fields["f06"]["piece"].colour)
    pg(board.fields["g21"]["piece"].colour)
    pt(board.fields["f12"]["piece"].colour)
    ps()
    ps()
    ps()
    ps()
    nl()
    
    ps()
    ps()
    ps()
    ps()
    pt(board.fields["f05"]["piece"].colour)
    pg(board.fields["g22"]["piece"].colour)
    pt(board.fields["f13"]["piece"].colour)
    ps()
    ps()
    ps()
    ps()
    nl()
    
    pg(board.fields["f00"]["piece"].colour)
    pt(board.fields["f01"]["piece"].colour)
    pt(board.fields["f02"]["piece"].colour)
    pt(board.fields["f03"]["piece"].colour)
    pt(board.fields["f04"]["piece"].colour)
    pg(board.fields["g23"]["piece"].colour)
    pt(board.fields["f14"]["piece"].colour)
    pt(board.fields["f15"]["piece"].colour)
    pt(board.fields["f16"]["piece"].colour)
    pt(board.fields["f17"]["piece"].colour)
    pt(board.fields["f18"]["piece"].colour)
    nl()
    
    pt(board.fields["f39"]["piece"].colour)
    pg(board.fields["g10"]["piece"].colour)
    pg(board.fields["g11"]["piece"].colour)
    pg(board.fields["g12"]["piece"].colour)
    pg(board.fields["g13"]["piece"].colour)
    ps()
    pg(board.fields["g33"]["piece"].colour)
    pg(board.fields["g32"]["piece"].colour)
    pg(board.fields["g31"]["piece"].colour)
    pg(board.fields["g30"]["piece"].colour)
    pt(board.fields["f19"]["piece"].colour)
    nl()
    
    pt(board.fields["f38"]["piece"].colour)
    pt(board.fields["f37"]["piece"].colour)
    pt(board.fields["f36"]["piece"].colour)
    pt(board.fields["f35"]["piece"].colour)
    pt(board.fields["f34"]["piece"].colour)
    pg(board.fields["g43"]["piece"].colour)
    pt(board.fields["f24"]["piece"].colour)
    pt(board.fields["f23"]["piece"].colour)
    pt(board.fields["f22"]["piece"].colour)
    pt(board.fields["f21"]["piece"].colour)
    pg(board.fields["f20"]["piece"].colour)
    nl()
    
    ps()
    ps()
    ps()
    ps()
    pt(board.fields["f33"]["piece"].colour)
    pg(board.fields["g42"]["piece"].colour)
    pt(board.fields["f25"]["piece"].colour)
    ps()
    ps()
    ps()
    ps()
    nl()
    
    ps()
    ps()
    ps()
    ps()
    pt(board.fields["f32"]["piece"].colour)
    pg(board.fields["g41"]["piece"].colour)
    pt(board.fields["f26"]["piece"].colour)
    ps()
    ps()
    ps()
    ps()
    nl()
    
    pg(board.fields["s41"]["piece"].colour)
    pg(board.fields["s42"]["piece"].colour)
    ps()
    ps()
    pt(board.fields["f31"]["piece"].colour)
    pg(board.fields["g40"]["piece"].colour)
    pt(board.fields["f27"]["piece"].colour)
    ps()
    ps()
    pg(board.fields["s31"]["piece"].colour)
    pg(board.fields["s32"]["piece"].colour)
    nl()
    
    pg(board.fields["s43"]["piece"].colour)
    pg(board.fields["s44"]["piece"].colour)
    ps()
    ps()
    pg(board.fields["f30"]["piece"].colour)
    pt(board.fields["f29"]["piece"].colour)
    pt(board.fields["f28"]["piece"].colour)
    ps()
    ps()
    pg(board.fields["s33"]["piece"].colour)
    pg(board.fields["s34"]["piece"].colour)
    nl()
    nl()
    nl()