# MnGui - Containernet version

### Features

- Visualize the Mininet topology with information about its nodes
- Define a custom startup topology
- Dynamically modify the toplogy (add/remove hosts/switches)
- Simulate a client/server setup through nodes
- Control which client can reach a specific server (connect/disconnect nodes)
- Connect clients to multiple servers or to none
- Send a request to the server from the client to test connectivity

### Limitations
- There has to be at least 2 host nodes (client or server) present in a topology at all times
- There has to be at least 1 switch in the topology at all times
- Currently works only with OpenFlow v1.3
- Relies on custom built controller to automatically manage flows

## Setup
### Dependencies
- Python 3.8.10
- Containernet
- Ryu
- PyQT6
- TinyRPC
- Docker

### How to run
1. Install all dependencies in your python venv with pip.
2. Clone the repo.
> git clone https://github.com/Peachmann/mnGui.git
3. Switch to *feature-containerize* branch.
4. Navigate to *src/containers/* subfolder.
5. Build the 2 containers.
> docker build -f Dockerfile.server -t test_server:latest .
> docker build -f Dockerfile.client -t test_client:latest .
6. Navigate to src subfolder.
7. Run the controller.
> sudo ryu-manager controller.py --observe-links
8. Run the main application
> sudo python mngui.py
9. Play around with the topology :)

### Create custom startup topology
- You can add your own custom topology based on the ones shown in *topos.py*
- Choose your topology as startup in *mininet_thread.py*
- Make sure to correctly set up all required information dicts for a correct startup
- Respect the current limitations