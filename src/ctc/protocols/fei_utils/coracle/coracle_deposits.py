from __future__ import annotations

import asyncio
import typing

from ctc import evm
from ctc import rpc
from ctc import spec
from . import coracle_spec
from . import coracle_tokens


function_abis = {
    'getDepositsForToken': {
        'inputs': [
            {'internalType': 'address', 'name': '_token', 'type': 'address'}
        ],
        'name': 'getDepositsForToken',
        'outputs': [
            {'internalType': 'address[]', 'name': '', 'type': 'address[]'}
        ],
        'stateMutability': 'view',
        'type': 'function',
    },
}


async def async_get_tokens_deposits(
    tokens: typing.Optional[typing.Sequence[spec.Address]] = None,
    block: typing.Optional[spec.BlockReference] = None,
    provider: spec.ProviderSpec = None,
) -> dict[spec.Address, typing.Tuple[spec.ContractAddress, ...]]:
    """get all deposits of all tokens in pcv"""

    if block is None:
        block = 'latest'
    block = await evm.async_block_number_to_int(block=block, provider=provider)

    # get tokens in pcv
    if tokens is None:
        tokens = await coracle_tokens.async_get_tokens_in_pcv(
            block=block, provider=provider
        )

    # get deposits of each token
    coroutines = []
    for token in tokens:
        coroutine = async_get_token_deposits(
            token=token,
            block=block,
            provider=provider,
        )
        coroutines.append(coroutine)

    # compile into tokens_deposits
    results = await asyncio.gather(*coroutines)
    tokens_deposits = dict(zip(tokens, results))
    return tokens_deposits


async def async_get_token_deposits(
    token: spec.Address,
    block: typing.Optional[spec.BlockNumberReference] = None,
    wrapper: bool = False,
    provider: spec.ProviderSpec = None,
) -> typing.Tuple[spec.ContractAddress, ...]:
    """get list of a token's deposits"""

    if block is None:
        block = 'latest'
    block = await evm.async_block_number_to_int(block=block, provider=provider)

    coracle = coracle_spec.get_coracle_address(wrapper=wrapper, block=block)
    return await rpc.async_eth_call(
        to_address=coracle,
        block_number=block,
        function_abi=function_abis['getDepositsForToken'],
        function_parameters={'_token': token},
        provider=provider,
    )


async def async_get_deposit_token(
    deposit: spec.ContractAddress,
    block: typing.Optional[spec.BlockNumberReference] = None,
    provider: spec.ProviderSpec = None,
) -> spec.Address:
    """get the token address of a deposit"""
    return await rpc.async_eth_call(
        to_address=deposit,
        block_number=block,
        function_name='token',
        provider=provider,
    )

