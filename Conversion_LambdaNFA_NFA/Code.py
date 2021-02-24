import copy
f = open("tests.in")


def dict_index(positions,value):
    for cheie, val in positions.items():
        if value == val:
            return cheie


def inchidere(state,result,closure):
    global matrix,lambda_position
    # orice stare face parte din propria sa lambda inchidere
    result.extend(matrix[state][lambda_position])
    # parcurgem starile in care starea state poate ajunge printr-o tranzitie lambda
    for j in matrix[state][lambda_position]:
        # avand in vedere ca lista closure respecta corespondenta: pe pozitia x(care reprezinta starea x) se afla
        # inchiderea lui x, verificam pe baza inegalitatii urmatoare daca inchiderea starii j a fost deja calculata
        if j<len(closure):
            result.extend(closure[j]) #in cazul in care a fost deja calculata, stiind ca λ-inchiderea unei multimi
                                     # de stari este egala cu reuniunea λ-inchiderii fiecarei stari din multime,
                                     # adaugam inchiderea stari j la inchiderea pe care o calculam in momentul de fata
        else:
            # in cazul in care nu a fost calculata inchiderea starii j, apeleam functia inchidere pentru starea j
            inchidere(j,result,closure)

# functia calculeaza multimea starilor in care putem ajunge plecand de la starile din state_set si folosindu-ne de
# o tranzitie cu letter
def find_states(state_set,letter):
    result=[]
    global matrix,position
    for state in state_set:
        result.extend(matrix[state][position[letter]])
    return set(result)

# marcam starea i ca fiind eliminata
def eliminare(i,j,matrix_transition,n,m,new_final_states):

    for k in range(n):
        for l in range(m):
            if (i in matrix_transition[k][l]):
                matrix_transition[k][l].remove(i)
                matrix_transition[k][l].add(j)
    for l in range(m):
        matrix_transition[i][l]= {-1}
    if i in new_final_states:
        new_final_states.remove(i)

def conversion():
    global matrix,n,m,alfa,position,final_q,q0
    # Step 1 - lambda closure
    closure=[] # aceasta lista va contine la finalul pasului lambda closururile tuturor starilor ale automatul initial
    for state in range(n):
        # Vom calcula pentru fiecare stare lambda closure, retinand rezultatul in result
        result=[state]
        inchidere(state,result,closure)
        # pentru a nu avea stari care se repeta in inchidere, transformam elementele listei closure in multimi
        closure.append(set(result))

    print(*closure)
    # Step 2 - * char *
    #cream un dictionar care sa retina pentru fiecare litera alfa din alfabet starile in care putem ajunge plecand
    # de la inchiderea fiecarei stari printr-o tranzitie alfa
    reachable_States=dict.fromkeys(alfa,[])
    for letter in reachable_States.keys():
        find=[]
        for state_set in closure:
            find.append(find_states(state_set,letter))
        reachable_States[letter]=copy.deepcopy(find)
    print(reachable_States)
    # pentru fiecare multime de stari corespondenta unei litera alfa, vom calcula inchiderea acesteia
    # si o vom retine in dictionarul new_states
    # dictionarul new_states este de forma: litera α: [ {λ∗αλ∗ raportata la starea 0} , {λ∗αλ∗ raportata la starea 1}, etc..]
    new_states=dict.fromkeys(alfa,[])
    for letter in new_states.keys():
        final=[]
        for state_set in reachable_States[letter]:
            rezultat=[]
            for state in state_set:
                rezultat.extend(closure[state])
            final.append(set(rezultat))
        new_states[letter]=copy.deepcopy(final)
    for letter in new_states.keys():
        for x in new_states[letter]:
            print(*x)

    # cream matricea de tranzitii
    # indicele liniei va reprezenta numarul starii
    # indicele coloanei va reprezenta pozitia literei in alfabet
    matrix_transition= [[[] for j in range(m)] for i in range(n)]
    for letter in new_states.keys():
        i=0
        for list in new_states[letter]:
           matrix_transition[i][position[letter]]=list
           i=i+1
    for x in matrix_transition:
        print(*x)
