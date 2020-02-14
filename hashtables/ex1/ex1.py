#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_retrieve,)


def get_indices_of_item_weights(weights, length, limit):
    print('limit: ', limit)
    print('length: ', length)
    print('weights: ', weights)

    # instantiate the hash table
    ht = HashTable(limit)


    for i_len in range(length):
        # use ht as the table, find value coorresponding key ()
        val = hash_table_retrieve(ht, (limit - weights[i_len]))
        
        hash_table_insert(ht, weights[i_len], i_len)
        if val is not None:
            if i_len > val:
                print_answer([i_len, val])
            else:
                print_answer([val, i_len])



def print_answer(answer):
    print('answer: ', answer[0], answer[1])
    if answer is not None:
        print(f"({answer[0]} {answer[1]})")
    else:
        print("None")
