=================
`crashlog` README
=================
:Date: $Date$
:Author: Miki Tebeka <miki.tebeka@gmail.com>

What?
=====
`carshlog` is a simple utility the reports crashes to your application via email
and log file

How?
====
Either use `import crashlog` at the top of your application or run 
`python -m crashlog`.

Configuration
-------------
Currently you'll need to change the default values in `crashlog.py`:

* `_LOG_FILE`
* `_MAIL_TO`
* All the section below `if gethostname() != "production-machine":`

Where?
======
https://developer.berlios.de/projects/crashlog/

Who?
====
Just me_ currently, however if you have the time and energy ...


.. _me: mailto:miki.tebeka@gmail.com


.. comment: vim:ft=rst spell
