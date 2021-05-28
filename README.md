# Gossip Chat

### Dependencias necesarias

- pyzmq

Este ejemplo esta diseñado con los siguientes scripts:

- server.py: distribuye los mensajes recibidos del prompt siguiendo el protocolo gossip
- prompt.py: es desde donde se envian los mensajes al server
- display.py: muestra los mensajes distribuidos por el server

### Para ejecutar el server

```
python3 server.py <node_port> <display_port>
```

### Para ejecutar el prompt

```
python3 prompt.py <username> <node_port>
```

### Para ejecutar el display

```
python3 display.py <display_port>
```
