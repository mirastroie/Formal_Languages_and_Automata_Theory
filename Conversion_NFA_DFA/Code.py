f = open("tests.in")


def dict_index(positions,value):
    for cheie, val in positions.items():
        if value == val:
            return cheie

def conversion():
    global q0, matrix,n,m

    # Step 1

    # ne luam o coada in care vom avea initial doar starea initiala
    Q=[q0]
    # cream transition_matrix - un dictionar de forma stare_folosita : [lista de stari in care poate sa ajunga]
    # astfel, primul element din lista va fi starea corespunzatoare elementului new_matrix[stare_folosita][prima litera din alfabet], al
    # doilea element din lista va fi  starea corespunzatoare elementului new_matrix[stare_folosita][a doua litera din alfabet], etc.
    # unde consideram new_matrix noua matrice de tranzitii a dfa-ului pe care il vom obtine
    transition_matrix=dict.fromkeys(Q,[])
    # ne luam un alt dictionar unde vom retine daca o stare peste care dam sau pe care o cream
    # a fost adaugata anterior in coada
    viz=dict()
    viz[q0]=1
    index=0
    while index<len(Q):
        # pentru urmatorul element din coada, trecem prin starile prin care poate sa ajunga
        for j in range(m):

            if type(Q[index])==frozenset: # daca starea este compusa, atunci obtinem tranzitia sa cu caracterul j din reuniunea starilor accesibile cu caracterul j din
                                          # toate starile componente
                set_states = set()
                for string_state in Q[index]:
                    set_states = set_states.union(set(matrix[int(string_state)][j]))
            else:
                set_states=set(matrix[Q[index]][j]) #daca starea nu e compusa, luam elementul ce reprezinta starea unica in care putem ajunge cu caracterul j
            set_states=frozenset(set_states)
            if len(set_states)==1: #daca putem ajunge intr-o singura stare
                element=list(set_states)[0]
                if element not in viz: # nu e in dictionarul de vizitat -> nu e in coada-> il adaug
                     viz[element]=1
                     Q.append(element)
                     transition_matrix[element] = [] #adaugam in dictionar starea

                transition_matrix[Q[index]].append(element) #indiferent daca a fost sau nu vizitat anterior, adaug elementul
                                                            # in matricea de tranzitii in construire, in lista corespondenta elementului din coada
                                                            # luat la momentul actual in considerare

            elif len(set_states)>1: #daca starea pe care o analizam este compusa
                 element=set()
                 for x in set_states:
                     element.add(x)
                 element=frozenset(element)
                 if element not in viz:
                    viz[element]=1
                    Q.append(element)
                    transition_matrix[element] = []

                 transition_matrix[Q[index]].append(element)
            else: # nu avem nicio tranzitie corespunzatoare
                transition_matrix[Q[index]].append(-1)
        index=index+1
    print(transition_matrix)

    # Step 2 - initial and final states

    new_q0=q0
    global final_q
    new_final_states=[]
    for x in transition_matrix.keys():
        # daca dam peste o stare compusa => verificam daca aceasta stare are in componenta cel putin o stare finala din automatul initial
        if type(x)==frozenset:
            for letter in x:
                if letter in final_q:
                    new_final_states.append(x)
                    break
        else:
            if x in final_q:
                new_final_states.append(x)
    print(new_final_states)

    # Step 3 - redenumirea starilor

    string_states=[x for x in transition_matrix.keys() if type(x)==frozenset]
    new_key=0
    # pentru fiecare cheie compusa old_key, iteram prin cheile dictionarului. Daca in listele corespunzatoare
    # acestor chei, gasim o stare egala cu old_key, atunci inlocuim valoarea din lista cu noul nume al starii old_key
    for old_key in transition_matrix.keys():
            for x in transition_matrix.keys():

                for i  in range(len(transition_matrix[x])):
                    if transition_matrix[x][i]==old_key:
                        transition_matrix[x][i]=new_key
            # daca old_key se regaseste printre starile finale, trebuie sa ii actualizam denumirea si in aceasta lista
            for i in range(len(new_final_states)):
                if new_final_states[i]==old_key:
                    new_final_states[i]=new_key
            if old_key==new_q0:
                new_q0=new_key

            transition_matrix[new_key] = transition_matrix.pop(old_key)
            new_key=new_key+1


    print(transition_matrix)
    print(new_final_states)

    r=open("output_dfa.txt","w")
    r.write(str(len(transition_matrix.keys()))+"\n")
    global  alfa, position
    r.write(str(m)+"\n")
    for x in alfa:
        r.write(x+" ")
    r.write("\n")
    r.write(str(new_q0)+"\n")
    r.write(str(len(new_final_states))+"\n")
    r.write(str(*new_final_states)+"\n")
    # numaram tranzitiile
    transitions=0
    for x in transition_matrix.keys():
        for y in transition_matrix[x]:
            if y!=-1:
                transitions+=1
    r.write(str(transitions)+"\n")
    for x in transition_matrix.keys():
        for i in range(len(transition_matrix[x])):
            if transition_matrix[x][i]!=-1:
               r.write(str(x)+" "+str(dict_index(position,i))+" "+str(transition_matrix[x][i])+"\n")



n = int(f.readline())  # numarul de stari
m = int(f.readline())  # numarul de caractere din alfabet
linie = f.readline()  # alfabetul
alfa = [x for x in linie.split()]
# cream un dictionar pentru retinerea literelor
position = {}
for i in range(m):
    position[alfa[i]] = i

q0 = int(f.readline())  # starea initiala
final_states = int(f.readline())  # numarul starilor finale
linie = f.readline()  # starile finale
final_q = [int(x) for x in linie.split()]
l = int(f.readline())  # numarul de translatii

matrix = [[[] for j in range(m)] for i in range(n)]

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


