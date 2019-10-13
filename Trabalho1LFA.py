class Automato:
    def __init__(self, es_inicial, es_finais = [], estados = [], transicoes = []):
        self.es_inicial = es_inicial
        self.es_finais = es_finais
        self.estados = estados
        self.transicoes = transicoes

# Vefifica se o estado está na lista de estados, ordenando os nomes
def contem_estado(estado, lista_estados):
    estado_sorted = sorted(estado)
    for estado_da_lista in lista_estados:
        if estado_sorted == sorted(estado_da_lista):
            return True

# Os estados finais do afd serão os estados que são compostos pelos estados finais do afnd
def estados_finais_afd(estados_finais_afnd, estados_afd):
    list_est_fin_afd = []
    for estado_final_afnd in estados_finais_afnd:
        for estado_afd in estados_afd:
            if estado_final_afnd in estado_afd:
                list_est_fin_afd.append(estado_afd)
    return list_est_fin_afd

arq_entrada = []           # Cria uma lista para armazenar as linhas do arquivo
file = open("entrada.txt", "r")  # Abre o arquivo de entrada em modo leitura
for line in file:  # Pega as linhas do arquivo
    arq_entrada.append(line.replace('\n', ''))  # Armazena a linha do arquivo na lista, removendo '\n' se houver
file.close()  # Fecha o arquivo

for i in range(2, len(arq_entrada)):    # Transforma as strings dos estados finais e das transições em listas
    arq_entrada[i] = arq_entrada[i].split()

# Cria o automato nao deterministico com os dados do arquivo de entrada
afnd = Automato(arq_entrada[1], arq_entrada[2], arq_entrada[0], arq_entrada[3:])

# Cria o automato deterministico
afd = Automato(afnd.es_inicial)      # Seta o estado inicial do AFD
afd.estados.append(afnd.es_inicial)  # Adiciona o estado inicial a lista de estados do AFD

for estado in afd.estados:  # percorre a lista de estados do afd
    transicao_afd_0 = [estado, '0', '']  # seta o estado e o simbolo de transicao para montar a transicao 0 do estado atual
    transicao_afd_1 = [estado, '1', '']  # seta o estado e o simbolo de transicao para montar a transicao 1 do estado atual
    for transicao_afnd in afnd.transicoes:   # percorre as transicoes do afnd
        if transicao_afnd[0] in estado:         # checa se estado atual do afd é composto do estado da transicao do afnd
            # Se o simbolo da transicao for 0, pega o estado resultante dessa transicao
            # Caso contrario, pega o estado resultante da transicao com o simbolo 1
            if transicao_afnd[1] == '0':
                # Adiciona a transicao de simbolo 0 do estado do afnd a transicao de simbolo 0 do afd, caso ja não esteja adicionada
                if transicao_afnd[2] not in transicao_afd_0[2]:
                    transicao_afd_0[2] += transicao_afnd[2]
            else:
                # Adiciona a transicao de simbolo 1 do estado do afnd a transicao de simbolo 1 do afd, caso ja não esteja adicionada
                if transicao_afnd[2] not in transicao_afd_1[2]:
                    transicao_afd_1[2] += transicao_afnd[2]
    # Verifica se ha estados de transição formados e se os estados formados no loop acima ja estão na lista de estados do afd
    # Se não estiverem, os adiciona na lista
    if transicao_afd_0[2] and not(contem_estado(transicao_afd_0[2], afd.estados)):
        afd.estados.append(transicao_afd_0[2])
    if transicao_afd_1[2] and not(contem_estado(transicao_afd_1[2], afd.estados)):
        afd.estados.append(transicao_afd_1[2])
    # Adiciona a lista de transicoes do afd as duas transicoes
    if transicao_afd_0[2]:
        afd.transicoes.append(' '.join(transicao_afd_0))
    if transicao_afd_1[2]:
        afd.transicoes.append(' '.join(transicao_afd_1))

# Seta os estados finais do afd
afd.es_finais = estados_finais_afd(afnd.es_finais, afd.estados)

file = open('saida.txt', "w") # Abre o arquivo de saida em modo gravacao
file.writelines(' '.join(afd.estados))  # Grava os estados na primeira linha, separados por espaço
file.write('\n' + afd.es_inicial + '\n') # Quebra uma linha, grava o estado inicial e quebra mais uma linha
file.writelines(' '.join(afd.es_finais))    # Grava os estados finais na terceira linha
file.write('\n')    # Quebra uma linha
file.writelines('\n'.join(afd.transicoes)) # Grava as transicoes, uma em cada linha
file.close() # Fecha o arquivo