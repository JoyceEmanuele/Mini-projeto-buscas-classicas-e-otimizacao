def gradiente_descendente(inicial, objetivo, taxa=0.1, iteracoes=20):
    x = [float(bit) for bit in inicial]
    y = [float(bit) for bit in objetivo]
    transformacoes = []

    for passo in range(iteracoes):
        anterior = x.copy()
        for i in range(len(x)):
            x[i] = x[i] - taxa * 2 * (x[i] - y[i])
        diferenca = [x[i] - anterior[i] for i in range(len(x))]
        transformacoes.append(diferenca)
        erro = sum((x[i] - y[i]) ** 2 for i in range(len(x)))
        print(f"passo {passo + 1}: erro = {erro:.6f}")

    return x, transformacoes


print("gradiente descendente sem custo")
vetor_final, transformacoes = gradiente_descendente("101", "000")
print("vetor final:", vetor_final)
print("transformações:", len(transformacoes), "passos\n")


print("instabilidade: xk negativo para eta > 1/2")
xk, yk, eta = 1.0, 0.0, 0.6
xk_novo = xk - eta * 2 * (xk - yk)
print(f"xk={xk}, yk={yk}, eta={eta}")
print(f"x_novo = {xk} - {eta} * 2 * ({xk} - {yk}) = {xk_novo}")
print(f"saiu de [0,1]: {not (0 <= xk_novo <= 1)}\n")


def gradiente_com_custo(inicial, objetivo, taxa=0.1, lamb=0.1,
                        iteracoes=20, epsilon=1e-8):
    x = [float(bit) for bit in inicial]
    y = [float(bit) for bit in objetivo]
    n = len(x)

    for passo in range(iteracoes):
        z = [2 * ((x[i] - y[i])**2 + epsilon)**0.5 for i in range(n)]

        grad_c_z = [0.0] * n
        for i in range(n):
            if i > 0:
                grad_c_z[i] += z[i] - z[i - 1]
            if i < n - 1:
                grad_c_z[i] += z[i] - z[i + 1]

        gradiente = []
        for i in range(n):
            d = x[i] - y[i]
            dz_dx = 2 * d / (d**2 + epsilon)**0.5
            gradiente.append(2 * d + lamb * grad_c_z[i] * dz_dx)

        for i in range(n):
            x[i] -= taxa * gradiente[i]

        erro = sum((x[i] - y[i])**2 for i in range(n))
        z = [2 * ((x[i] - y[i])**2 + epsilon)**0.5 for i in range(n)]
        custo = 0.5 * sum((z[i + 1] - z[i])**2 for i in range(n - 1))
        J = erro + lamb * custo
        print(f"passo {passo + 1}: erro={erro:.6f}, custo={custo:.6f}, J={J:.6f}")

    return x


print("gradiente com custo - variando λ")
for lamb in [0, 0.1, 1.0]:
    print(f"\nλ = {lamb}")
    resultado = gradiente_com_custo("101", "000", lamb=lamb)
    print("vetor final:", resultado)
