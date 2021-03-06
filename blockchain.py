import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

class Blockchain(object): 
    
    # create the constructor 
    def __init__(self):
        # create the chain array
        self.chain = []
        # create the transaction array
        self.current_transactions = [] 
        # set additional nodes, to track other http connections
        self.nodes = set()

        # create the genesis block
        self.new_block(previous_hash=1, proof=100)

    
    # Registers all the connected nodes in a nodes array
    def register_node( self, address): 
        """ 
        Add a new node to the list of nodes
        
        :param address: <str> Address of node. eg. 'http://192.168.0.5:5000'
        :return: None
        """ 
        
        # parse the URL and place it in the nodes array
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain): 
        """
        Determine if a given blockchain is valid
        
        :param chain: <list> A Blockchain
        :return: <bool> True if valid, False if not
        """
        
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print(f"\n----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                # Break the chain, the hash has been corropted
                return false

            # Check that the proof of work is correct
            if not self.valid_proof(last_block['proof'], blook['proof']):
                # Break the chain, the proof has been corropted
                return false
            
            # Make the new last block result be this block ( to jump to the next, next iteration )
            last_block = block
            # Go to the next index in the chain
            current_index += 1
            
        # it's a valid chain,
        return True

    def resolve_conflicts(self): 

        """
        This is out Consensus Algorithm, it resolves conflics
        by replacing our chain with he longest one in the network. 

        It technically just updates all the chains that are shorter
        than the one that created the latest block
        
        :return: <bool> True if our chain was replaced, False if not
        """
        
        neighbours = self.nodes
        new_chain = None
        
        # We're only looking for chains from all the nodes in our network
        # this should be the next step to change
        max_length = len(self.chain)
        
        # Grab and verify the chains from all the nodes in the network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            
            # if the response is successful, grab the chain and it's length
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                # Check if the length is longer and the chain is valid 
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain: 
            self.chain = new_chain
            return True
        
        return False

    # create the method for a new block
    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        
        :param proof: <int> the proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> hash of previous Block
        :return <dict> New Block
        """
        
        # creates a new block and adds it to the chain
        block = { 
            'index': len(self.chain) + 1, 
            'timestamp': time(), 
            'transactions': self.current_transactions, 
            'proof': proof, 
            'previous_hash': previous_hash or self.hash(self.chain[-1]), 
        }

        # Reset the current list of transactions 
        # its a class paul, remember it's part of the contructor scope, not js
        self.current_transactions = []
        
        # add the new block to the chain & return it in order to chain the command 
        self.chain.append(block)
        return block



    # create the method for a transaction
    def new_transaction(self, sender, recipient, amount): 

        """ 
        Creates a new transaction to go into the next mined Block
        
        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the block that will hold this transaction
        """
        
        # Add the transaction into the list of the last transaction
        self.current_transactions.append({ 
          'sender': sender, 
          'recipient': recipient, 
          'amount': amount,
       })

        # Adds a new transaction to the list of transactions
        # in the old last block created (the new one)
        return self.last_block['index'] + 1


    @property
    def last_block(self):
        # just return the last block when this method is called
        return self.chain[-1]


    @staticmethod
    def hash(block):
        # Hashes a Block 
        """ 
        Creates a SHA-256 hash of a Block
        
        :param block: <dict> Block
        :return: <str>
        """
        
        # Make sure the Dictionary is Ordered, or we'll have inconsistent hashes
        # this part needs more breaking down
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm: 
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        
        :param last_proof: <int> 
        :return: <int>
        """
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
            
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof: does hash(last_prof, proof) contain 4 leading zeroes?
        
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> true if correct, false if not. 
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# instatiate our node
app = Flask(__name__)             
    
# Generate a globally unique address for this node 
node_identifier = str(uuid4()).replace('-', '') 
 
# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine(): 
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier, 
        amount=1,
    )

    # Forge a new Block by adding it to the chain
    block = blockchain.new_block(proof)

    response = { 
        'message': "New Block Forged", 
        'index': block['index'],
        'transactions': block['transactions'], 
        'proof': block['proof'], 
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200



@app.route('/transactions/new', methods=['POST'])
def new_transactions():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'} 
    return jsonify(response), 201


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "We'll add a new transaction"

@app.route('/chain', methods=['GET']) 
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register',methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    # is this a base case?
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    # I think this is recursive, i confus...
    for node in nodes:
        blockchain.register_node(node)

    response = { 
        'message': 'New nodes have been added', 
        'total_nodes': list(blockchain.nodes), 
    }
    
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus(): 
    replaced = blockchain.resolve_conflicts()
    
    if replaced: 
        response = { 
            'message': 'Our chain was replaced', 
            'new_chain': blockchain.chain
    }
    else: 
        response = {
            'message': 'Our chain was replaced', 
            'new_chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)

