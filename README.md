matt-daemon
===

Need to daemonize your Python2.7 projects? Matt Daemon has you covered.

Features
---
+ superuser (root) enforcement. Your script either requires it or it doesn't. You choose!
	+ if these checks fail, they exit with a status of __1__.
+ Uses the double-fork magic of UNIX to daemonize.

Dependencies
---
+ [Python2.7](https://python.org)

Notes
---
+ This is designed CLI scripts, because it decouples from the parent environment and all.
+ Includes annoying messages when you use root to run a script.
+ `daemon.start()` and `daemon.stop()` don't print messages. You'll have to decide what to print, if anything.
+ MIT Licensed code, so you're free to do whatever you want with this. Sell it, steal it, improve it, anything at all!

Running / Usage
---
+ Include the script in your project.
+ See the example files for usage.

Author
---
+ [plausibility](https://github.com/plausibility)
