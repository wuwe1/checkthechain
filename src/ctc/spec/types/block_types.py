import typing

from . import token_types
from . import binary_types


BlockHash = binary_types.PrefixHexData
TransactionHash = binary_types.PrefixHexData

block_number_names = ['latest', 'earliest', 'pending']
BlockNumberName = typing.Union[
    typing.Literal['latest'],
    typing.Literal['earliest'],
    typing.Literal['pending'],
]

# anything that can be converted to an int without node querying
RawBlockNumber = typing.Union[typing.SupportsRound, binary_types.HexData]

# an int or block number name
StandardBlockNumber = typing.Union[int, BlockNumberName]

# anything that refers to a block number, raw or standard
BlockNumberReference = typing.Union[RawBlockNumber, StandardBlockNumber]

# any reference to a block
BlockReference = typing.Union[BlockNumberReference, BlockHash]


class RawTransaction(typing.TypedDict):
    pass


class Transaction(typing.TypedDict):
    hash: TransactionHash
    block_hash: BlockHash
    block_number: int
    chain_id: binary_types.PrefixHexData
    # from: token_types.Address
    gas: int
    gas_price: int
    input: binary_types.PrefixHexData
    nonce: int
    r: binary_types.PrefixHexData
    s: binary_types.PrefixHexData
    to: token_types.Address
    transaction_index: int
    type: binary_types.PrefixHexData
    v: int
    value: int


class RawBlock(typing.TypedDict):
    pass


class Block(typing.TypedDict):
    number: int
    difficulty: int
    extra_data: binary_types.PrefixHexData
    gas_limit: int
    gas_used: int
    hash: BlockHash
    logs_bloom: binary_types.PrefixHexData
    miner: token_types.Address
    mix_hash: BlockHash
    nonce: binary_types.PrefixHexData
    parent_hash: BlockHash
    receipts_root: binary_types.PrefixHexData
    sha3_uncles: binary_types.PrefixHexData
    size: int
    state_root: binary_types.PrefixHexData
    timestamp: int
    total_difficulty: int
    transactions: typing.Union[list[TransactionHash], list[Transaction]]
    transactions_root: binary_types.PrefixHexData
    uncles: list[BlockHash]

