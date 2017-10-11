import hashlib
import json

from time import time 
from uuid import uuid4

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

    @property
    def las_block(self):
        # Returns the last Block in the chain
        pass
