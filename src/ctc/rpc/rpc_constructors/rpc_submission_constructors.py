from ctc import spec
from .. import rpc_request


def construct_eth_gas_price() -> spec.RpcRequest:
    return rpc_request.create('eth_gasPrice', [])


def construct_eth_accounts() -> spec.RpcRequest:
    return rpc_request.create('eth_accounts', [])


def construct_eth_sign(address, message) -> spec.RpcRequest:
    return rpc_request.create('eth_sign', [address, message])


def construct_eth_sign_transaction(
    from_address,
    data,
    to_address=None,
    gas=None,
    gas_price=None,
    value=None,
    nonce=None,
) -> spec.RpcRequest:

    parameters = {
        'from': from_address,
        'to': to_address,
        'gas': gas,
        'gasPrice': gas_price,
        'value': value,
        'data': data,
        'nonce': nonce,
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}

    return rpc_request.create('eth_signTransaction', [parameters])


def construct_eth_send_transaction(
    from_address: spec.BinaryData,
    data: spec.BinaryData,
    to_address: spec.BinaryData = None,
    gas: spec.BinaryData = None,
    gas_price: spec.BinaryData = None,
    value: spec.BinaryData = None,
    nonce: spec.BinaryData = None,
) -> spec.RpcRequest:
    parameters = {
        'from': from_address,
        'to': to_address,
        'gas': gas,
        'gasPrice': gas_price,
        'value': value,
        'data': data,
        'nonce': nonce,
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}

    return rpc_request.create('eth_sendTransaction', [parameters])


def construct_eth_send_raw_transaction(
    data: spec.BinaryData,
) -> spec.RpcRequest:
    return rpc_request.create('eth_sendRawTransaction', [data])

