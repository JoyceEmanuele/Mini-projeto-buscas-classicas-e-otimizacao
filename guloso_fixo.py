import time

INICIO   = "00001001000011001100111"
OBJETIVO = "00000000000000000000000"


def flip_flop(bits, inicio, fim):
    bits = list(bits)
    for i in range(inicio, fim + 1):
        bits[i] = '1' if bits[i] == '0' else '0'
    return ''.join(bits)


def heuristica(estado, objetivo):
    return sum(1 for a, b in zip(estado, objetivo) if a != b)


def guloso(inicial, objetivo):
    atual = inicial
    caminho = []
    visitados = {atual}

    while atual != objetivo:
        melhor_estado = None
        melhor_operacao = None
        melhor_h = float('inf')

        for i in range(len(atual)):
            for j in range(i, len(atual)):
                novo = flip_flop(atual, i, j)
                if novo in visitados:
                    continue
                h = heuristica(novo, objetivo)
                if h < melhor_h:
                    melhor_h = h
                    melhor_estado = novo
                    melhor_operacao = (i, j)

        if melhor_estado is None:
            return None, visitados

        atual = melhor_estado
        caminho.append(melhor_operacao)
        visitados.add(atual)

    return caminho, visitados


print(f"inicial: {INICIO}")
print(f"objetivo: {OBJETIVO}\n")

t0 = time.perf_counter()
caminho, visitados = guloso(INICIO, OBJETIVO)
tempo = time.perf_counter() - t0

print("\n RESULTADO FINAL:")
if caminho is not None:
    print(f"custo (número de operações): {len(caminho)}")
    print(f"operações: {caminho}")
    print(f"estados visitados: {len(visitados)}")
    print(f"tempo: {tempo:.4f}s")

    print("\nsequência de estados:")
    estado = INICIO
    print(f"  {estado}")
    for i, j in caminho:
        estado = flip_flop(estado, i, j)
        print(f"  flip({i},{j}) → {estado}")
else:
    print("sem solução.")
