# Mini-projeto: Buscas Clássicas e Otimização

Implementação do mini-projeto de PGC112 sobre a transformação de sequências de bits usando busca em largura (BFS), algoritmo guloso e gradiente descendente.

## Arquivos

### `bfs_fixo.py`

Resolve o experimento fixo do trabalho usando o algoritmo BFS (busca em largura).

O arquivo possui uma função chamada `flip_flop`, que inverte os bits dentro de um intervalo de índices. Em seguida, a função `bfs_com_progresso` realiza a busca usando uma fila. A cada 10 segundos, o programa mostra quantos estados já foram vistos e qual é a profundidade está.

No final, é mostrado o custo total, as operações realizadas, a quantidade de estados visitados, o tempo de execução e a sequência de estados gerada durante a execução.

**Atenção:** a execução pode levar aproximadamente 8 minutos.

```bash
python3 bfs_fixo.py
```

---

### `guloso_fixo.py`

Resolve o mesmo experimento fixo do trabalho, mas utilizando o algoritmo guloso.

Além da função `flip_flop`, o arquivo possui a função `heuristica`, que calcula a distância de Hamming entre o estado atual e o desejado, ou seja, quantos bits ainda são diferentes entre as sequências.

A cada passo, o algoritmo olha as possibilidades e escolhe aquela que apresenta a menor distância até o objetivo. Isso continua até encontrar a sequência desejada.

Ao final, é mostrado o custo total, as operações realizadas, a quantidade de estados visitados, o tempo de execução e a sequência de estados.

```bash
python3 guloso_fixo.py
```

---

### `desempenho.py`

Compara o desempenho do BFS e do algoritmo guloso em sequências aleatórias de diferentes tamanhos.

Os testes são realizados para tamanhos de sequência de 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048 e 4096 bits, utilizando 10 pares de sequências para cada tamanho. Cada execução tem um limite de 60s.

Quando uma execução passa o limite, o resultado é timeout. Nesse caso, o custo não entra no cálculo da média, mas o tempo da execução é contabilizado.

Ao final, o programa gera e salva dois gráficos: um com o tempo médio de execução e outro com o custo médio das soluções em função do tamanho das sequências.

**Atenção:** a execução completa pode levar cerca de 1 hora.

```bash
python3 desempenho.py
```

---

### `gradiente.py`

Tem a parte do projeto que utiliza gradiente descendente para otimizar a transformação das sequências de bits.

O arquivo começa com a função `gradiente_descendente`, que converte a sequência inicial em um vetor de valores contínuos entre 0 e 1 e atualiza. As diferenças entre os vetores consecutivos também são registradas.

Depois, o código apresenta um exemplo de instabilidade quando a taxa de aprendizado é maior que 0,5. Para isso, temos um valor inicial de 1, um valor desejado de 0 e uma taxa de aprendizado de 0,6. Com isso, o valor passa a ser -0,2, saindo do intervalo entre 0 e 1.

Também temos a função `gradiente_com_custo`, que acrescenta uma função de custo na otimização. Essa função castiga diferenças entre posições vizinhas. O cálculo utiliza a regra da cadeia.

Por fim, são realizados experimentos com diferentes valores de lambda: 0, 0,1 e 1,0 como foi pedido no projeto.

```bash
python3 gradiente.py
```

## Dependências

O projeto utiliza a biblioteca `matplotlib` para gerar os gráficos. Para instalá-la, execute:

```bash
pip install matplotlib
```