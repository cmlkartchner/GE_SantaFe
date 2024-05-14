
def prog2(progs1, progs2):
    print("prog2 is done") # all arguments are evaluated before calling
def prog3(progs1, progs2, progs3):
    print("prog3 is done") # all arguments are evaluated before calling

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

def if_food_ahead(arg1, arg2):
    print("look for food ahead")
    if food_ahead():
        arg1()
    else:
        arg2()

def run_phenotype(phenotype):
    phenotype = phenotype.replace("left", "left||").replace("right", "right||").replace("move", "move||")
    # for if_food_ahead remove () for parameters inside function
    
    for i in range(len(phenotype)):
        if phenotype[i:].startswith("if_food_ahead"):
            left_index = phenotype.find("(", i)
            right_index = phenotype.find(")", i)
            fixed_string = phenotype[left_index:right_index].replace("|", "")
            phenotype = phenotype[:left_index] + fixed_string + phenotype[right_index:]
    phenotype = phenotype.replace("||", "()")
    return eval(phenotype)

run_phenotype("prog3(move, prog2(move, if_food_ahead(right,left)),move)")

# prog3(if_food_ahead(right,move),if_food_ahead(move,left),move)
# prog3(if_food_ahead(left,right),right,prog3(prog2(move,prog2(right,move)),left,right))
#run_phenotype("prog3(if_food_ahead(left,right),right,prog3(prog2(move,prog2(right,move)),left,right))")