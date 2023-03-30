from flask import Flask, jsonify, request, render_template
from web3 import Web3
from web3.auto import w3
import json

class Blockchain:
    	def __init__(self, url):
            self.web3 = Web3(Web3.HTTPProvider(url))
            abi = json.loads(""" [
                    {
                        "inputs": [
                            {
                                "internalType": "uint256",
                                "name": "id",
                                "type": "uint256"
                            },
                            {
                                "internalType": "string",
                                "name": "name",
                                "type": "string"
                            },
                            {
                                "internalType": "string",
                                "name": "lastname",
                                "type": "string"
                            },
                            {
                                "internalType": "uint256",
                                "name": "gpax",
                                "type": "uint256"
                            },
                            {
                                "internalType": "bool",
                                "name": "flag",
                                "type": "bool"
                            }
                        ],
                        "name": "addStudent",
                        "outputs": [],
                        "stateMutability": "nonpayable",
                        "type": "function"
                    },
                    {
                        "inputs": [
                            {
                                "internalType": "uint256",
                                "name": "id",
                                "type": "uint256"
                            }
                        ],
                        "name": "deleteStudent",
                        "outputs": [],
                        "stateMutability": "nonpayable",
                        "type": "function"
                    },
                    {
                        "inputs": [
                            {
                                "internalType": "uint256",
                                "name": "id",
                                "type": "uint256"
                            },
                            {
                                "internalType": "string",
                                "name": "name",
                                "type": "string"
                            },
                            {
                                "internalType": "string",
                                "name": "lastname",
                                "type": "string"
                            },
                            {
                                "internalType": "uint256",
                                "name": "gpax",
                                "type": "uint256"
                            },
                            {
                                "internalType": "bool",
                                "name": "flag",
                                "type": "bool"
                            }
                        ],
                        "name": "editStudent",
                        "outputs": [],
                        "stateMutability": "nonpayable",
                        "type": "function"
                    },
                    {
                        "inputs": [],
                        "name": "getAllStudents",
                        "outputs": [
                            {
                                "internalType": "uint256[]",
                                "name": "",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "string[]",
                                "name": "",
                                "type": "string[]"
                            },
                            {
                                "internalType": "string[]",
                                "name": "",
                                "type": "string[]"
                            },
                            {
                                "internalType": "uint256[]",
                                "name": "",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "bool[]",
                                "name": "",
                                "type": "bool[]"
                            }
                        ],
                        "stateMutability": "view",
                        "type": "function"
                    },
                    {
                        "inputs": [
                            {
                                "internalType": "uint256",
                                "name": "id",
                                "type": "uint256"
                            }
                        ],
                        "name": "getStudent",
                        "outputs": [
                            {
                                "internalType": "string",
                                "name": "",
                                "type": "string"
                            },
                            {
                                "internalType": "string",
                                "name": "",
                                "type": "string"
                            },
                            {
                                "internalType": "uint256",
                                "name": "",
                                "type": "uint256"
                            },
                            {
                                "internalType": "bool",
                                "name": "",
                                "type": "bool"
                            }
                        ],
                        "stateMutability": "view",
                        "type": "function"
                    }
                ]""") 
            abi_address = ("0xf34DC8F14A0894Ecde39DB8399Bd04d0daFAeeC3")
            self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
            self.contract = self.web3.eth.contract(address=abi_address, abi = abi)   

app = Flask(__name__)
blockchain = Blockchain("http://127.0.0.1:8545")

@app.route('/')
def index():
    return render_template ('web.html')

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    result = blockchain.functions.getStudent(id).call()
    student = {
        'name': result[0],
        'lastname': result[1],
        'gpax': result[2],
        'flag': result[3]
    }
    return jsonify(student)

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    id = data['id']
    name = data['name']
    lastname = data['lastname']
    gpax = data['gpax']
    flag = data['flag']
    blockchain.functions.addStudent(id, name, lastname, gpax, flag).transact()
    return jsonify({'message': 'Student added'})

@app.route('/students/int:id', methods=['PUT'])
def edit_student(id):
    data = request.get_json()
    name = data['name']
    lastname = data['lastname']
    gpax = data['gpax']
    flag = data['flag']
    tx_hash = blockchain.functions.editStudent(id, name, lastname, gpax, flag).transact()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return jsonify({'tx_hash': tx_hash.hex()})

@app.route('/students/int:id', methods=['DELETE'])
def delete_student(id):
    tx_hash = blockchain.functions.deleteStudent(id).transact()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return jsonify({'tx_hash': tx_hash.hex()})

if __name__ == "__main__":
    app.run(debug=True)