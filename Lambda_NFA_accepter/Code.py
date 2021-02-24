f = open("tests.in")

# Acceptorul lambda-Nfa poate fi implementat:
# 1.) printr-o functie recursiva, care sa verifice daca o alegere
#     a traversari intr-o stare duce la o stare finala
# 2.) retinand un vector de stari in care putem ajunge in orice moment al verificarii cuvantului

# Programul meu ilustreaza prima varianta de implementare. Fie X un cuvant de verificat. Pentru prima litera
# din cuvant se  apeleaza functia recursiva "evaluate". In current_states retinem toate starile in care putem ajunge
# fara sa ne folosim de lambda miscari, iar in lambda state cele pentru care folosim lambda miscari. Pentru fiecare
# stare in current_states se apeleaza recursiv functia, trecandu-se la verificarea urmatoarei litere. La
#  reapelarea functiei, pentru toate  starile din lambda_states, nu se trece la urmatoarea litera.





def evaluate(pos_word, last_state):
    global matrix, final_q, position, word, lambda_position


    if pos_word < len(word):
        letter = position[word[pos_word]]
        current_states = matrix[last_state][letter]
        lambda_states= matrix[last_state][lambda_position]
        #pentru fiecare litera, la fiecare pas, se iau in considerare
        #starile in care putem ajunge, fie prin intermediul literei
        #luate in considerare, fie prin intermediul $


        #in cazul in care ajungem la verificarea ultimei litere
        # cautam o stare finala printre starile in care putem ajunge
        if pos_word == len(word) - 1:
            for x in current_states:
                if x in final_q:
                    return True

        #prin intermediul recursivitatii, pentru fiecare stare in care putem ajunge,
        # repetam algoritmul luand in considerare(sau nu, in cazul starilor date de $)
        # urmatoarea litera a cuvantului verificat
        value = False
        for state in current_states:
            value = value or evaluate(pos_word + 1, state)
        for state in lambda_states:
            value=value or evaluate(pos_word,state)
        # la sfarsit returnam valoarea gasita; de asemenea, se returneaza 0
        # in cazul in care din starea in care ne aflam nu mai avem alte drumuri
        return value


    #daca a terminat de verificat cuvantul si nu se ajunge intr-o stare finala, dar totusi
    # urmatoarea starea la care poate ajunge printr-o miscare lambda e finala, se returneaza 1
    lambda_states = matrix[last_state][lambda_position]
    for state in lambda_states:
        if state in final_q:
            return True
    #daca totusi mai avem stari  la care putem ajunge prin miscari lambda, atunci trebuie si acestea verificate
    value=False
    for state in lambda_states:
        value=value or evaluate(pos_word, state)
    return value
    # in cazul in care exista traiectorii pentru verificarea unui intreg cuvant,
    # dar printre ultimele stari in care putem ajunge nu regasim si una  finala, se returneaza 0


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


for word in f:
    word = word.replace("\n", "")
    print(evaluate(0, q0))

