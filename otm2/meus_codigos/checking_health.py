import str_padrao_problema as spp
import primal_dual as pd
import logging
import settings

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger("primal_dual")  # __main__
logger.debug("primal_dual.py")
logger.getChild("str_padrao_problema").setLevel(logging.INFO)

#VERBOSE = True

spp.check_health_status()
#pd.chec
""" 
manutencao em:
standard display
monta f_obj
monta restricao
"""


""" Spp functions:
_side_by_side_with_labels
display_matrix_f_obj
check_ge_zero
check_le_zero
remove_ge_le_constraints
change_variable_sign_in_constraints
change_variable_sign_in_f_obj
adicionando_variaveis_zeradas_na_expr
str_list_fraction
extrair_constantes_e_variaveis
extrai_f_obj
extrai_restricao
standard_display_variable
monta_f_obj
monta_restricao
extrai_variaveis_problema
extract_constraints_signs_problem
str_problem_to_standard_form
str_problem_to_std_form_matrix
std_matrix_to_str_problem
bateria_testes_str_padrao_problema
"""