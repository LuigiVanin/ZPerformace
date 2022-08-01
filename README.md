# ZigBee Test Tool

O projeto consiste em uma ferramenta para auxiliar na realização de testes de performaces com dispositivos digi XBee que utilizam o protocolo de comunicação ZigBee

Para utilizar as ferramentas do projeto basta baixar o repositório com `git clone` ou pelo próprio download do github, e instalar as dependências necessárias com o comando:

```bash
$ pip install -r requirements.txt
```

OBS.: Caso tenha problemas em instalar a biblioteca digi-xbee que consta no arquivo [requirements.txt](./requirements.txt) você pode instalar a biblioteca usando a recomendação do repositório da Digi, [LINK](https://github.com/digidotcom/xbee-python)

<br>

## Como utilizar a ferramenta?

No momento a ferramenta dispões de dois recursos um para medir a valor de throughput entre dois dispoistivos XBee e outro para enviar dados, que podem ser strings de até 256 caracteres ou imagens (ainda em implementação), entre dois dispositivos ambos os recursos utilizam o protocolo ZigBee. Para realizar o teste de throughput citado anteriormente existem dois métodos, se pode utilizar a linha de comando da ferramenta ou importar em arquivo python as funções necessárias para a realização do teste de throughput.

Vale salientar que para realizar o teste de throughput é necessário dois aparelhos, um receptor e outro entregador, ou seja, para que o teste seja realizado se deve ter dois comandos ocorrendo paralelamente, um para enviar dados e outro para receber.

-   ### **Via código Python**:

É Necessário utilizar a biblioteca Digi Xbee já citada, a utilização dessa biblioteca é simples e pode ser vista nos arquivos exemplo da pasta de [sample](samples/through_put_test). Para realizar o teste é necessário ter dois arquivos python um como receptor e outro como entregador, o entregador deve estar na máquina que irá enviar os pacotes do teste enqunato que o receptor deve estar na máquina a qual o está o dispositivo que irá receber e armazenar os dados do teste.

-   **Receptor**: O receptor deve ser o primeiro código a ser rodado.

```python
# importação da função que recebe os pacotes de dados do throughput
from zigbee_tool.core.tests.throughput import throughput_receiver
...
# utilização da função
throughput_receiver(
    device_receiver=local_device,
    file_dets=file_dest # arquivo CSV destino dos dados extraídos do teste (opcional)
)
```

-   **Entregador**: O entregador só pode ser rodado após o receptor já estiver sendo operado, caso contrário ocorrerá um erro.

```python
# importação da função que envia os pacotes de dados do throughput
from zigbee_tool.core.tests.throughput import throughput_sender
...
# utilização da função
throughput_sender(
        local=local_device,
        remote=remote_device,
        packet_size=size_Bytes,
        pack_amount=amount_packet,
        rep_amount=repetition_number
        
    )
```

Para um exemplo prático de como utilizar ambas as funções `throughput_receiver` e `throughput_sender` paralalemente veja o README da pasta de samples e os arquivos python de demostração. [LINK](samples/through_put_test)

-   ### **Via CLI**:

Para utilizar a CLI do projeto basta usar o terminal e chamar um arquivo python que possua a importação da ferramenta CLI, como no arquivo [main_cli](./main_cli.py)(inclusive o mesmo arquivo pode ser utilizado para se chamar as funções via linha de comando).

Abaixo um exemplo de como utilizar a CLI:

```bash
> python main_cli.py senddata --help
```

_O comando acima checa os parâmetros do comando senddata que performa a tarefa de mandar uma mensagem síncrona para um nó definido._

Agora, como utilizar a cli para realizar um teste de throughput? Para isso é necessário utilizar os comandos `peformacereceiver` e `performacesender`, esses comandos devem ser utilizados na respectiva ordem pelo mesmo motivo citado do método **via python**. Caso fique confuso sobre o funcionamento desses dois comandos é sempre possível utilizar a flag `--help` para conseguir mais informações sobre o comando e seus parâmetros.

Abaixo um exemplo do teste de throughput via CLI, supondo que temos um dispositivo na porta _/dev/ttyUSB0_(receptor com ID de router4) e outro na _/dev/ttyUSB1_(entregador com ID de router2) de uma mesma máquina:

-   Comando receptor:

```bash
# python main_cli.py peformacereceiver PORT DEST_FILE(opcional) <-- comentário(ignore)

> python main_cli.py peformacereceiver /dev/ttyUSB0

ou

> python main_cli.py peformacereceiver /dev/ttyUSB0 /data/data.csv
```

-   Comando entregador:

```bash
# python main_cli.py performacesender PORT DEST PACKET_SIZE PACKET_AMOUNT REPETITIONS <-- comentário(ignore)

> python main_cli.py performacesender /dev/ttyUSB1 router4 84 100 3
```

Esses comandos acima resultariam em um teste com pacotes com 84 bytes de tamanho, com 100 testes e com 3 repetições, que tem como aparelho receptor o _router4_ e como entregador o _router2_.

-   ### **Envio e recebimento de dados**:
Também é possível enviar e receber dados utilizando esta ferramenta. Para enviar dados é necessário a porta, o nó de destino e o dado a ser enviado. Já para receber é nescessário apenas a porta do dispositivo.
Para enviar dados é similar ao recurso anterior:

```bash
# python main_cli.py senddata PORT DEST String <-- comentário(ignore)

> python main_cli.py senddata /dev/ttyUSB0 route04 teste123

ou

# python main_cli.py senddata PORT DEST IMAGE_FILE <-- comentário(ignore)

> python main_cli.py senddata /dev/ttyUSB0 route04 imageFrag/image.png

```

Para receber dados:

```bash
# python main_cli.py receivedata PORT <-- comentário(ignore)

> python main_cli.py receivedata /dev/ttyUSB1
```
Esses comandos acima resultariam em um envio de dados que tem como aparelho receptor o _router4_ e como entregador o _router2_.

-   ### **Verificar dispositivos conectados fisicamente**:
É possível detectar dispositivos conectados fisicamente através do comando `checkdevices`, porém funciona apenas no Linux!
Seram apresentados os dados de porta, nó e endereço MAC.

```bash
> python main_cli.py checkdevices

Possível saida:
Foram encontrados 2 dispositos:
PORT - NODE - MAC
(1)/dev/ttyUSB1 - router04 - 0000000000001234
(2)/dev/ttyUSB0 - router02 - 0000000000001234
```

