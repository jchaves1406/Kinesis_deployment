# Ejercicio de procesamiento en tiempo real con Amazon Kinesis y Amazon EC2

Este ejercicio muestra cómo utilizar Amazon Kinesis y Amazon EC2 para procesar datos en tiempo real y realizar análisis de datos utilizando las franjas de Bollinger. El escenario planteado involucra el uso de 4 máquinas EC2 y se divide en dos partes principales: la producción de datos y el consumo y análisis de datos.

## Producción de datos

En esta parte del ejercicio, utilizamos dos máquinas EC2 para producir datos de las acciones de AMD y NVIDIA respectivamente. Cada máquina ejecuta un script de Python llamado `stream_producer.py` que descarga el precio histórico de las acciones desde 2021 y simula un flujo continuo de datos en tiempo real. Los datos se envían al servicio de Amazon Kinesis para su procesamiento posterior.

La estructura de producción de datos se divide de la siguiente manera:

- **Máquina EC2 1 (stream_producer AMD):** Esta máquina se encarga de producir los datos de la acción de AMD. El script `stream_producer.py` se modifica el simbolo a consultar por `AMD` y se ejecuta en esta máquina y se encarga de descargar los datos históricos de las acciones de AMD desde 2021. Luego, genera un flujo continuo de datos simulando un entorno en tiempo real y los envía al flujo de Kinesis correspondiente.

- **Máquina EC2 2 (stream_producer NVIDIA):** Esta máquina se encarga de producir los datos de la acción de NVIDIA. El script `stream_producer.py` se modifica el simbolo a consultar por `NVDA` se ejecuta en esta máquina y realiza un proceso similar al de la máquina EC2 1, pero para las acciones de NVIDIA. Descarga los datos históricos, genera un flujo continuo de datos y los envía al flujo de Kinesis correspondiente.

## Consumo y análisis de datos

En esta parte del ejercicio, utilizamos otras dos máquinas EC2 para consumir y analizar los datos generados por las máquinas de producción. Cada máquina ejecuta un script de Python llamado `stream_consumer.py` que lee los datos del flujo de Kinesis y realiza el cálculo de las franjas de Bollinger para cada registro. Además, muestra una alerta cuando el valor de cierre de una acción supera el límite establecido en alguna de las franjas.

La estructura de consumo y análisis de datos se divide de la siguiente manera:

- **Máquina EC2 3 (stream_consumer Bollinger superior):** Esta máquina se encarga de consumir los datos del flujo de Kinesis y realizar el cálculo de las franjas de Bollinger superiores. El script `stream_consumer_upper.py` se ejecuta en esta máquina y lee los datos en tiempo real. Para cada registro, calcula las franjas de Bollinger utilizando el método correspondiente y compara el valor de cierre de la acción con la franja superior. Si el valor de cierre supera el límite establecido, se muestra una alerta.

- **Máquina EC2 4 (stream_consumer Bollinger inferior):** Esta máquina se encarga de consumir los datos del flujo de Kinesis y realizar el cálculo de las franjas de Bollinger inferiores. El script `stream_consumer_lower.py` se ejecuta en esta máquina y realiza un proceso similar al de la máquina EC2 3, pero para las franjas inferiores. Lee
