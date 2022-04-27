Changelog
=========

`Unreleased`_
-------------

- allow to disable the message filter.

`1.4.0`_
--------

- warn user if command has wrong syntax.
- warn user if language code is invalid.
- added filter to translate text sent in private (user can set the language to which text will be translated)

`1.3.0`_
--------

- improved commad description.
- try other engines if the default engine fails.

`1.2.0`_
--------

- moved check for correct engine from ``deltabot_init``, to ``deltabot_start`` to allow to change engine after a wrong engine was set.

`1.1.0`_
--------

- allow to translate quoted message (#1)
- quote translated message
- allow to set engine

1.0.0
-----

- initial release


.. _Unreleased: https://github.com/adbenitez/simplebot_translator/compare/v1.4.0...HEAD
.. _1.4.0: https://github.com/adbenitez/simplebot_translator/compare/v1.3.0...v1.4.0
.. _1.3.0: https://github.com/adbenitez/simplebot_translator/compare/v1.2.0...v1.3.0
.. _1.2.0: https://github.com/adbenitez/simplebot_translator/compare/v1.1.0...v1.2.0
.. _1.1.0: https://github.com/adbenitez/simplebot_translator/compare/v1.0.0...v1.1.0
