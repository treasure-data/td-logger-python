td-logger: logging library for Treasure Data Cloud
=================================================

Setup
-----

Before using this logging handler, td-agent must be properly configured at the
localhost. Please confirm these settings are in your
/etc/td-agent/td-agent.conf.

    ## built-in TCP input
    <source>
      type tcp
    </source>

    # Treasure Data output
    # match events whose tag is td.DATABASE.TABLE
    <match td.*.*>
      type tdlog
      apikey YOUR_API_KEY
    </match>

For more information, please look at the documentation.

* http://docs.treasure-data.com/

Install
-------

    $ easy_install td-logger

or

    $ pip install td-logger

Usage
-----

Check out the tests folder for more samples.

    import logging
    from tdlog import logger

    logging.basicConfig(level=logging.INFO)
    l = logging.getLogger('td_logger.test')
    l.addHandler(logger.TreasureDataHandler())

    l.info('Some message')
    js = { "semicolon" : ";", "at" : "@" }
    l.info(js)

This will throw the log entries to the local td-agent. And there's an important
point. This logger accepts only 'dict' and 'json string'.

Also, these parameters are logged by default.

* sys_host
* sys_name
* sys_module
* sys_lineno
* sys_levelno
* sys_levelname
* sys_filename
* sys_funcname
* sys_exc_info
* msg

These parameters can be specified at TreasureDataHander constructor.

* host: td-agent host (default: 127.0.0.1)
* port: td-agent port (default: 24224)
* db: td database name (default: log)
* table: td table name (default: default)
* bufmax: buffer size max when td-agent is unavailable (default: 1*1024*1024)
* timeout: network timeout (default: 3.0)

Have fun!

How to Develop
--------------

Following are the way to setup development environment on MacOSX.

    $ sudo easy_install virtualenv
    $ virtualenv --no-site-packages .
    New python executable in ./bin/python
    Installing setuptools............done.
    Installing pip...............done.
    $ source bin/activate
    $ bin/pip install msgpack-python

Running tests

    $ python setup.py test

Special Thanks
--------------

- [Joshua Kuntz](https://github.com/j3kuntz) for the original work
