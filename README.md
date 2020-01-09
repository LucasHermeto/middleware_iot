# README

Last Edited: Jan 08, 2020 10:50 PM

# Middleware

Middleware para soluções IoT (Internet das Coisas) utilizando protocolo de comunicação MQTT para realizar atualizações tanto locais quanto para cloud (Google Cloud)

---

## Raspberry Pi

Para instalar o middleware na Raspberry é necessário primeiramente ter alguns pré requisitos nela:

- [Raspbian OS](https://www.raspberrypi.org/downloads/)
- Java Virtual Machine - Normalmente vem instalado dependendo da versão instalada do Raspbian OS, caso não venha execute o comando:
    sudo apt install openjdk-11-jdk
- Docker
- [Docker Compose](https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl)

OBS: Caso o python possua tanto sua versão 2 e 3 instaladas na raspberry, é necessário modificar os últimos comandos da instalação do Docker Compose para:
    sudo apt-get install -y python3-pip
    sudo pip3 install docker-compose 

## Arquitetura

Tal middleware funciona totalmente com Docker, então cada um dos seus componentes é na verdade um container, o que facilita a manutenção e também a flexibilidade no momento de escalar o projeto para soluções mais complexas. 

Os seguinte Container foram utilizados:

- Mosquitto: MQTT Broker, funciona como um intermediário para os dispositivos utilizando o protocolo MQTT consigam realizar subscribe de diversas publish's. um exemplo é a ESP32 e o servidor web de controle que realizam o publish.
- heimdall.py: Servidor intermediário que realiza subscripe a diversos tópicos que a ESP32 faz publish e envia essas informações para o banco de dados, InfluxDB
- InfluxDB: Banco de dados próprio para aplicações de tempo real e com diversos acessos em pouco tempo
- Grafana: Dashboard para criar modelos de gráficos mais simples e assim conseguir monitorar o funcionamento de cada equipamento. É possível também criar diversos alertas dependendo do estado de algum sensor e assim pedir para a ESP32 realizar algumas alterações, tudo isso ocorre com intermédio do hermodr.
- hermodr: Servidor intermediário para enviar os alertas do grafana e assim a esp32 conseguir realizar modificações diante de cada ação. Funciona também como um servidor web (Flask) para o usuário conseguir modificar os objetos.

---

# Uso

Antes de executar qualquer comando é necessário adicionar o IP do MQTT Broker e do InfluxDB que serão utilizados, caso sejam locais mesmo apenas apague todo o arquivo server.env; Lembrando que os campos no arquivo caso deseja mudar o IP devem ser por exemplo:
    BROKER_IP=192.168.0.1
    INFLUX_IP=192.168.0.1

## Uso de toda arquitetura
Para executar toda a arquitetura de controle do Middleware:

    cd docker
    sudo docker-compose up --build

OBS: O comando do docker ira ler o arquivo chamado docker-compose.yml e irá rodar todos os containers. O atributo "--build" é necessário pois existe um container que são montados na hora e não baixados do docker hub.
OBS2: Duas pastas (grafana e influxdb) serão criadas após a execução do comando, elas são utilizadas para manter ativo o backup de todas as modificações mesmo após parar o docker.

### Uso Hermodr
Caso deseja controlar a aplicação enviar publish para algum dispositivo ler você deve utilizar o Hermoder:
    cd hermodr
    source venv/bin/activate
    pip3 install -r requirements.txt
    flask run

## Uso individual de cada container

### Mosquitto:
- Instalação: sudo docker pull eclipse-mosquitto
- Execução (background): sudo docker run -itd -p 1883:1883 -p 9001:9001 --name mosquitto eclipse-mosquitto

### InfluxDB:
- Instalação: sudo docker pull influxdb
- Execução (background): sudo docker run -d -p 8086:8086 -v influxdb:/var/lib/influxdb --name influxdb influxdb
- Executando InfluxDB no docker: docker exec -it influxdb influx

### Grafana:
- Instalação: sudo docker pull grafana/grafana

## Uso - Pós iniciado
Após iniciado o docker é possível acessar alguns deles utilizando comandos do próprio docker

- InfluxDB:
    sudo docker exec -it docker_influxdb_1 influx

OBS: O argumento -it é adicionado ao comando para poder assim acessar o serviço e continuar modificando, caso contrátio será apenas um comando do docker e irá parar a execução.

## Comandos Docker
- Lista de todos os container em execução: sudo docker ps
- Parar container: sudo docker stop <containerID || name>

OBS: Para nao executar em segundo remover a opcao '-d'

---

# Erros
Caso apareça um erro nos logs com o nome de:
    middleware_heimdall_1 exited with code 1
Verifique se o seu firewall está bloquando as portas 1883 e 8086