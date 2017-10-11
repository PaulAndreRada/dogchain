
class Blockchain(object): 
    
    # create the constructor 
    def __init__(self):
        # create the chain array
        self.chain = []
        # create the transaction array
        self.current_transactions = [] 

    # create the method for a new block?
    def new_block(self):
        # creates a new block and adds it to the chain
        pass


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
        pass

    @property
    def las_block(self):
        # Returns the last Block in the chain
        pass
