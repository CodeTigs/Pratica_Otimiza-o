def simplex(c, A, b):
    import numpy as np

    # Criar a matriz do tableau
    num_restricoes, num_variaveis = A.shape
    tableau = np.zeros((num_restricoes + 1, num_variaveis + num_restricoes + 1))

    # Preencher os coeficientes da função objetivo
    tableau[-1, :num_variaveis] = -c

    # Preencher as restrições
    tableau[:num_restricoes, :num_variaveis] = A
    tableau[:num_restricoes, num_variaveis:num_variaveis + num_restricoes] = np.eye(num_restricoes)
    tableau[:num_restricoes, -1] = b

    # Função para encontrar o pivô
    def encontrar_pivo(tableau):
        coluna_pivo = np.argmin(tableau[-1, :-1])
        if tableau[-1, coluna_pivo] >= 0:
            return None, None
        linhas = tableau[:-1, -1] / tableau[:-1, coluna_pivo]
        linhas = np.where(linhas > 0, linhas, np.inf)
        linha_pivo = np.argmin(linhas)
        if linhas[linha_pivo] == np.inf:
            return None, None
        return linha_pivo, coluna_pivo

    # Iteração do método Simplex
    while True:
        linha_pivo, coluna_pivo = encontrar_pivo(tableau)
        if linha_pivo is None:
            break
        pivo = tableau[linha_pivo, coluna_pivo]
        tableau[linha_pivo] /= pivo
        for i in range(len(tableau)):
            if i != linha_pivo:
                tableau[i] -= tableau[i, coluna_pivo] * tableau[linha_pivo]

    # Solução
    solucao = np.zeros(num_variaveis)
    for i in range(num_restricoes):
        if np.argmax(tableau[i, :num_variaveis]) < num_variaveis:
            solucao[np.argmax(tableau[i, :num_variaveis])] = tableau[i, -1]
    lucro_otimo = tableau[-1, -1]
    return solucao, lucro_otimo, tableau


# Exemplo de entrada de dados
if __name__ == "__main__":
    import numpy as np

    while True:
        try:
            while True:
                try:
                    num_variaveis = int(input("Escolha o número de variáveis (2, 3 ou 4): "))
                    if num_variaveis in [2, 3, 4]:
                        break
                    else:
                        print("Por favor, escolha um valor válido: 2, 3 ou 4.")
                except ValueError:
                    print("Erro: Por favor, insira um número inteiro válido para o número de variáveis.")

            print("Insira os coeficientes da função objetivo:")
            try:
                c = list(map(float, input().split()))
            except ValueError:
                print("Erro: Por favor, insira apenas valores numéricos para os coeficientes da função objetivo.")
                continue

            try:
                num_restricoes = int(input("Número de restrições: "))
            except ValueError:
                print("Erro: Por favor, insira um número inteiro válido para o número de restrições.")
                continue

            A = []
            b = []
            print("Insira os coeficientes das restrições e o lado direito:")
            for i in range(num_restricoes):
                while True:
                    try:
                        linha = list(map(float, input(f"Restrição {i + 1}: ").split()))
                        if len(linha) == num_variaveis + 1:
                            A.append(linha[:-1])
                            b.append(linha[-1])
                            break
                        else:
                            print(f"Por favor, insira {num_variaveis + 1} valores (coeficientes e lado direito).")
                    except ValueError:
                        print("Erro: Por favor, insira apenas valores numéricos para os coeficientes e o lado direito.")

            c = np.array(c)
            A = np.array(A)
            b = np.array(b)

            solucao, lucro_otimo, tableau = simplex(c, A, b)
            print("\nSolução:")
            print("Ponto ótimo:", solucao)
            print("Lucro ótimo:", lucro_otimo)
            print("Tableau final:")
            print(tableau)
        
        except ValueError:
            print("Erro na entrada de dados. Por favor, insira os valores corretamente.")
            continue

        repetir = input("Deseja executar novamente? (S=sim, N=não): ").strip().upper()
        if repetir == 'N':
            break
