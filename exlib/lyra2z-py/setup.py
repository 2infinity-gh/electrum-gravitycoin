from setuptools import setup, Extension

lyra2z_hash_module = Extension('lyra2z_hash',
                               sources = [
										  'lyra2zmodule.c',
                                          'lyra2z.c',
										  'Sponge.c',
										  'Lyra2.c',
										  'blake.c'],
                               include_dirs=['.'])

setup (name = 'lyra2z_hash',
       version = '0.1.0',
       author_email = 'contact@bitcoinzerox.net',
       author = 'bitcoinzero',
       url = 'https://github.com/BitcoinzeroOfficial',
       description = 'Bindings for Lyra2Z proof of work used by Bitcoinzero',
       ext_modules = [lyra2z_hash_module])

