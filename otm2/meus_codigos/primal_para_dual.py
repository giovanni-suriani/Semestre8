from fractions import Fraction
import logging
logger = logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(funcName)s:%(message)s")
logger = logging.getLogger(__name__)
import re

from otm2.meus_codigos.str_padrao_problema import *


def primal_to_dual(problem:list):
    type_problem = problem[0]
    objective_function = problem[1]
    # logica para pegar as restricoes
    for restriction in problem[2]:
        
        if re.findall(">= | <= ")


def primal_to_dual_matrixes(A, b, c, standard_form: bool, constraints):

    