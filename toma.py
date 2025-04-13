import json

def main():
    arquivo = open('lista_materias.json', 'r')
    arquivo = json.load(arquivo)
    print(f"arquivo = {arquivo}")
    lista_horas = []
    for hora in arquivo['Disciplinas2'].items():
        print(f"{hora[0]} = {hora[1]}")
        hora_falsa = hora[1].replace('h', '')
        lista_horas.append(int(hora_falsa))
        
    total = sum(lista_horas)
    print(f"total = {total}")
    
main()