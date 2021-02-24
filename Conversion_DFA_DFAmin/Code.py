import copy
f=open("test.in")

def dict_index(positions,value):
    for cheie, val in positions.items():
        if value == val:
            return cheie


def parcurgere_dead_end(i, new_final_states,new_matrix,groups,m):

    # daca starea pe care vrem sa o verificam e finala => returnam True
    if groups[i] in new_final_states:
        return True

    prim=0            #  indice 0        1    2
                      #  viz    1        0    1
                      #  groups {1,2,3} {4}  {0}
    coada=[i]
    viz=[0]*len(groups)
    viz[i]=1
    while prim<len(coada):
        varf=coada[prim]
        for j in range(m):
            if new_matrix[varf][j] in new_final_states:
                return True
            element=groups.index(new_matrix[varf][j])
            if viz[element]==0:
                viz[element]=1
                coada.append(element) # folosim functia index cu observatia ca elementele din lista groups sunt distincte
        prim+=1

    return False

def parcurgere_inaccesbile(q0,state, new_final_states,new_matrix,groups,m):

                      #  indice 0        1    2
                      #  viz    1        0    1
                      #  groups {1,2,3} {4}  {0}
    if state==q0:
        return True
    prim = 0
    coada=[q0]
    viz=[0]*len(groups)
    viz[q0]=1
    while prim<len(coada):
        varf=coada[prim]
        for j in range(m):
            if new_matrix[varf][j]==groups[state]:
                return True
            element=groups.index(new_matrix[varf][j]) # folosim functia index cu observatia ca elementele din lista groups sunt distincte
            if viz[element]==0:
                viz[element]=1
                coada.append(element)
        prim+=1

    return False

