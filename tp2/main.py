import random
cant_prendas = 0
max_lavado_len = 0

class Prenda:
    def __init__(self, tiempo_requerido,index):
        self.tiempo_requerido = tiempo_requerido
        self.incompatible = []
        self.index = index

class PrendasManager:
    def __init__(self):
        self.prendas = []

    def add_prenda(self, tiempo_requerido, index):
        prenda = Prenda(tiempo_requerido,index)
        self.prendas.append(prenda)

    def set_incompatible(self, prenda_index, incompatible_index):
        self.prendas[prenda_index].incompatible.append(incompatible_index)

    def set_tiempo_requerido(self, prenda_index, tiempo_requerido):
        self.prendas[prenda_index].tiempo_requerido = tiempo_requerido

def read_file(filename):
    prendas_manager = PrendasManager()
    global cant_prendas
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if parts[0] == 'p':
                num_prendas = int(parts[2])
                cant_prendas = num_prendas
                for i in range(num_prendas):
                    prendas_manager.add_prenda(tiempo_requerido=None, index=i)
            elif parts[0] == 'e':
                prenda_index = int(parts[1]) - 1
                incompatible_index = int(parts[2]) - 1
                prendas_manager.set_incompatible(prenda_index, incompatible_index)
            elif parts[0] == 'n':
                prenda_index = int(parts[1]) - 1
                tiempo_requerido = int(parts[2])
                prendas_manager.set_tiempo_requerido(prenda_index, tiempo_requerido)
    return prendas_manager

class Lavado:
    def __init__(self,indices,max_tiempo_requerido,incompatible,lavado):
        self.indices = sorted(indices)
        self.max_tiempo_requerido = max_tiempo_requerido
        self.incompatible = incompatible
        self.lavado = lavado
    def __eq__(self, other):
        return sorted(self.indices) == sorted(other.indices)

def check_valid_lavado(lavado1, lavado2):
    if any(index in lavado2.incompatible for index in lavado1.indices):
        return False
    if any(index in lavado1.incompatible for index in lavado2.indices):
        return False
    if any(index in lavado1.indices for index in lavado2.indices):
        return False
    return True

def combine_lavados(lavado1, lavado2):
    lavados_indices = list(set(lavado1.indices + lavado2.indices))

    max_tiempo_requerido = max(lavado1.max_tiempo_requerido, lavado2.max_tiempo_requerido)

    if max_tiempo_requerido == lavado1.max_tiempo_requerido:
        lavado = lavado1.lavado
    else:
        lavado = lavado2.lavado

    lavados_incompatible = list(set(lavado1.incompatible + lavado2.incompatible))

    lavados_combination = Lavado(lavados_indices,max_tiempo_requerido,lavados_incompatible,lavado)
    return lavados_combination

def lavados_creator(prendas):
    global max_lavado_len
    global cant_prendas
    lavados = []
    longest_incompatibles = 0
    for prenda in prendas:
        if len(prenda.incompatible) > longest_incompatibles:
            longest_incompatibles = len(prenda.incompatible) 
        lavados.append(Lavado(indices = [prenda.index],max_tiempo_requerido = prenda.tiempo_requerido, incompatible=prenda.incompatible,lavado=prenda.index))
    lavados_copy = lavados[:]
    n = 0
    lavados_copy = lavados[:]
    lavados2 = []
    while len(lavados_copy) > 0:
        
        lavados_copy.sort(key=lambda lavado: lavado.max_tiempo_requerido, reverse=True)
        top_lavado_incompatible = lavados_copy[:5]
        top_lavado_incompatible.sort(key=lambda lavado: len(lavado.incompatible), reverse=True)
        lavado = random.choice(top_lavado_incompatible)
        lavados_copy.remove(lavado)
        for j in lavados_copy:
            if check_valid_lavado(lavado, j):
                        lavado = combine_lavados(lavado, j)
                        lavados_copy.remove(j)
                        if lavado not in lavados2:
                            if len(lavado.indices) > max_lavado_len:
                                max_lavado_len = len(lavado.indices)
                            #print(lavado.indices)
                            #print(lavado.max_tiempo_requerido)
        lavados2.append(lavado)
        n+=1
    lavados2 = list(reversed(lavados2))
    for i in lavados2:
        lavados.append(i)
    print(max_lavado_len)
    print(len(lavados)-385)
    return lavados

class Combination:
    def __init__(self,indices,tiempo_requerido,lavados):
        self.indices = indices
        self.tiempo_requerido = tiempo_requerido
        self.lavados = lavados

def add_to_combination(combination, lavado):
    combined_indices = list(set(combination.indices + lavado.indices))

    tiempo_requerido = combination.tiempo_requerido + lavado.max_tiempo_requerido

    lavados_copy = combination.lavados[:]
    lavados_copy.append(lavado)

    lavados = lavados_copy

    new_combination = Combination(combined_indices, tiempo_requerido, lavados)

    return new_combination

def combination_filler(best_combination,combination,lavados):
    global cant_prendas
    # print(len(combination.indices))
    # indices_to_exclude = combination.indices
    # lavados = [lavado for lavado in lavados if not any(index in indices_to_exclude for index in lavado.indices)]
    indices_to_exclude = combination.indices

# Filter out lavados based on the comparison between lavado.lavado and indices_to_exclude
    lavados = [lavado for lavado in lavados if lavado.lavado not in indices_to_exclude]

# Sort lavados based on the number of indices each Lavado object has
    lavados.sort(key=lambda lavado: len(lavado.indices), reverse=True)
    lavados2 = lavados[:1]
    for i in lavados2:
        new_combination = add_to_combination(combination,i)
        if len(new_combination.indices)== cant_prendas:
            if new_combination.tiempo_requerido < best_combination[0].tiempo_requerido:
                #print(new_combination.tiempo_requerido)
                #print(len(new_combination.lavados))
                best_combination[0] = new_combination
        elif new_combination.tiempo_requerido > best_combination[0].tiempo_requerido:
            break
        else:
            if len(new_combination.lavados) < len(best_combination[0].lavados):
                combination_filler(best_combination= best_combination,combination=new_combination,lavados=lavados[:])



def combiantion_creator(lavados):
    best_combination = [Combination(indices=[],tiempo_requerido=1000000,lavados=[0] * 385)]
    lavados = list(reversed(lavados))
    for i in lavados[:]:
        if len(i.indices) >= len(lavados[0].indices): 
            combination = Combination(indices=i.indices,tiempo_requerido=i.max_tiempo_requerido,lavados=[i])
            pop_item = lavados.pop(0)
            #print(pop_item.indices)
            combination_filler(best_combination= best_combination,combination=combination,lavados=lavados)
    return best_combination

def write_file(combiantion):
    with open('solucion.txt', 'w') as file:
        for lavado in combiantion.lavados:
            for i in lavado.indices:
                line = f"{i+1} {lavado.lavado+1}\n"
                file.write(line)

def main():
    filename = "segundo_problema"
    prendas_manager = read_file(filename)
    for prenda in prendas_manager.prendas:
        print("prenda:",prenda.index)
        print("Tiempo requerido:", prenda.tiempo_requerido)
        print("Incompatible:", prenda.incompatible)
    tiempo = 10000
    while  tiempo > 500:
        lavados = lavados_creator(prendas_manager.prendas)
        combination = combiantion_creator(lavados)
        tiempo = combination[0].tiempo_requerido
        print("tiempo:",combination[0].tiempo_requerido)
    for i in combination[0].lavados:
        print(i.indices)
    write_file(combination[0])
    return 0

main()