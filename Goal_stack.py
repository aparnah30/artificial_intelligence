init = [["B", "C"], ["A"], ["D"]]
'''
         [B]   
    _____[C]__[A]___[D]______
  
'''
goal = [["C","A"],["B","D"]]

'''  
         [C]  [B]
      ___[A]__[D]___
'''   

hand = None

#Database:-
dbOnTable = set()
dbOn = set()
dbClear = set()

#---------------------------------------------------------------------------

for i in init:
    dbClear.add(i[0])                 # first in list is clear
    dbOnTable.add(i[-1])              # last in list is on table
    for ii in range(len(i)-1):
        dbOn.add(i[ii]+"*"+i[ii+1])   #  2 * 3 , 3 * 4   ---> 2 on 3 || 3 on 4

def fun(predicate):
     # predicate[0] -->  ON
     # predicate[1] -->   1
     # predicate[2] -->   2
    global dbClear, dbOn, dbOnTable, hand

    if predicate[0]=="ON": # ON 1 2
        if predicate[1]+"*"+predicate[2] in dbOn:
            return
        else:                               # We need to perform stack action, before that call its predicates
            fun(["CL", predicate[2]])       # CLEAR 2
            fun(["HL", predicate[1]])       # HOLDING 1
            print("Stack", predicate[1], predicate[2]) #''' Stack Action'''

            dbClear.remove(predicate[2])    # Modify database once performed action 
            dbClear.add(predicate[1])
            dbOn.add(predicate[1]+"*"+predicate[2])
            hand = None

    elif predicate[0]=="CL":         # CLEAR 1
        if predicate[1] in dbClear:  # To check if 1 is clear we need to traverse dbClear
            return
        else:                        # If not clear ; To access block that is on (1 or a) i.e b
            a = predicate[1]
            b = None
            for i in dbOn:           # Here we are traversing
                if a==i[2]:
                    b = i[0]
                    break
            if b==None: return  # If no such block found that means it is clear
                                # Else we need to perform unstack operation , and before that statisy predicates
            fun(["CL", b])      
            fun(["ON", b, a])
            fun(["AE"])
            hand = b
            dbClear.add(a)
            dbClear.add(b)
            dbOnTable.add(a)
            dbOn.remove(b+"*"+a)
            print("UnStack", b, a)  #''' UnStack Action '''

    elif predicate[0]=="AE":    # ARM EMPTY 
        if hand==None:          
            return
        else:                   # If not arm empty perform putdown action
            print("PutDown", hand)  #''' PUT DOWN ACTION '''
            dbOnTable.add(hand)
            hand = None

    elif predicate[0]=="ONT": # ON TABLE 1  
        if predicate[1] in dbOnTable:
            return                 # check database
        else:
            b = None
            a = predicate[1]
            for i in dbOn:         # If not ONTABLE check what is on it first
                if a==i[2]:
                    b = i[0]
                    break
            if b==None: return
            fun(["CL", b])
            fun(["ON", b, a])
            fun(["AE"])
            hand = b
            dbClear.add(a)
            dbClear.add(b)
            dbOnTable.add(a)
            dbOn.remove(b+"*"+a)
            print("UnStack", b, a)  #'''  UNSTACK action '''

    elif predicate[0]=="HL":  # Holding
        if hand==predicate[1]: # if holding somthing return else perform Pick UP action
            return
        else:
            fun(["CL", predicate[1]])
            fun(["ONT", predicate[0]])
            fun(["AE"])

            hand = predicate[1]
            print("PickUp", hand)  #'''  PICK UP action '''

# Start with satisfying goal state
for i in goal:
    fun(["CL",i[0]])
    for ii in range(len(i)-2, -1, -1):
        fun(["ON", i[ii], i[ii+1]])
    fun(["ONT",i[-1]])
    fun(["AE"])




for i in goal:
    fun(["CL",i[0]])
    for ii in range(len(i)-2, -1, -1):
        fun(["ON", i[ii], i[ii+1]])
    fun(["ONT",i[-1]])
    fun("AE")
