# MnGui - Containernet version

### Features

- Visualize the Mininet topology with information about its nodes
- Define a custom startup topology
- Dynamically modify the toplogy (add/remove hosts/switches)
- View and modify flowtable of any active switch

### Limitations
- Needs RYU controller with access to topology information

## Setup
### Dependencies
- Python 3.8.10
- Mininet (or Mininet Fork such as Containernet)
- Ryu (Topology API)
- PyQT6

### How to run
1. Install all dependencies in your python venv with pip.
2. Clone the repo.
> git clone https://github.com/Peachmann/mnGui.git
3. Switch to *master* branch.
4. Navigate to src subfolder.
5. Run the controller.
> sudo ryu-manager controller.py --observe-links
6. Run the main application
> sudo python mngui.py
7. Play around with the topology :)

### Create custom startup topology
- You can add your own custom topology based on the ones shown in *topos.py*
- Choose your topology as startup in *mininet_thread.py*
- Make sure to correctly set up all required information dicts for a correct startup
- Respect the current limitations