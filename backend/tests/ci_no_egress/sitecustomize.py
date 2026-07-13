"""Process-wide loopback-only socket policy for ordinary CI test commands."""
from __future__ import annotations

import ipaddress
import socket


_original_connect = socket.socket.connect
_original_connect_ex = socket.socket.connect_ex
_original_create_connection = socket.create_connection
_original_getaddrinfo = socket.getaddrinfo
_original_sendto = socket.socket.sendto


def _host(address) -> str:
    return str(address[0] if isinstance(address, tuple) else address).strip().lower()


def _loopback(address) -> bool:
    host = _host(address)
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _blocked(address) -> RuntimeError:
    return RuntimeError(f"CI egress blocked for non-loopback destination: {_host(address)}")


def _connect(sock, address):
    if not _loopback(address):
        raise _blocked(address)
    return _original_connect(sock, address)


def _connect_ex(sock, address):
    if not _loopback(address):
        raise _blocked(address)
    return _original_connect_ex(sock, address)


def _create_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, *, all_errors=False):
    if not _loopback(address):
        raise _blocked(address)
    return _original_create_connection(address, timeout, source_address, all_errors=all_errors)


def _getaddrinfo(host, *args, **kwargs):
    if host is not None and not _loopback((host, 0)):
        raise _blocked((host, 0))
    return _original_getaddrinfo(host, *args, **kwargs)


def _sendto(sock, data, *args):
    address = args[-1] if args else None
    if address is not None and not _loopback(address):
        raise _blocked(address)
    return _original_sendto(sock, data, *args)


socket.socket.connect = _connect
socket.socket.connect_ex = _connect_ex
socket.create_connection = _create_connection
socket.getaddrinfo = _getaddrinfo
socket.socket.sendto = _sendto
