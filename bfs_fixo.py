from collections import deque
import time

INICIO   = "00001001000011001100111"
OBJETIVO = "00000000000000000000000"


def flip_flop(bits, inicio, fim):
    bits = list(bits)
    for i in range(inicio, fim + 1):
        bits[i] = '1' if bits[i] == '0' else '0'
    return ''.join(bits)


def bfs_com_progresso(inicial, objetivo):
    fila = deque([(inicial, [])])
    visitados = {inicial}
    inicio_tempo = time.perf_counter()
    ultimo_relatorio = inicio_tempo

    print(f"iniciando BFS...")
    print(f"inicial: {inicial}")
    print(f"objetivo: {objetivo}\n")

    while fila:
        atual, caminho = fila.popleft()

        agora = time.perf_counter()
        if agora - ultimo_relatorio >= 10:
            elapsed = agora - inicio_tempo
            print(
                f"  [{elapsed:.0f}s] estados visitados: {len(visitados):,} "
                f"| profundidade atual: {len(caminho)}"
            )
            ultimo_relatorio = agora

        if atual == objetivo:
            return caminho, len(visitados), time.perf_counter() - inicio_tempo

        for i in range(len(atual)):
            for j in range(i, len(atual)):
                novo = flip_flop(atual, i, j)
                if novo not in visitados:
                    visitados.add(novo)
                    fila.append((novo, caminho + [(i, j)]))

    return None, len(visitados), time.perf_counter() - inicio_tempo


caminho, n_visitados, tempo = bfs_com_progresso(INICIO, OBJETIVO)

print("\n RESULTADO FINAL:")
if caminho is not None:
    print(f"solução encontrada em {tempo:.2f}s")
    print(f"estados visitados: {n_visitados:,}")
    print(f"custo (número de operações): {len(caminho)}")
    print(f"operações: {caminho}")

    estado = INICIO
    print(f"\nsequência de estados:")
    print(f"  {estado}")
    for i, j in caminho:
        estado = flip_flop(estado, i, j)
        print(f"  flip({i},{j}) → {estado}")
else:
    print("sem solução.")
