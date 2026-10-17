from collections import deque
import random
import time
import matplotlib.pyplot as plt
import multiprocessing as mp


def flip_flop(bits, inicio, fim):
    bits = list(bits)
    for i in range(inicio, fim + 1):
        bits[i] = '1' if bits[i] == '0' else '0'
    return ''.join(bits)

def bfs(inicial, objetivo):
    fila = deque([(inicial, [])])
    visitados = {inicial}

    while fila:
        atual, caminho = fila.popleft()
        if atual == objetivo:
            return caminho
        for i in range(len(atual)):
            for j in range(i, len(atual)):
                novo = flip_flop(atual, i, j)
                if novo not in visitados:
                    visitados.add(novo)
                    fila.append((novo, caminho + [(i, j)]))

def executar_com_limite(funcao, inicial, objetivo, limite_segundos=5):
    def trabalhador(inicial, objetivo, conexao):
        try:
            resultado = funcao(inicial, objetivo)
            conexao.send(("OK", resultado))
        except Exception as erro:
            conexao.send(("ERRO", str(erro)))
        finally:
            conexao.close()

    conexao_receber, conexao_enviar = mp.Pipe(duplex=False)
    processo = mp.Process(target=trabalhador, args=(inicial, objetivo, conexao_enviar))
    inicio_tempo = time.perf_counter()
    processo.start()
    conexao_enviar.close()
    processo.join(limite_segundos)
    tempo = time.perf_counter() - inicio_tempo

    if processo.is_alive():
        processo.terminate()
        processo.join()
        conexao_receber.close()
        return None, tempo, False, "tempo limite"

    if conexao_receber.poll():
        tipo, resultado = conexao_receber.recv()
        conexao_receber.close()
        if tipo == "OK":
            return resultado, tempo, True, "concluído"
        return None, tempo, True, f"erro: {resultado}"

    conexao_receber.close()
    return None, tempo, True, "processo terminou sem resultado"

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
            return None

        atual = melhor_estado
        caminho.append(melhor_operacao)
        visitados.add(atual)

    return caminho

def gerar_sequencia(L):
    return ''.join(random.choice('01') for _ in range(L))


def gerar_pares(L, N):
    return [(gerar_sequencia(L), gerar_sequencia(L)) for _ in range(N)]


tamanhos = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
N = 10

experimentos = {L: gerar_pares(L, N) for L in tamanhos}
resultados = {}

for L in tamanhos:
    resultados[L] = []
    for inicial, obj in experimentos[L]:
        res_bfs, t_bfs, ok_bfs, st_bfs = executar_com_limite(
            bfs, inicial, obj, limite_segundos=60
        )
        res_gul, t_gul, ok_gul, _ = executar_com_limite(
            guloso, inicial, obj, limite_segundos=60
        )
        resultados[L].append({
            "bfs": res_bfs, "tempo_bfs": t_bfs, "ok_bfs": ok_bfs,
            "guloso": res_gul, "tempo_guloso": t_gul, "ok_guloso": ok_gul,
        })
        if not ok_bfs:
            print(f"BFS timeout: L={L}")
        if not ok_gul:
            print(f"Guloso timeout: L={L}")

medias = {}

for L in tamanhos:
    custos_bfs, custos_gul = [], []
    tempos_bfs, tempos_gul = [], []

    for r in resultados[L]:
        tempos_bfs.append(r["tempo_bfs"])
        tempos_gul.append(r["tempo_guloso"])
        if r["bfs"] is not None:
            custos_bfs.append(len(r["bfs"]))
        if r["guloso"] is not None:
            custos_gul.append(len(r["guloso"]))

    medias[L] = {
        "custo_bfs":   sum(custos_bfs) / len(custos_bfs) if custos_bfs else None,
        "custo_guloso": sum(custos_gul) / len(custos_gul) if custos_gul else None,
        "tempo_bfs":   sum(tempos_bfs) / len(tempos_bfs),
        "tempo_guloso": sum(tempos_gul) / len(tempos_gul),
    }

print("\nMÉDIAS")
for L in tamanhos:
    m = medias[L]
    print(f"\nL = {L}")
    print(f"BFS   - custo: {m['custo_bfs']}, tempo: {m['tempo_bfs']:.3f}s")
    print(f"Guloso - custo: {m['custo_guloso']}, tempo: {m['tempo_guloso']:.3f}s")

Ls          = list(tamanhos)
tempos_bfs  = [medias[L]["tempo_bfs"]   for L in Ls]
tempos_gul  = [medias[L]["tempo_guloso"] for L in Ls]
custos_bfs  = [medias[L]["custo_bfs"]   for L in Ls]
custos_gul  = [medias[L]["custo_guloso"] for L in Ls]

plt.figure(figsize=(10, 5))
plt.plot(Ls, tempos_bfs, marker='o', label='BFS')
plt.plot(Ls, tempos_gul, marker='o', label='Guloso')
plt.xscale('log', base=2)
plt.xticks(Ls, labels=Ls, rotation=45, fontsize=8)
plt.xlabel("Tamanho da sequência (L) — escala log₂")
plt.ylabel("Tempo médio (segundos)")
plt.title("Tempo médio de execução")
plt.legend()
plt.grid(True, which='both')
plt.tight_layout()
plt.savefig("grafico_tempo.png", dpi=150, bbox_inches='tight')
plt.close()

Ls_bfs = [L for L, c in zip(Ls, custos_bfs) if c is not None]
vals_bfs = [c for c in custos_bfs if c is not None]
Ls_gul = [L for L, c in zip(Ls, custos_gul) if c is not None]
vals_gul = [c for c in custos_gul if c is not None]

plt.figure(figsize=(8, 5))
plt.plot(Ls_bfs, vals_bfs, marker='o', label='BFS')
plt.plot(Ls_gul, vals_gul, marker='o', label='Guloso')
plt.xscale('log', base=2)
plt.xticks(Ls_gul, labels=Ls_gul, rotation=45, fontsize=8)
plt.xlabel("Tamanho da sequência (L) — escala log₂")
plt.ylabel("Custo médio")
plt.title("Custo médio das soluções")
plt.legend()
plt.grid(True, which='both')
plt.tight_layout()
plt.savefig("grafico_custo.png", dpi=150, bbox_inches='tight')
plt.close()

print("\ngráficos salvos: grafico_tempo.png, grafico_custo.png")
