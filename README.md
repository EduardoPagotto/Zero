# Zero
RPC json 2.0 API

## Test Protocol only:
- [server simple](./test/simple/server.py): ./test/simple/server.py
- [client simple](./test/simple/client.py): ./test/simple/client.py

## Test RPC json 2.0:
- [server rpc](./test/rpc/server.py): ./test/rpc/server.py
- [client rpc](./test/rpc/client.py): ./test/rpc/client.py

## Setup the venv
```bash
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
pip3 list
deactivate
```

## Install global
```bash
python3 -m setup.py install
```

## Install venv
```bash
source ./venv/bin/activate
./setup.py install
```

## Protocols Transport
Segmented binary chunk

## Address
|Prot   | connection string    |
|-------|----------------------|
|UDS    |  uds://uds_test_rpc  |
|TCP/IP | tcp://127.0.0.1:5151 |

### API Server
    - ServiceObject.py
        - SocketFactory.py (SocketFactoryServer)
        - ServiceServer.py
        - RPC_Response.py (json protocol 2.0 call)

### API Client
    - ServiceBus.py
        - SocketFactory.py (SocketFactoryClient)
        - ConnectionControl.py
            - ConnectionData.py
        - ProxyObject.py
            - RPC_Call.py (json protocol 2.0 execute)


