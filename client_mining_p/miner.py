import hashlib
import requests

import sys
import json

# def hash(self, block):
#     string_object = json.dumps(block, sort_keys = True)
#     block_string = string_object.encode()

#     raw_hash = hashlib.sha256(block_string)
#     hex_hash = raw_hash.hexdigest()

#     return hex_hash

def proof_of_work(block):
    print(block)
    block_string = json.dumps(block, sort_keys = True)
    proof = 0

    while not valid_proof(block_string, proof):
        proof += 1
    return proof

def valid_proof(block_string, proof):
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://127.0.0.1:5000/"

    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    coins = 0

    while True:
        r = requests.get(url=node + "/last_block")
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break
        print("finding proof...")
        new_proof = proof_of_work(data)
        print("proof found")
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        if data["message"] == "New Block Forged":
            coins += 1
            print(coins)
        else:
           print(data["message"])

