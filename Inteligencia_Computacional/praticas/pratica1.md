As configurações tomadas como menor foram as com maior accuracy, em caso de empate a de menor número de vizinhos próximos (k).

## Conjunto de dados Iris, melhores configurações:


- Dados Normalizados: k = 3, as três métricas de distância deram empate (Manhattan, Euclidiana e Minkowski), com acurácia de 100%, com pesos uniformes ou usando o inverso da distância.


- Dados não normalizados: k = 1, as três métricas de distância deram empate (Manhattan, Euclidiana e Minkowski), com acurácia de 100%, utilizando na distância euclidiana pesos uniformes ou usando o inverso da distância.

a normalização não teve impacto, sugerindo que as variáveis já estão em escalas semelhantes.


## Conjunto de dados WineQT, melhores configurações:
- Dados Normalizados: k = 17, acurácias:
  - Distância Minkowski = 0.6356
  - Distância Euclidiana (peso uniforme) = 0.6356
  - Distância Euclidiana (peso inverso da distância) = 0.6822
  - Distância Manhattan = 0.6181
<br>
- Dados Não Normalizados: k = 1, acurácias:
  - Distância Minkowski = 0.5306
  - Distância Euclidiana (peso uniforme) = 0.5306
  - Distância Euclidiana (peso inverso da distância) = 0.5306
  - Distância Manhattan = 0.5394

A normalização melhorou o desempenho, provavelmente equilibrando variáveis que tinham escalas muito diferentes.

## Conjunto de dados Evasao, melhores configurações:
- Dados Normalizados: k = 9, acurácias:
  - Distância Minkowski = 0.6356
  - Distância Euclidiana (peso uniforme) = 0.6356
  - Distância Euclidiana (peso inverso da distância) = 0.6822
  - Distância Manhattan = 0.6181
<br>
- Dados Não Normalizados: k = 1, acurácias:
  - Distância Minkowski = 0.8537
  - Distância Euclidiana (peso uniforme) = 0.8537
  - Distância Euclidiana (peso inverso da distância) = 0.8488
  - Distância Manhattan = 0.8488


A normalização piorou o desempenho, provavelmente pois a normalização reduziu diferenças relevantes dentro das variáveis.
