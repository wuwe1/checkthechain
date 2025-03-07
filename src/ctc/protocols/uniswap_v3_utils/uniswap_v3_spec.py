from __future__ import annotations

import typing
from ctc import evm
from ctc import spec


#
# # addresses
#

tick_lens = '0xbfd8137f7d1516d3ea5ca83523914859ec47f573'
quoter = '0xb27308f9f90d607463bb33ea1bebb41c27ce5ab6'


#
# # abi's
#


_abi_cache: dict[
    str,
    typing.Optional[
        dict[
            str,
            typing.Union[
                spec.FunctionABI,
                spec.EventABI,
            ],
        ]
    ],
] = {
    'pool': None,
    'quoter': None,
    'tick_lens': None,
}


async def _async_load_abi_cache(contract) -> None:

    # ensure cache in empty
    if _abi_cache[contract] is not None:
        return

    # load abi
    if contract == 'pool':
        address = '0x8f8ef111b67c04eb1641f5ff19ee54cda062f163'
    elif contract == 'quoter':
        address = quoter
    elif contract == 'tick_lens':
        address = tick_lens
    else:
        raise Exception('unknown contract')

    # get contract abi
    contract_abi = await evm.async_get_contract_abi(contract_address=address)

    # place in cache
    contract_abi_by_name = {
        entry['name']: entry for entry in contract_abi if 'name' in entry
    }
    _abi_cache[contract] = contract_abi_by_name


async def async_get_function_abi(
    function_name: str, contract: str
) -> spec.FunctionABI:
    await _async_load_abi_cache(contract)
    abi_entry = _abi_cache[contract]
    if abi_entry is None:
        raise Exception('must load abi into cache')
    return typing.cast(spec.FunctionABI, abi_entry[function_name])


async def async_get_event_abi(event_name: str, contract: str) -> spec.EventABI:
    await _async_load_abi_cache(contract)
    abi_entry = _abi_cache[contract]
    if abi_entry is None:
        raise Exception('must load abi into cache')
    return typing.cast(spec.EventABI, abi_entry[event_name])

