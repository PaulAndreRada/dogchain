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

</br>
If any of those don't work you might be missing Xcode's command line tools, [here's some help](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos)

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
This shows you the full chain ( it's just one chain for now, the consensus algorithm is being buggy )

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

Thats pretty much it...extreamely simplified. 