def conversion():
    # Step 1 - making the equivalence matrix
    global matrix,n,m
    # 1.1 initializam o matrice de echivalenta cu valoare True
    eq_matrix=[[True for i in range(n)] for j in range(n)]
    # 1.2 punem False, oriunde gasim falsa relatia (r apartine lui F) <=> ( q apartine lui F)
    # intrucat matricea este simetrica, luam in considerare doar in partea de jos a acesteia
    for i in range(1,n):
        for j in range(0,i):
            if (i in final_q)!=(j in final_q):
                eq_matrix[i][j]=False
    # 1. 3 punem False, oriunde gasim perechea (p,q) pentru care  (trans(p, alfa), trans(q,alfa) este False
    # iteram prin matrice pana cand nu se mai produce nicio schimbare
    # de asemenea, trebuie sa se indeplineasca conditia pentru orice litera din alfabet sau pentru cel putin una?
    change=True
    while change!=False:
        change=False
        for i in range(1,n):
            for j in range(0,i):
                if eq_matrix[i][j]==True:
                    value=True
                    for k in range(m):
                        i_transition=matrix[i][k]
                        j_transition=matrix[j][k]
                        if i_transition<j_transition:
                            aux=i_transition
                            i_transition=j_transition
                            j_transition=aux
                        if eq_matrix[i_transition][j_transition]==False:
                            value=False
                            change=True
                            break
                    eq_matrix[i][j]=value
    # gasirea grupurilor de stari de echivalenta
    # punem in groups toate perechile (p,q) pentru care eq_matrix[p][q]=True
    groups=[]
    viz=[0]*n
    for i in range(1,n):
        for j in range(i):
            if eq_matrix[i][j]==True:
                viz[i]=1
                viz[j]=1
                groups.append({i, j})
    # in cazul in care o stare nu a fost deja pusa in vreo pereche in situatia anteriora, adaugam un set format din aceea pereche
    for i in range(len(viz)):
        if viz[i]==0:
            groups.append({i})
    # iteram prin groupuri si incercam sa gasim grupuri de forma (p,q) si (q,r) si pe acestea le transformam in (p,q,r)
    i=0
    while i<(len(groups)-1):
        j=i+1
        while j<len(groups):
            if len(groups[i].intersection(groups[j]))>0:
                new_group=groups[i].union(groups[j])
                groups[i]=new_group
                groups.remove(groups[j])
                j=j-1

            j=j+1
        i=i+1

    # afisarea matricei de echivalenta
    print(*groups)
    for i in range(n):
        for j in range(i):
            print(eq_matrix[i][j],end=" ")
        print()



    # Step 2
    new_matrix=[[-1 for i in range(m)] for j in range(len(groups))]
    for i in range(len(groups)):
       for j in range(m):

           union_result=set()
           for k in groups[i]: # pentru index-ul liniei i, luam grupul de pe pozitia i in set-ul groups
               union_result=union_result.union({matrix[k][j]})
           for x in union_result:
               for group in groups:
                   if x in group:
                       new_matrix[i][j]=group
                       break
               else:
                   # daca for-ul interior nu a fost intrerupt -> se trece la urmatoare iteratie a for-ului exterior
                   continue
               break # altfel, daca for-ul interior a fost intrerupt -> se intrerupe si for-ul exterior

    for i in range(len(groups)):
        print(groups[i],end=" : ")
        for j in range(m):
            print(new_matrix[i][j], end=" ")
        print()
    # Step 3
    for group in groups:
        if q0 in group:
            new_q0=copy.deepcopy(group)
    print("Starea initala este ",new_q0)

    new_final_states=[]
    for group in groups:
        for state in final_q:
            if state in group:
                new_final_states.append(group)
                break

    print("Starile finale sunt: ", " ".join(str(x) for x in new_final_states))

    # # Step 4 + 5: eliminarea starilor dead-end si inaccesibile
    # pentru fiecare grup-stare reprezentat de indicele i vom verifica conditiile de stare dead end, respectiv stare inaccesibila
    deleted_states=[]
    for state_index in range(len(groups)):
        # facem un algoritm modificat de parcurgere in latime a grafurilor
        v1=parcurgere_dead_end(state_index,new_final_states,new_matrix,groups,m)
        v2=parcurgere_inaccesbile(groups.index(new_q0), state_index, new_final_states, new_matrix, groups,m)
        if v1==False or v2==False:
                print("Starile care trebuie sa fie sterse: ", groups[state_index])
                deleted_states.append(state_index)



    N=len(groups)-len(deleted_states)
    M=m
    new_indexes=[]
    index=0
    # cream o noua matrice finala
    MATRIX=[[-1 for i in range(M)]for j in range(N)]
    # iteram prin starile actuale
    for i in range(len(groups)):
        #daca indexul starii nu se afla printre cele pe care vrem sa le stergem,
        # adaugam starea la new_indexes si completam tranzitiile corespunzatoare
        # starii; luam in calcul daca starea in care ajunge se mai afla
        # in automatul pe care vrem sa il construi - in caz contrar, facem abstactie
        # de tranzitie;
        if i not in deleted_states:
            new_indexes.append(groups[i])
            for j in range(m):
                if groups.index(new_matrix[i][j]) not in deleted_states:
                  MATRIX[index][j]=new_matrix[i][j]
            index=index+1

    for i in range(N):
        print(new_indexes[i],end=" : ")
        for j in range(M):
            print(MATRIX[i][j],end=" ")
        print()
    # Redenumirea starilor cu numere intregi naturale de la 0 la N-1
    for i in range(N):
        for j in range(M):
            if MATRIX[i][j]!=-1:
               MATRIX[i][j]=new_indexes.index(MATRIX[i][j])

    print(new_indexes)
    new_q0=new_indexes.index(new_q0)
    for i in range(len(new_final_states)):
        new_final_states[i]=new_indexes.index(new_final_states[i])


    for i in range(N):
        print(new_indexes[i],end=": ")
        for j in range(M):
            print(MATRIX[i][j],end=" ")
        print()

    print(new_q0)
    print(new_final_states)
    r = open("output_dfa_min.txt", "w")
    r.write(str(N) + "\n")
    global alfa, position
    r.write(str(M) + "\n")
    for x in alfa:
        r.write(x + " ")
    r.write("\n")
    r.write(str(new_q0) + "\n")
    r.write(str(len(new_final_states)) + "\n")
    r.write(str(*new_final_states) + "\n")
    # numaram tranzitiile
    transitions = 0
    for i in range(N):
        for j in range(M):
            if MATRIX[i][j]!=-1:
                transitions+=1
    r.write(str(transitions) + "\n")
    for i in range(N):
        for j in range(M):
            if MATRIX[i][j]!=-1:
                r.write(str(i)+" "+dict_index(position,j)+" "+str(MATRIX[i][j])+"\n")

n=int(f.readline()) #numarul de stari
m=int(f.readline()) #numarul de caractere din alfabet
linie=f.readline()  # alfabetul
alfa=[x for x in linie.split()]
#cream un dictionar pentru retinerea literelor
position={}
for i in range(m):
    position[alfa[i]]=i

q0=int(f.readline()) #starea initiala
final_states=int(f.readline()) #numarul starilor finale
linie=f.readline() #starile finale
final_q=[int(x) for x in linie.split()]
l=int(f.readline()) #numarul de translatii


matrix=[ [-1 for j in range(m)] for i in range(n)]
#translatiile
for i in range(l):
    linie=f.readline()
    t=[x for x in linie.split()]
    t[0]=int(t[0])
    char=t[1]
    t[1]=position[char]
    t[2]=int(t[2])

    matrix[t[0]][t[1]]=t[2]

for x in matrix:
    print(*x)

conversion()