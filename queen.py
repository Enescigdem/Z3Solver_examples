
import sys
import itertools

def declare(board,out):
    for i in range(1,board+1):
        for j in range(1,board+1):
            s="(declare-const p{}y{} Bool)".format(i,j)
            #print("(declare-const p{}{} Bool)".format(i,j))
	    out.write(s+"\n")
def getQueens(board,out):
    for i in range(1,board+1):
        s = "(assert (or " 
        for j in range(1,board+1):
            
            s+="p{}y{} ".format(i,j)


        s = s.strip(" ") +"))"+"\n"

        #print(s)
        out.write(s)
def getarr(board):
    arr = []
    for i in range(1,board): 
        for j in range(1,board):

            arr.append((i,j))
    return arr

def p(arr,j):
    arr1 =[e for e in arr if e[0]==j]
    lst = list(itertools.product(arr1, repeat=2))
    lst1= []
    for l in lst:
        if not l[0]==l[1]:
            lst1.append(l)

    for l in lst1:
        
        for l1 in lst1:
            
            if l[0]==l1[1]:
                if l in lst1:
                    lst1.remove(l)
    return lst1

def pCol(arr,j):
    arr1 =[e for e in arr if e[1]==j]
    lst = list(itertools.product(arr1, repeat=2))
    lst1= []
    for l in lst:
        if not l[0]==l[1]:
            lst1.append(l)

    for l in lst1:
        
        for l1 in lst1:
            
            if l[0]==l1[1]:
                if l in lst1:
                    lst1.remove(l)
    return lst1

def checkRows(board,out):
    arr = getarr(board+1)
    for j in range(1,board+1):
        lst1 = p(arr,j)
        s = "(assert (not (or " 
        for i in lst1:
                
            s+="(and p{}y{} p{}y{})".format(i[0][0],i[0][1],i[1][0],i[1][1])

        s = s.strip(" ") +")))"+"\n"
	out.write(s)
        #print(s)

#column
def checkCols(board,out):
    arr = getarr(board+1)
    for j in range(1,board+1):
        lst1 = pCol(arr,j)
        s = "(assert (not (or " 
        for i in lst1:
                
            s+="(and p{}y{} p{}y{})".format(i[0][0],i[0][1],i[1][0],i[1][1])

        s = s.strip(" ") +")))" + "\n"

        #print(s)
        out.write(s)

def get_diags(board):
    max_col = board
    max_row = board
    cols = [[] for _ in range(max_col)]
    rows = [[] for _ in range(max_row)]
    fdiag = [[] for _ in range(max_row + max_col - 1)]
    bdiag = [[] for _ in range(len(fdiag))]
    min_bdiag = -max_row +1

    for x in range(max_col):
        for y in range(max_row):
            fdiag[x+y].append((y+1,x+1))
            bdiag[x-y-min_bdiag].append((y+1,x+1))
    for f,b in zip(fdiag,bdiag):
    
        if len(f)==1:
            fdiag.remove(f)
        if len(b)==1:
            bdiag.remove(b)
    return fdiag,bdiag

def checkdiags(fdiag,bdiag,out):

    for bf in bdiag:

        s = "(assert (not (or " 
        l=list(itertools.product(bf, repeat=2))
        
        lst1= []
        for e in l:
            if not e[0]==e[1]:
                lst1.append(e) 

 
        for i in lst1:
            if not (i[0][0]==i[1][0] and i[0][1]==i[1][1]):       
                s+="(and p{}y{} p{}y{})".format(i[0][0],i[0][1],i[1][0],i[1][1])
  
        s = s.strip(" ") +")))"+"\n"
        out.write(s)
        #print(s)
       
    for df in fdiag:

        s = "(assert (not (or " 
        l=list(itertools.product(df, repeat=2))
        lst1= []
        for e in l:
            if not e[0]==e[1]:
                lst1.append(e) 

        
        for i in lst1:
            if not (i[0][0]==i[1][0] and i[0][1]==i[1][1]):       
                s+="(and p{}y{} p{}y{})".format(i[0][0],i[0][1],i[1][0],i[1][1])
            
      
        s = s.strip(" ") +")))"+"\n"
        out.write(s)
        #print(s)

def main(board,filename):
    outfile = open(filename,"w")
    outfile.write(";;declare variables\n")
    declare(board,outfile)
    outfile.write(";;should be 1 queen per line\n")
    getQueens(board,outfile)
    outfile.write(";;At most 1 queen on same column\n\n")
    checkCols(board,outfile)
    outfile.write(";;At most 1 queen on same row\n\n")
    checkRows(board,outfile)
    fdiag,bdiag = get_diags(board)[0],get_diags(board)[1]
    outfile.write(";;At most 1 queen on same diagonal lines\n")
    checkdiags(fdiag,bdiag,outfile)


    outfile.write("(check-sat)\n")
    outfile.write("(get-model)")
    outfile.close()

board = sys.argv[1]
filename = sys.argv[2]
board = int(board)

main(board,filename)





