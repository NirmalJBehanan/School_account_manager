import hashlib
import json
from time import time
from django.core.serializers.json import DjangoJSONEncoder
from .models import BlockchainRecord

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, cls=DjangoJSONEncoder, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()

    @classmethod
    def from_record(cls, record):
        block = cls(record.index, record.timestamp, record.data, record.previous_hash)
        block.hash = record.hash
        return block

class Blockchain:
    def __init__(self):
        if not BlockchainRecord.objects.exists():
            self.create_genesis_block()
        self.chain = [Block.from_record(record) for record in BlockchainRecord.objects.all()]

    def create_genesis_block(self):
        genesis_block = Block(0, time(), {"message": "Genesis Block"}, "0")
        self._save_block_to_db(genesis_block)
        return genesis_block

    def get_latest_block(self):
        return self.chain[-1] if self.chain else None

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_index = previous_block.index + 1
        new_block = Block(new_index, time(), data, previous_block.hash)
        self._save_block_to_db(new_block)
        self.chain.append(new_block)
        return new_block

    def _save_block_to_db(self, block):
        BlockchainRecord.objects.create(
            index=block.index,
            timestamp=block.timestamp,
            data=block.data,
            previous_hash=block.previous_hash,
            hash=block.hash
        )

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_all_blocks(self):
        return [
            {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "hash": block.hash,
                "previous_hash": block.previous_hash
            }
            for block in self.chain
        ] 