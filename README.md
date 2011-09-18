td-loger: logging library for Treasure Data Cloud
=================================================

Setup
-----

Before using this logging handler, td-agent must be properly configured. Please
confirm these settings are in your /etc/td-agent/td-agent.conf.

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

Have fun!
