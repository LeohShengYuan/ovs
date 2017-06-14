#!/flask/bin/python
from flask import Flask, jsonify, request, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth
import lists

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
    return make_response(jsonify({'error': 'unauthorized access'}), 403)

#Read
@ovs.route('/ovs/api/read', methods=['GET'])
@auth.login_required
def get_port():
    
    return lists.get_ports()

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
           # 'type': request.json.get('type', "internal")
}
    return jsonify({bridge: brarray}), 201
   #return jsonify({'bridge': bridge, 'port': port}), 201      

#Update
@ovs.route('/ovs/api/update/<port>', methods=['PUT'])
@auth.login_required
def update_port(port):
    tp = request.json['type']
    lists.update_port(port, tp)
    return jsonify({'port': port,'type': tp})

#Delete
@ovs.route('/ovs/api/delete/<port>', methods=['DELETE'])
@auth.login_required
def delete_port(port):

    bridge=request.json['bridge']
    lists.delete_port(bridge, port)
    return jsonify({'Result': True})

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
    return lists.get_VLAN()

#Update (VLAN)
@ovs.route('/ovs/api/update/tag/<port>', methods=['PUT'])
@auth.login_required
def update_vlan(port):
    tag=request.json['tag']
    lists.update_vlan(port, tag)
    return jsonify({'port': port, 'tag': tag})

#DELETE (VLAN)
@auth.login_required
@ovs.route('/ovs/api/delete/vlan/<vlan>', methods=['DELETE'])
def delete_vlan(vlan):
    bridge=request.json['bridge']
    lists.delete_vlan(bridge, vlan)
    return jsonify({'Result': True})

    
@ovs.errorhandler(404)

def not_found(error):
        return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__== '__main__':
        ovs.run(debug=True)
""" 
#Read
@ovsclient.route('/ovs/api/read', methods=['GET'])
def get_port():
    
    return lists.get_ports()

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
    return lists.get_VLAN()

#Update (VLAN)
@ovsclient.route('/ovs/api/update/tag/<port>', methods=['PUT'])
def update_vlan(port):
    tag=request.json['tag']
    lists.update_vlan(port, tag)
    return jsonify({'port': port, 'tag': tag})

#DELETE (VLAN)
@ovsclient.route('/ovs/api/delete/vlan/<vlan>', methods=['DELETE'])
def delete_vlan(vlan):
    bridge=request.json['bridge']
    lists.delete_vlan(bridge, vlan)
    return jsonify({'Result': True})
"""
