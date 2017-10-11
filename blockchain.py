
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

    # create the method for a transaction?
    def new_transaction(self): 
        # Adds a new transaction to the list of transactions
        pass 

    @staticmethod
    def hash(block):
        # Hashes a Block 
        pass

    @property
    def las_block(self):
        # Returns the last Block in the chain
        pass
