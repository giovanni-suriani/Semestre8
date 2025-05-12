import re

texto = "3 +3 -4.5 2/3 +2/3x1 -7a +4 -3/2 x1 -3/2"

padrao = re.compile(r'(?<![\w/])([+-]?(?:\d+\.\d+|\d+/\d+|\d+))(?![\w/])')
matches = padrao.findall(texto)
print(matches)
