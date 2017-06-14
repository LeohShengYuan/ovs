from flask import Flask, jsonify
import subprocess

#Create (Bridge with Port)
def add_port(bridge, port):
           add = subprocess.call(['sudo', 'ovs-vsctl','add-br', bridge, '--', 'add-port', bridge, port])

#Read  
def get_ports():

    ports = subprocess.check_output(['sudo', 'ovs-vsctl', 'show'])      
    
    return ports 
 #ports = subprocess.check_output(['sudo', 'ovs-ofctl', 'dump-ports-desc', bridge])


#Delete (Delete The Port from Bridge)
def delete_port(bridge, port):
        delete = subprocess.call(['sudo', 'ovs-vsctl', 'del-port', bridge, port])

#Update (Update the Port for Type)
def update_port(port,tp):
    update = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'Interface', port, tp])
######################################################################################

#Create (Bridge with Port and VLAN)
def add_VLAN(bridge, vlan, tag, tp):
           vlan = subprocess.call(['sudo', 'ovs-vsctl','add-port', bridge, vlan, tag, '--' , 'set', 'interface', vlan, tp])

#Read (Read VLAN)
def get_VLAN():
    
    pr = subprocess.check_output(['sudo', 'ovs-vsctl', 'show'])

    return pr

#Update (Update Tag)
def update_vlan(port, tag):
    update_vlan = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'port', port, tag])

#DELETE (VLAN)
def delete_vlan(bridge, vlan):
    delete_vlan = subprocess.call(['sudo', 'ovs-vsctl', 'del-port', bridge, vlan])
