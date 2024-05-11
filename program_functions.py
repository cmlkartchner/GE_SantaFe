
def prog2(progs1, progs2):
    print("prog2")
    if callable(progs1):
        progs1()
    if callable(progs2):
        progs2()

def prog3(progs1, progs2, progs3):
    print("prog3")
    # progs could be a function call if_food_ahead(move, left) -> already evaluated
    # else progs is a function (left, right, move)
    if callable(progs1):
        progs1()
    if callable(progs2):
        progs2()
    if callable(progs3):
        progs3()

def if_food_ahead(progs1, progs2):
    print("look for food ahead")
    if food_ahead():
        progs1()
    else:
        progs2()

def food_ahead():
    # TODO: create grid or something 
    return True
def left():
    print("turned left")
    pass
def right():
    print("turned right")
    pass
def move():
    print("moved")
    pass

def run_phenotype(phenotype):
    # translate phenotype to python code
    # run code
    # prog3(if_food_ahead(right,move),if_food_ahead(move,left),move)
    return eval(phenotype)

# prog3(if_food_ahead(right,move),if_food_ahead(move,left),move)
# prog3(if_food_ahead(left,right),right,prog3(prog2(move,prog2(right,move)),left,right))
run_phenotype("prog3(if_food_ahead(left,right),right,prog3(prog2(move,prog2(right,move)),left,right))")

# "<code>": ["<code>", "<progs>", "<progs>"],
#         "<progs>": ["<condition>","<prog2>","<prog3>","<op>"],
#         "<condition>" : ["if_food_ahead(<progs>,<progs>)"],
#         "<prog2>" : ["prog2(<progs>,<progs>)"],
#         "<prog3>" : ["prog3(<progs>,<progs>,<progs>)"],
#         "<op>" :["left","right","move"] 