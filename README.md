# Zero
RPC json 2.0 API

## Test Protocol only:
- [server simple](./examples/simple/server.py): ./examples/simple/server.py
- [client simple](./examples/simple/client.py): ./examples/simple/client.py

## Test RPC json 2.0:
- [server rpc](./examples/rpc/server.py): ./examples/rpc/server.py
- [client rpc](./examples/rpc/client.py): ./examples/rpc/client.py

## Setup the venv to develop
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
. ./enable_develop_path.sh
```

## Install
```bash
make install
```

## Protocols Transport
Segmented binary chunk

## Address
| Prot          | connection string    |
|---------------|----------------------|
| Domain Socket | unix:./uds_test_rpc  |
| TCP/IP        | tcp://127.0.0.1:5151 |

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


