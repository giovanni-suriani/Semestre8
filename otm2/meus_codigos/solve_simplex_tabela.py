
""" Módulo para resolver o problema de programação linear utilizando o método Simplex em tabela"""
import logging
import settings
import re

# Configuração do logger
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger("top_module")  # __main__

import str_padrao_problema as spp
import primal_dual as pd

VERBOSE = settings.VERBOSE

explain = settings.PRECISO_EXPLICAR

logger.debug("Iniciando o módulo solve_simplex_tabela")

def print_tabela():
    pass

def bateria_de_testes_solve_simplex_tabela():
    pass
    
def check_health_status():
    pass