.. cdumay-error documentation master file, created by
   sphinx-quickstart on Thu Feb 22 11:37:27 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome
=======

cdumay-error is a basic library used to standardize exception objects and to
serialize them into json using `marshmallow`.

Example usage
-------------

.. code-block:: python

   >>> from cdumay_error import Error
   >>> raise Error(message="Something wrong happen...")
   Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
   cdumay_error.Error: 1: Something wrong happen...


Serialization
-------------

As marshmallow dump into dict, it's easy to use other libraries to dump

Json serialization
******************

.. code-block:: python

    >>> import os
    >>> from cdumay_error import Error, ErrorSchema
    >>>
    >>> try:
    ...     os.listdir("/path/not/exists")
    ... except FileNotFoundError as exc:
    ...     print(ErrorSchema().dumps(Error(
    ...         code=exc.args[0], message=exc.args[1],
    ...         extra=dict(path="/path/not/exists")
    ...     )).data)
    ...
    {"code": 2, "extra": {"path": "/path/not/exists"}, "msgid": null, "stack": "Traceback (most recent call last):\n  File \"<stdin>\", line 2, in <module>\nFileNotFoundError: [Errno 2] No such file or directory: '/path/not/exists'", "message": "No such file or directory"}

Yaml serialisation
******************

Can use any Yaml lib, we'll use PyYAML(==3.11):

.. code-block:: python

   >>> import yaml
   >>> import os
   >>> from cdumay_error import Error, ErrorSchema
   >>>
   >>> try:
   ...     os.listdir("/path/not/exists")
   ... except FileNotFoundError as exc:
   ...     print(yaml.dump(ErrorSchema().dump(Error(
   ...         code=exc.args[0], message=exc.args[1],
   ...         extra=dict(path="/path/not/exists")
   ...     )).data, default_flow_style=False, default_style=''))
   ...
   code: 2
   extra:
     path: /path/not/exists
   message: No such file or directory
   msgid: null
   stack: "Traceback (most recent call last):\n  File \"<stdin>\", line 2, in <module>\n\
     FileNotFoundError: [Errno 2] No such file or directory: '/path/not/exists'"

.. seealso::

    `marshmallow <http://marshmallow.readthedocs.io/en/latest/index.html>`_
        Simplified object serialization
