from flask import Flask, jsonify
import subprocess

#Create (Bridge with Port)
def add_port(bridge, port):
           add = subprocess.call(['sudo', 'ovs-vsctl','add-br', bridge, '--', 'add-port', bridge, port])

#Read  
def get_ports(bridge):

  ports = subprocess.check_output(['sudo', 'ovs-ofctl', 'dump-ports-desc', bridge])
  return ports

#Delete (Delete The Port from Bridge)
def delete_port(bridge, port):
        delete = subprocess.call(['sudo', 'ovs-vsctl', 'del-port', bridge, port])

#Update (Update the Port for Type)
def update_port(bridge, port, config):
    
     update = subprocess.call(['sudo', 'ovs-ofctl', 'mod-port', bridge, port, config])

######################################################################################

#Create (Bridge with VLAN)
def add_VLAN(bridge, vlan, tag, tp):
           vlan = subprocess.call(['sudo', 'ovs-vsctl','add-port', bridge, vlan, tag, '--' , 'set', 'interface', vlan, tp])

#Read (Read VLAN)
def get_vlan():
    
    vlan = subprocess.check_output(['sudo', 'ovs-vsctl', 'show'])

    return vlan

#Update (Update Tag)
def update_vlan(vlan, tag):
    
    update_vlan = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'port', vlan, tag])

#DELETE (VLAN)
def delete_vlan(bridge, vlan):
    
    delete_vlan = subprocess.call(['sudo', 'ovs-vsctl', 'del-port', bridge, vlan])

#######################################################################

#Create (Port and VLAN)
def add_PortVLAN(port, tag):
    
    vlan = subprocess.call(['sudo', 'ovs-vsctl','set', 'port', port, tag])

#Update (Update Tag)
def update_portvlan(port, tag):
    
    update_vlan = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'port', port, tag])

#DELETE (Port Tag)
def delete_portvlan(port, tag):
    
    delete_vlan = subprocess.call(['sudo', 'ovs-vsctl', 'remove', 'port', port, 'tag', tag])

#Read (Read Port VLAN)
def get_portvlan():

    portvlan = subprocess.check_output(['sudo', 'ovs-vsctl', 'show'])

    return portvlan
