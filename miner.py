import hashlib, struct
import json
import sys
import random

UPPER_LIMIT = 0x100000000

def read_json(path):
    file = open(path, 'r')
    the_dict = json.loads(file.read())
    file.close()
    return the_dict

class Block:
    def __init__(self, dict_block):
        if type(dict_block['version']) is int:
            self.version = dict_block['version']
        else:
            self.version = int(dict_block['version'], 16)
        self.prev_block = dict_block['prev_block']
        self.merkle_root = dict_block['merkle_root']
        self.time = int(dict_block['time'], 16)
        self.bits = int(dict_block['bits'], 16)

def get_block(path):
    return Block(read_json(path))

def find_hash(block, start_at=0):
    exp = block.bits >> 24
    mant = block.bits & 0xffffff
    target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
    target_str = target_hexstr.decode('hex')

    print exp
    print mant
    print target_hexstr
    print len(target_str)
    
    nonce = start_at

    while nonce < UPPER_LIMIT:
        header = ( struct.pack("<L", block.version) + block.prev_block.decode('hex')[::-1] +
            block.merkle_root.decode('hex')[::-1] + struct.pack("<LLL", block.time, block.bits, nonce))
        hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
        if nonce % 50000 == 0:
            print(nonce, hash[::-1].encode('hex'))
        if hash[::-1] < target_str:        
            print('Found hash:')
            print(nonce, hash[::-1].encode('hex'))
            break
        nonce += 1

# find_hash(get_block('check_block.json'), 538460000)
# find_hash(get_block('main_block.json'), 3000000000)
nonce = 3060331852
start_at = random.randint(nonce, UPPER_LIMIT)
print 'Starting at ' + str(start_at)
find_hash(get_block('main_block.json'), start_at)
