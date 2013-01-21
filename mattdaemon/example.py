#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
	Please note, I am well aware this is a very bare-bones example.
	That's what I intended it to be! I'm not using optparse, or anything
	related because it's very simple to check for start/stop/whatever,
	and respond accordingly. You, however, can easily do that.
"""

# So we can iterate through args.
import sys
# Matt Daemon's class
import mattdaemon

# This is what you have to do to daemonize stuff.
# Easy-peasy! Just override Daemon.run() and go!
class MyDaemon(mattdaemon.daemon):
	def run(self):
		from my.project import main
		main()

if __name__ == "__main__":
	args = {
		"pidfile": "/tmp/example-daemon.pid",
		"root": False # does this script require root?
	}
	daem = MyDaemon(**args) # alternatively: MyDaemon("/tmp/example-daemon.pid")

	for arg in sys.argv[1:]: # not including script name
		arg = arg.lower()
		if arg in ('-v', '--version'):
			print 'Matt Daemon (Example): v1.2_3.4'

		elif arg in ('-h', '--help'):
			# You can come up with a better help block I'm sure.
			print 'python', sys.argv[0], 'start|stop|restart|status'

		elif arg in ('start'):
			daem.start()

		elif arg in ('start-no-daemon'):
			# For easy debugging.
			daem.start(daemonize=False)

		elif arg in ('stop'):
			daem.stop()

		elif arg in ('restart'):
			daem.restart()

		elif arg in ('status'):
			if daem.status():
				print 'matt-daemon currently running! :)'
			else:
				print 'matt-daemon not running! :('

		elif arg in ('--requires-root'):
			# Just ignore this, since it's for the superuser check.
			continue

		else:
			print 'Unknown arg:', arg