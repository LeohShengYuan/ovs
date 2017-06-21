#!/flask/bin/python
from flask import Flask, jsonify, request, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth
import lists, re

ovs = Flask(__name__)

#Auth

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'SY':
       return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'Error': 'Unauthorized Access'}), 403)

#Read
@ovs.route('/ovs/api/read/<bridge>', methods=['GET'])
@auth.login_required
def get_port(bridge):
    

    read = re.split('\n', lists.get_ports(bridge))
    
    return jsonify({'Output':read}) 

#Create
@ovs.route('/ovs/api/create/<port>', methods=['POST'])
@auth.login_required
def create_port(port):
    if not request.json or not 'bridge' in request.json:
       abort(400)

    bridge=request.json['bridge']
    lists.add_port(bridge, port)
    brarray = {
            'Bridge': request.json.get('Bridge', bridge),
            'Port': request.json.get('Port', port),
            'Interface': request.json.get('Interface', port)
           
}
    return jsonify({bridge: brarray}), 201


#Update
@ovs.route('/ovs/api/update/<port>', methods=['PUT'])
@auth.login_required
def update_port(port):
    config = request.json['config']
    bridge=request.json['bridge']
    lists.update_port(bridge, port, config)
    
    return jsonify({'bridge':bridge, 'port': port, 'config': config})

#Delete
@ovs.route('/ovs/api/delete/<port>', methods=['DELETE'])
@auth.login_required
def delete_port(port):

    bridge=request.json['bridge']
    lists.delete_port(bridge, port)
    
    return jsonify({'Result': True})

###############################

#Create (Create VLAN)
@ovs.route('/ovs/api/vlan/<vlan>', methods=['POST'])
@auth.login_required
def create_vlan(vlan):

    bridge=request.json['bridge']
    tag=request.json['tag']
    tp = request.json['type']     
    lists.add_VLAN(bridge, vlan, tag, tp)
    
    return jsonify({'bridge': bridge, 'vlan': vlan, 'tag': tag, 'interface': vlan, 'type': tp}), 201


#Read (VLAN)
@ovs.route('/ovs/api/vlan/read', methods=['GET'])
@auth.login_required
def get_vlan():
    
    vlanread = re.split('\n', lists.get_vlan())
    
    return jsonify({'Output':vlanread})
    

#Update (VLAN)
@ovs.route('/ovs/api/update/tag/<vlan>', methods=['PUT'])
@auth.login_required
def update_vlan(vlan):
    
    tag=request.json['tag']
    lists.update_vlan(vlan, tag)
    
    return jsonify({'vlan': vlan, 'tag': tag})

#DELETE (VLAN)
@auth.login_required
@ovs.route('/ovs/api/delete/vlan/<vlan>', methods=['DELETE'])
def delete_vlan(vlan):
    
    bridge=request.json['bridge']
    lists.delete_vlan(bridge, vlan)
    
    return jsonify({'Result': True})

######################################################################

#Create (Create Port VLAN)
@ovs.route('/ovs/api/port/<port>', methods=['POST'])
@auth.login_required
def create_portvlan(port):

    tag=request.json['tag']
    lists.add_PortVLAN(port, tag)

    return jsonify({'port': port, 'tag': tag}), 201

#Update (Port VLAN)
@ovs.route('/ovs/api/update/tag/<port>', methods=['PUT'])
@auth.login_required
def update_portvlan(vlan):
    
    tag=request.json['tag']
    lists.update_vlan(port, tag)
    
    return jsonify({'port': port, 'tag': tag})

#DELETE (Port VLAN)
@auth.login_required
@ovs.route('/ovs/api/delete/port/<port>', methods=['DELETE'])
def delete_portvlan(port):
    
    tag=request.json['tag']
    lists.delete_portvlan(port, tag)
    
    return jsonify({'Result': True})
    
#Read (Port VLAN)
@ovs.route('/ovs/api/port/read', methods=['GET'])
@auth.login_required
def get_portvlan():
   
   pvread = re.split('\n', lists.get_portvlan()) 
   return jsonify({'Output':pvread})


