from __future__ import annotations

from ctc import evm
from ctc import rpc
from ctc import spec
from . import coracle_spec


async def async_get_tokens_in_pcv(
    block: spec.BlockReference = 'latest',
    wrapper: bool = False,
    provider: spec.ProviderSpec = None,
) -> list[spec.Address]:
    """get list of all tokens in pcv"""

    block = evm.standardize_block_number(block)
    coracle = coracle_spec.get_coracle_address(wrapper=wrapper, block=block)

    return await rpc.async_eth_call(
        to_address=coracle,
        function_name='getTokensInPcv',
        block_number=block,
        provider=provider,
    )


async def async_get_pcv_tokens_symbols(
    tokens: list[spec.ERC20Reference],
    block: spec.BlockNumberReference = 'latest',
    provider: spec.ProviderSpec = None,
) -> dict[spec.ERC20Reference, str]:

    non_usd_tokens = list(
        token for token in tokens if token != coracle_spec.usd_token
    )
    symbols = await evm.async_get_erc20s_symbols(
        tokens=non_usd_tokens,
        provider=provider,
        block=block,
    )
    tokens_symbols = dict(zip(non_usd_tokens, symbols))
    if coracle_spec.usd_token in tokens:
        tokens_symbols[coracle_spec.usd_token] = 'USD'

    return tokens_symbols

