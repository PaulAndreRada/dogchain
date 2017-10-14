import hashlib
import json
from textwrap import dedent
from time import time 
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object): 
    
    # create the constructor 
    def __init__(self):
        # create the chain array
        self.chain = []
        # create the transaction array
        self.current_transactions = [] 

        # create the genesis block
        self.new_block(previous_hash=1, proof=100)


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
