# dogchain 
Paul's overly simplified blockchain, just for fun. </br>
Created using [this tutorial](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)

### Dependencies: 
- Python 3.6+
- pip3
- Flask 0.12.2 
- requests 2.18.4 

</br>



### The easy way to get those dependencies:
Download homebrew:</br>
`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

Download python 3: </br>
`brew install python3`

Download Pip 3: </br>
`brew install pip3`

Download Flask and Requests: </br>
`pip3 install Flask==0.12.2 requests==2.18.4` 


If any of those don't work you might be missing Xcode's command line tools, here's some help:</br> 
https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos
</br>

### How to run the blockchain: 
- Download or clone it
- Open terminal
- go to the dogchain folder
- run `python3 blockchain.py`

</br>


## Play with the blockchain (while it's running): 

### In your browser
`http://localhost:5000/mine` </br>
This mines a new block


`http://localhost:5000/chain` </br>
This shows you the full chain

### In the terminal: 
```
$ curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "d4ee26eee15148ee92c6cd394edd974e",
 "recipient": "someone-other-address",
 "amount": 5
}' "http://localhost:5000/transactions/new"
```
This sends a transaction in the blockchain, you'll see it when you mine the next block ( mine one and check the chain again )
</br>

### To create multiple chains

### in the terminal
`python3 blockchain.py --port=5001`
This starts up another chain in a separate port, mine and get the chain in the same way you would with the first one but use this new port  `http://localhost:5001/mine` & `http://localhost:5000/chain`

### Resolve conflics between chains

### in postman or cURL
Register a node doing a POST request to `http://localhost:5000/nodes/register` with a body of `{ "nodes": ["http://127.0.0.1:5001"] }` to register that new node.

Then do a GET request to `http://localhost:5000/nodes/resolve` to resolve any conflics between the chains by replacing them with the longest chain. You will receive a response with a message if your chain was updated and a new_chain list. 


Thats pretty much it...extreamely simplified, hope you enjoyed. 