#         Step 3 - initial and final states
#     calculam starile finale
    new_final_states=[]
    for i in range(len(closure)):
        ok=0
        for x in final_q:
            # trebuie verificat in closure sau in matrix_transition?
            if x in closure[i]:
                ok=1
        if ok==1:
            new_final_states.append(i)
    print(*new_final_states)
#     Step 4 - get rid of the redundant states
    N=n #la inceput avem acelasi numar de stari
    deleted_states=[]
    for i in range(n-1):
        for k in range(i+1,n):
            ok=1

            # verificam conditia ca toate tranzitiile pentru toate caracterele sa fie identice
            for j in range(m):
                if matrix_transition[i][j]!=matrix_transition[k][j]:
                    ok=0
                    continue
            # verificam conditia ca ambele sa fie stari finale sau nu
            if (i in new_final_states)!=(k in new_final_states):
                ok=0

            if ok==1:
                N-=1
                eliminare(k,i,matrix_transition,n,m,new_final_states)
                deleted_states.append(k)
    print()
    for x in matrix_transition:
        print(*x)
    print(*new_final_states)



    MATRIX=dict()
    for i in range(n):
        if i not in deleted_states:
            MATRIX[i]=[]
            for j in range(m):
                MATRIX[i].append(matrix_transition[i][j])


    #redenumirea starilor
    new_key=0
    for old_key in range(n):
        if old_key not in deleted_states:

            for x in MATRIX.keys():
               for k in range(len(MATRIX[x])):
                   if old_key in MATRIX[x][k]:
                       MATRIX[x][k].remove(old_key)
                       MATRIX[x][k].add(new_key)

            for i in range(len(new_final_states)):
               if new_final_states[i]==old_key:
                      new_final_states[i]=new_key
            if old_key==q0:
                 q0=new_key


            MATRIX[new_key] = MATRIX.pop(old_key)
            new_key += 1

    print(MATRIX)
    r = open("output_nfa.txt", "w")
    r.write(str(N) + "\n")
    r.write(str(m) + "\n")
    for x in alfa:
        r.write(x + " ")
    r.write("\n")
    r.write(str(q0) + "\n")
    r.write(str(len(new_final_states)) + "\n")
    for x in new_final_states:
       r.write(str(x) + " ")
    r.write("\n")
    # numaram tranzitiile
    transitions = 0
    for x in MATRIX.keys():
        for y in MATRIX[x]:
            if y!=set():
               transitions+=len(y)
    print(position)
    r.write(str(transitions) + "\n")
    for x in MATRIX.keys():

        for list_index in range(len(MATRIX[x])):
            if MATRIX[x][list_index]!= set():
                for state in MATRIX[x][list_index]:
                    r.write(str(x)+" "+dict_index(position,list_index)+" "+str(state)+"\n")




n = int(f.readline())  # numarul de stari
m = int(f.readline())  # numarul de caractere din alfabet
linie = f.readline()  # alfabetul
alfa = [x for x in linie.split()]
# cream un dictionar pentru retinerea literelor
position = {}
for i in range(m):
    position[alfa[i]] = i

position['$']=m
lambda_position=m

q0 = int(f.readline())  # starea initiala
final_states = int(f.readline())  # numarul starilor finale
linie = f.readline()  # starile finale
final_q = [int(x) for x in linie.split()]
l = int(f.readline())  # numarul de translatii

matrix = [[[] for j in range(m+1)] for i in range(n)]

# translatiile
for i in range(l):
    linie = f.readline()
    t = [x for x in linie.split()]
    t[0] = int(t[0])
    char = t[1]
    t[1] = position[char]
    t[2] = int(t[2])

    matrix[t[0]][t[1]].append(t[2])

for x in matrix:
    print(*x)
conversion()

