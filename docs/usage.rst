Usage
=====

.. _pypi: https://pypi.python.org/pypi/mattdaemon
.. |br| raw:: html
    
    <br />

Install & setup
---------------

What's the point in an awesome module (which this is!) if you can't use it? Nothing, that's what!

mattdaemon is on `pypi`_, so you just have to ``pip install mattdaemon``, and you're good to ``import mattdaemon``.

Setup
^^^^^

mattdaemon is fairly simple to setup, all you have to do is subclass the ``mattdaemon.daemon.daemon`` (usable as ``mattdaemon.daemon``) class, and override the ``run()`` method.

Here is how you'd make a simple daemon instance.

.. code-block:: python
    
    import mattdaemon

    class MyDaemon(mattdaemon.daemon):
        def run(self):
            # ... do something ...

    # /tmp/my-daemon.pid is our PID file.
    daem = MyDaemon("/tmp/my-daemon.pid")

Working with the daemon
-----------------------

.. note::
    In these examples, ``daem`` refers to the instance of the MyDaemon class, demonstrated above.

.. note::
    Most of these are fairly simple to grasp; there isn't a dying need to document them, it's just nice to have.

start
^^^^^
Use this to start and daemonize your app.

.. code-block:: python
    
    daem.start()

    # start without daemonizing (stay in the front)
    daem.start(daemonize=False)

stop
^^^^

.. code-block:: python

    if daem.status():
        daem.stop()

restart
^^^^^^^
.. note::
    This literally just calls ``stop()`` and ``start()``, in that order.

.. code-block:: python

    if daem.status():
        daem.restart()

status
^^^^^^
This will return a ``True`` or ``False`` value based on whether or not the daemon process is currently running.

.. code-block:: python

    if daem.status():
        print 'daemon currently running!'
    else:
        print 'daemon not running!'

run
^^^
.. note:: python
    You don't actually call this; it's called by the ``start()`` method.

This is the method you override to get your daemon calling what you want it to call.

.. code-block:: python

    import mattdaemon

    class MyDaemon(mattdaemon.daemon):
        def run(self):
            # ...

Daemonizing your app
--------------------
.. note::
    These are just some good ideas to keep in mind when creating your app with mattdaemon.

There is no std*
^^^^^^^^^^^^^^^^
Why would there be? Your daemon will be running in the background. If you need the user to enter information, perhaps in a loop, you'll have to look for other ways of doing that.

By default, ``sys.stdin``, ``sys.stdout`` and ``sys.stderr`` are all redirected to ``/dev/null``, they're useless now.

What does this mean? If you want to log anything, you'll need to use a dedicated logger, or provide a log file to your daemon instance (example below).

.. code-block:: python
    
    kw = {
        "pidfile": "/tmp/my-daemon.pid",
        "stdin": "/dev/null", # since we don't need it
        "stdout": "/tmp/my-daemon.log",
        "stderr": "/tmp/my-daemon.log"
    }
    daem = MyDaemon(**kw)
    # daem.start(), whathaveyou

Don't assume your working dir
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Due to how daemonization works, the working directory is changed to ``/``, the root of the file system.
Because of this, you can't assume any required files are relative, since they might not be.

.. code-block:: python

    # Relative, bad!
    with open('relative/file', 'rb') as f:
        # ...

    # Absolute, good!
    with open('/some/absolute/file', 'rb') as f:
        # ...

To root or not to root
^^^^^^^^^^^^^^^^^^^^^^
.. note::
    The default for the root check is ``False``; as in, no, we don't require root.

mattdaemon understands you, as well as your app. Careless users often run things with a higher privilege than they need. Do you need root to write some files to temp, or serve data on a high port? **Nope**. Do people do it anyway? They sure do!

Due to this, there is a built in root check. You can either tell the user that they **do** require root, or that they **don't** (which, to be fair, you should be aiming for anyway). Why yes or no? If you don't need root, you shouldn't allow it. If you **do** need root, you should require it, since it will be needed at one point or another.

Root checks are simple, and can be controlled like such (with the ``root`` keyword):

.. code-block:: python
    
    # Yes, we need root!
    daem = MyDaemon("/tmp/my-daemon.pid", root=True)

By default, the check also requires ``--requires-root`` to be in the arguments passed, so that the user acknowledges the use of root. This might not be what you want, so you can easily disable that, with the ``root_chk_argv`` keyword.

.. code-block:: python
    
    # Yes, we need root!
    # No, we don't care about --requires-root
    daem = MyDaemon("/tmp/my-daemon.pid", root=True, root_chk_argv=False)

Handling SIGTERM
^^^^^^^^^^^^^^^^
.. warning::
    This only works in POSIX compliant operating systems, since it uses signals, and Windows doesn't.

If you do anything with resources, be it an open port, file, network request, you should handle SIGTERM.

.. code-block:: python

    import signal

    def my_handler(signum, frame):
        print 'Received signal', signum, 'cleaning up resources to exit'
        my_resource.close()
        my_socket.close()
        print 'done..'

    # Register the handler.
    signal.signal(signal.SIGTERM, my_handler)
