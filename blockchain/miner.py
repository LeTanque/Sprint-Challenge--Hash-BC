import hashlib
import requests
import json

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


# def hash(self, block):
#     string_object = json.dumps(block, sort_keys=True)
#     block_string = string_object.encode()
#     raw_hash = hashlib.sha256(block_string)
#     hex_hash = raw_hash.hexdigest()
#     return hex_hash


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """
    start = timer()
    # rcv and sort
    last_proof_string = json.dumps(last_proof, sort_keys=True)

    print("Searching for next proof")
    # Start the search here
    proof = 1076306

    cash = {}

    while valid_proof(last_proof_string, proof) is False:
        proof += 1

    # proof found
    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_proof, proof):
    # Validates the Proof:  Multi-ouroborus:
    #
    # Do the last six characters of the hash of the last proof 
    # match the first six characters of the hash of the new proof?
    #
    # IE:  last_hash: ...AE9123456, new hash 123456E88...
    # proof_string = str(proof)
    guess_last = f'{last_proof}'.encode()
    guess_last_proof = hashlib.sha256(guess_last).hexdigest()

    guess = f'{proof}'.encode()
    guess_proof = hashlib.sha256(guess).hexdigest()

    return guess_last_proof[-6:] == guess_proof[0:6]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        print('data - last proof from the server: ', data)
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}
        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
