import numpy as np

import skfuzzy as fuzz

from skfuzzy import control as ctrl

import matplotlib.pyplot as plt

import pandas as pd

from openpyxl import load_workbook


def ler_planilha(nome):
    """faz a leitura do arquivo excell e retorna a planilha"""
    xl = pd.ExcelFile("ferramenta-gut.xlsx")
    planilha = xl.parse(nome)
    return planilha


planilha = ler_planilha("Planilha1")



def universo():
    """Retorna o conjunto universo"""
    return planilha["G X U X T"].max() + 1


def retorna_lista_de_planilha(nome_planilha, coluna):
    """Esta funcao retorna uma lista de coluna pertencente a uma planilha"""
    return ler_planilha(nome_planilha)[coluna].values[::-1]


def gera_valores_e_graficos_das_entradas_e_saida():
    """
    esta função gera os valores das variaveis para a analise difusa
    ela retorna um dicionario como {"nome da variavel": variavel}:
    {"gravidade" : gravidade, "urgencia" : urgencia, "tendencia": tendencia, "saida" : saida}
    """

    # Variaveis do problema
    gravidade = ctrl.Antecedent(np.arange(1, 6, 1), "gravidade")
    urgencia = ctrl.Antecedent(np.arange(1, 6, 1), "urgencia")
    tendencia = ctrl.Antecedent(np.arange(1, 6, 1), "tendencia")
    saida = ctrl.Consequent(np.arange(1, 6, 1), "saida")

    # Formação do grafico das variaveis de entrada
    gravidade.automf(names=retorna_lista_de_planilha("Plan2", "Gravidade"))
    urgencia.automf(names=retorna_lista_de_planilha("Plan2", "Urgência"))
    tendencia.automf(names=retorna_lista_de_planilha("Plan2", "Tendência"))

    # formação do grafico da saida
    saida.automf(names=['Muito pouco', 'Pouco',
                        'Meio', 'Muito', 'Extremamente'])

    dicionario = {"gravidade": gravidade, "urgencia": urgencia,
                  "tendencia": tendencia, "saida": saida}

    return dicionario



def salva_imagens_do_gráfico(lista):
    """
    Esta função recebe como paramentro uma lista de variaveis da
    classe control instanciada em ctrl, Usando os metodos Antecedent
    e Consequent
    """
    for i in lista:
        i.view()
        save = i.label
        plt.savefig(save + ".png")


def regras(g, u, t):
    """ esta função gera as regras e retorna uma lista delas
    """

    # onde é gerado os valores que estão na planilha
    valores = gera_valores_e_graficos_das_entradas_e_saida()  # dict
    gravidade = retorna_lista_de_planilha("Plan2", "Gravidade")  # list
    urgencia = retorna_lista_de_planilha("Plan2", "Urgência")   # list
    tendencia = retorna_lista_de_planilha("Plan2", "Tendência")  # list
    saida = ['Muito pouco', 'Pouco', 'Meio', 'Muito', 'Extremamente']

    # salva em as regras em lista_regras
    lista_regras = []

    # aqui é onde as regras são geradas
    for indice in range(5):
        """regra = ctrl.Rule(valores["gravidade"][gravidade[indice]] |
                            valores["urgencia"][urgencia[indice]] &
                            valores["tendencia"][tendencia[indice]],
                            valores["saida"][saida[indice]]
                            )"""
        if g > t:
            regra = ctrl.Rule(valores["gravidade"][gravidade[indice]] |
                            valores["urgencia"][urgencia[indice]] &
                            valores["tendencia"][tendencia[indice]],
                            valores["saida"][saida[indice]]
                            )
            lista_regras.append(regra)

        if g <= t:
            regra = ctrl.Rule(valores["tendencia"][tendencia[indice]] |
                            valores["urgencia"][urgencia[indice]] &
                            valores["gravidade"][gravidade[indice]],
                            valores["saida"][saida[indice]]
                            )
            lista_regras.append(regra)

        if u >= g:
            regra = ctrl.Rule(valores["urgencia"][urgencia[indice]] |
                            valores["gravidade"][gravidade[indice]] &
                            valores["tendencia"][tendencia[indice]],
                            valores["saida"][saida[indice]]
                            )
            lista_regras.append(regra)
        
    return lista_regras


def out_system(g, u,  t):
    """
    Esta função recebe os parametros do metodo gut e retorna
    o numero gerado de acordo com as regras da função regras()
    """

    saida = gera_valores_e_graficos_das_entradas_e_saida()["saida"]
    # instanciando o controle do sitema
    variavel_ctrl = ctrl.ControlSystem(regras(g , u, t))
    variavel_simulador = ctrl.ControlSystemSimulation(variavel_ctrl)

    variavel_simulador.input["gravidade"] = g
    variavel_simulador.input["urgencia"] = u
    variavel_simulador.input["tendencia"] = t

    variavel_simulador.compute()
    

    return variavel_simulador.output["saida"]


def analise_difusa():
    """
    Esta função faz a operação da analise difusa em todos os itens da planilha

    """

    g = list(planilha["G"][1:])
    u = list(planilha["U"][1:])
    t = list(planilha["T"][1:])

    lista = []
    for i in range(len(g)):
        lista.append(out_system(g[i], u[i], t[i]))



    return lista


def escreve_excell():
    """
    a definir"""
    copia = planilha.copy()
    
    s = pd.Series([float("nan")] + analise_difusa(), name="vals")
    
    copia["valores"] = s

    writer = pd.ExcelWriter("arquivoeditado1.xlsx", engine= 'openpyxl')


    copia.to_excel(writer, "Sheet1")

    #analise_difusa().to_excel(writer, 'Sheet1', startrow=1, startcol=6, header=False, index=False)

    writer.save()

"""salva_imagens_do_gráfico([gera_valores_e_graficos_das_entradas_e_saida()["gravidade"]
, gera_valores_e_graficos_das_entradas_e_saida()["urgencia"]])"""

out_system(3, 2, 2)