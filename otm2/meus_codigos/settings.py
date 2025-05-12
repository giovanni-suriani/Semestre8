# settings.py
import os
import logging.config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VERBOSE = False

PRECISO_EXPLICAR = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "not_too_simple": {
            "format": "{levelname} {name} {funcName}: {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "debug.log"),
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "not_too_simple",
        },
    },
    "loggers": {
        "primal_dual": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "primal_dual.str_padrao_problema": { # Logger filho de primal_dual
            "level": "DEBUG",
            "propagate": True,         # <- agora sim, bloqueia propagação para o pai
            #"handlers": [],             # <- sem handler próprio
        },
        "__main__": { #  <- logger chamado quando usa getLogger(__name__)
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        # "root": {  #  <-  logger raiz
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        # },
    },
}
