### Configurar a interface virtual CAN (vcan0):

´sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0´

### Ferramentas necessárias:

Certifique-se de ter o pacote can-utils instalado. Este pacote inclui candump e cansend.

´sudo apt-get install can-utils´

### Escutar as mensagens CAN:

* Use candump para escutar todas as mensagens na interface vcan0:

´candump vcan0´

### Enviar mensagens CAN:

* Envie uma mensagem CAN usando cansend. Em outro terminal, execute:

´cansend vcan0 533#6DCA6EAA4264E349´
