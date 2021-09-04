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


