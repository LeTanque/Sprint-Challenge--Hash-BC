import hashlib
import requests
import json

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof):
    start = timer()
    timeout = random.randrange(4, 10)
    # rcv and sort
    # last_last_proof = json.dumps(last_proof, sort_keys=True)

    print(f" \n> Searching for next proof. Timeout in {timeout}s")
    # Start the search here

    cash = {}

    proof = random.randrange(1, 99999) + random.random()
    print('proof in POW: ', proof)

    while valid_proof(last_proof, proof) is False:
        proof += random.randrange(1, 10)
        if timer() - start > 12:
            proof = 0
            break

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
        node2 = sys.argv[1]
    else:
        node2 = "https://lambda-coin-test-1.herokuapp.com/api"

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
        # r = requests.get(url=node + "/last_proof")
        r2 = requests.get(url=node2 + "/last_proof")
        try:
            data = r2.json()
            print('Last proof ', data)
        except:
            print("Server down, try again please", r2)
            r2 = None

        while r2 is not None:
            data = r2.json()
            print(' ', r2)

            new_proof = proof_of_work(data.get('proof'))

            post_data = {"proof": new_proof,
                        "id": id}

            print('post_data: ', post_data)
            if post_data["proof"] is 0:
                print("> XXX took too long XXX try again \n")
                break

            attempt_mine_response = requests.post(url=node2 + "/mine", json=post_data)
            print(" ", attempt_mine_response, 'attempt_mine_response ')

            if attempt_mine_response is not None:
                response = attempt_mine_response.json()
                if response.get('message') == 'New Block Forged':
                    coins_mined += 1
                    print("Total coins mined: " + str(coins_mined))
                else:
                    print(response.get('message'))
            else:
                print("failed")
