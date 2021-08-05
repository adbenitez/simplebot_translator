Translator
==========

.. image:: https://img.shields.io/pypi/v/simplebot_translator.svg
   :target: https://pypi.org/project/simplebot_translator

.. image:: https://img.shields.io/pypi/pyversions/simplebot_translator.svg
   :target: https://pypi.org/project/simplebot_translator

.. image:: https://pepy.tech/badge/simplebot_translator
   :target: https://pepy.tech/project/simplebot_translator

.. image:: https://img.shields.io/pypi/l/simplebot_translator.svg
   :target: https://pypi.org/project/simplebot_translator

.. image:: https://github.com/adbenitez/simplebot_translator/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/adbenitez/simplebot_translator/actions/workflows/python-ci.yml

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

🌎 Translator plugin for `SimpleBot`_.

This plugin registers the ``/tr`` command that end-users can use to
translate text. Example: ``/tr en es hello world``.

Install
-------

To install run::

  pip install simplebot-translator

To configure the engine use::

  simplebot db -s simplebot_translator/engine deepl

You may need to install other dependencies to make some engines work, check: https://github.com/UlionTse/translators

Available engines:

- google
- yandex
- bing
- sogou
- baidu
- tencent
- youdao
- alibaba
- deepl

.. _SimpleBot: https://github.com/simplebot-org/simplebot
