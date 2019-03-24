#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-bitcoinzero.desktop']),
        (os.path.join(usr_share, 'icons/'), ['icons/electrum-bitcoinzero.png'])
    ]

setup(
    name="Electrum-Bitcoinzero",
    version=version.ELECTRUM_VERSION,
    install_requires=[
        'pyaes>=0.1a1',
        'ecdsa>=0.9',
        'pbkdf2',
        'requests',
        'qrcode',
        'protobuf',
        'dnspython',
        'jsonrpclib-pelix',
        'PySocks>=1.6.6',
    ],
    packages=[
        'electrum_bzx',
        'electrum_bzx_gui',
        'electrum_bzx_gui.qt',
        'electrum_bzx_plugins',
        'electrum_bzx_plugins.audio_modem',
        'electrum_bzx_plugins.cosigner_pool',
        'electrum_bzx_plugins.email_requests',
        'electrum_bzx_plugins.hw_wallet',
        'electrum_bzx_plugins.labels',
        'electrum_bzx_plugins.ledger',
        'electrum_bzx_plugins.trezor',
        'electrum_bzx_plugins.digitalbitbox',
        'electrum_bzx_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_bzx': 'lib',
        'electrum_bzx_gui': 'gui',
        'electrum_bzx_plugins': 'plugins',
    },
    package_data={
        'electrum_bzx': [
            'servers.json',
            'servers_testnet.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum-bitcoinzero'],
    data_files=data_files,
    description="Lightweight Bitcoinzero Wallet",
    author="Bitcoinzero",
    author_email="contact@bitcoinzerox.net",
    license="MIT Licence",
    url="https://bitcoinzerox.net",
    long_description="""Lightweight Bitcoinzero Wallet"""
)