@ovs.errorhandler(404)

def not_found(error):
        return make_response(jsonify({'Error': 'Resource Not Found'}), 404)

@ovs.errorhandler(400)

def bad_request(error):
        return make_response(jsonify({'Error': 'Bad Request'}), 400)

@ovs.errorhandler(500)

def internal_error(error):
        return make_response(jsonify({'Error': 'Internal Server Error'}), 500)


if __name__== '__main__':
        ovs.run(debug=True)
""" 
#Read
@ovsclient.route('/ovs/api/read', methods=['GET'])
def get_port():
    
    read = re.split('\n', lists.get_ports(bridge))
    
    return jsonify({'Output':read})

#Create
@ovsclient.route('/ovs/api/create/<port>', methods=['POST'])
def create_port(port):
    if not request.json or not 'bridge' in request.json:
       abort(400)

    bridge=request.json['bridge']
    lists.add_port(bridge, port)
    brarray = {
            'Bridge': request.json.get('Bridge', bridge),
            'Port': request.json.get('Port', port),
            'Interface': request.json.get('Interface', port),
}
    return jsonify({bridge: brarray}), 201  

#Update
@ovsclient.route('/ovs/api/update/<port>', methods=['PUT'])
def update_port(port):
    
    tp = request.json['type']
    lists.update_port(port, tp)
    
    return jsonify({'port': port,'type': tp})

#Delete
@ovsclient.route('/ovs/api/delete/<port>', methods=['DELETE'])
def delete_port(port):

    bridge=request.json['bridge']
    lists.delete_port(bridge, port)
    
    return jsonify({'Result': True})

#Create (Create VLAN)
@ovsclient.route('/ovs/api/vlan/<vlan>', methods=['POST'])
def create_vlan(vlan):

    bridge=request.json['bridge']
    tag=request.json['tag']
    tp = request.json['type']     
    lists.add_VLAN(bridge, vlan, tag, tp)
    
    return jsonify({'bridge': bridge, 'vlan': vlan, 'tag': tag, 'interface': vlan, 'type': tp}), 201


#Read (VLAN)
@ovsclient.route('/ovs/api/vlan/read', methods=['GET'])
def get_vlan():
    
    vlanread = re.split('\n', lists.get_vlan())
    return jsonify({'Output':vlanread})


#Update (VLAN)
@ovsclient.route('/ovs/api/update/<port>', methods=['PUT'])
def update_port(port):
    
    state = request.json['state']
    bridge=request.json['bridge']
    lists.update_port(bridge, port, state)
    
    return jsonify({'bridge':bridge, 'port': port, 'state': state})

#DELETE (VLAN)
@ovsclient.route('/ovs/api/delete/vlan/<vlan>', methods=['DELETE'])
def delete_vlan(vlan):
    
    bridge=request.json['bridge']
    lists.delete_vlan(bridge, vlan)
    
    return jsonify({'Result': True})

############################################################################################################

#Create (Create Port VLAN)
@ovsclient.route('/ovs/api/port/<port>', methods=['POST'])
def create_portvlan(port):

    tag=request.json['tag']
    lists.add_PortVLAN(port, tag)

    return jsonify({'port': port, 'tag': tag}), 201

#Update (Port VLAN)
@ovsclient.route('/ovs/api/update/tag/<port>', methods=['PUT'])
def update_portvlan(vlan):
    
    tag=request.json['tag']
    lists.update_vlan(port, tag)
    
    return jsonify({'port': port, 'tag': tag})

#DELETE (Port VLAN)
@ovsclient.route('/ovs/api/delete/port/<port>', methods=['DELETE'])
def delete_portvlan(port):
    
    tag=request.json['tag']
    lists.delete_portvlan(port, tag)
    
    return jsonify({'Result': True})

#Read (Port VLAN)
@ovsclient.route('/ovs/api/port/read', methods=['GET'])
def get_portvlan():

   pvread = re.split('\n', lists.get_portvlan())
   
   return jsonify({'Output':pvread})

"""
