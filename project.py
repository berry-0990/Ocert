import hashlib
import json
from time import time
from flask import Flask, render_template, request

# Define Block class
class Block:
    def _init_(self, index, previous_hash, timestamp, document_hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.document_hash = document_hash

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "document_hash": self.document_hash
        }

# Function to hash the block
def hash_block(block):
    block_string = json.dumps(block.to_dict(), sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

# Function to create a new block
def create_block(previous_block, document_hash):
    index = previous_block.index + 1
    timestamp = time()
    return Block(index, hash_block(previous_block), timestamp, document_hash)

# Function to create the genesis block
def create_genesis_block():
    return Block(0, "0", time(), "genesis_document_hash")

# Function to verify the document in the blockchain
def verify_document(document_hash, blockchain):
    for block in blockchain:
        if block.document_hash == document_hash:
            return True
    return False

# Create the Flask app
app = Flask(__name__)

# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]

@app.route('/')
def index():
    return render_template('hackathon.html')

# Route to add a document to the blockchain
@app.route('/add_document', methods=['POST'])
def add_document():
    # Get the document from the textarea
    document_content = request.form.get('document')
    
    if not document_content:
        return "No document content provided!", 400

    # Compute the document hash
    document_hash = hashlib.sha256(document_content.encode()).hexdigest()

    # Create and add a new block
    new_block = create_block(blockchain[-1], document_hash)
    blockchain.append(new_block)

    return "Document added to the blockchain!"

# Route to verify the document
@app.route('/verify_document', methods=['POST'])
def verify():
    # Get the document from the textarea
    document_content = request.form.get('document')
    
    if not document_content:
        return "No document content provided!", 400

    # Compute the document hash
    document_hash = hashlib.sha256(document_content.encode()).hexdigest()

    # Verify the document in the blockchain
    is_verified = verify_document(document_hash, blockchain)

    if is_verified:
        return "The document is verified and present in the blockchain."
    else:
        return "The document is not verified or not present in the blockchain."

if __name__ == '__main__':
    app.run(debug=True) 