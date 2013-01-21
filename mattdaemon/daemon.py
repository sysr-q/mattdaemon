#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based off of code from: www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python
# It's licensed under Public Domain, so we're free to use it.

import sys, os, time, atexit
from signal import SIGTERM 

class RootCheck:
	# The IDs of various accounts.
	# If you're using linux: root=0; it might not in *BSD or others.
	ids = {
		"root": 0
	}

	@staticmethod
	def check(require, check_argv=True):
		if require:
			# If they're not root, tell them to run with root!
			if os.getuid() != RootCheck.ids['root']:
				sys.stdout.write("This script requires root (id={0}), and you're currently id={1}.\n".format(RootCheck.ids['root'], os.getuid()))
				sys.stdout.write("Please re-run the script as root (id={0})".format(RootCheck.ids['root']))
				sys.exit(1)
			# If we're checking argv, 
			if check_argv and '--requires-root' not in sys.argv:
				sys.stdout.write("To run this script, you must append '--requires-root' to the args.\n")
				sys.stdout.write("This is so that you can't say you didn't know that using root is a bad idea.\n")
				sys.stdout.write("Please re-run the script with '--requires-root'.")
				sys.exit(1)
			# Should we berate them? A warning is enough, really.
			sys.stdout.write("[WARNING!] You've run this script as root, which is bad.\n")

		else: # down with root, down with root!
			if os.getuid() == RootCheck.ids['root']:
				sys.stdout.write("This script does not require root, but you've given it that anyway.\n")
				sys.stdout.write("It is very poor practice to run a script with more privilege than it needs.\n")
				sys.stdout.write("Please re-run the script without root access")
				sys.exit(1)


class daemon:
	"""
	A generic daemon class.
	
	Usage: subclass the Daemon class and override the run() method
	"""
	def __init__(self, pidfile, root=False, root_chk_argv=True, stdin="/dev/null", stdout="/dev/null", stderr="/dev/null"):
		"""
		Make our daemon instance.
		pidfile: the file we're going to store the process id in. ex: /tmp/matt-daemon.pid
		root:    does this script require root? True if it does, False if it doesn't. Will be enforced.
		root_chk_argv:  does the script require '--requires-root' in sys.argv to run as root? (usage is good)
		stdin:   where the script gets stdin from. "/dev/null", "/dev/stdin", etc.
		stdout:  where the script writes stdout. "/dev/null", "/dev/stdout", etc.
		stderr:  where the script writes stderr. "/dev/null", "/dev/stderr", etc.
		"""
		# Enforce root usage or non-usage.
		RootCheck.check(root, check_argv=root_chk_argv)
		self.pidfile = pidfile
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
	
	def daemonize(self):
		"""
		do the UNIX double-fork magic, see Stevens' "Advanced
		Programming in the UNIX Environment" for details (ISBN 0201563177)
		http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
		"""
		try:
			pid = os.fork()
			if pid > 0:
				# exit first parent
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #1 failed: {0} ({1})\n".format(e.errno, e.strerror))
			sys.exit(1)
	
		# decouple from parent environment
		os.chdir("/")
		os.setsid()
		os.umask(0)
	
		# do second fork
		try: 
			pid = os.fork()
			if pid > 0:
				# exit from second parent
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #2 failed: {0} ({1})\n".format(e.errno, e.strerror))
			sys.exit(1)
	
		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	
		# write pidfile
		atexit.register(self.delpid)
		pid = str(os.getpid())
		file(self.pidfile,'w+').write("{0}\n".format(pid))
	
	def delpid(self):
		os.remove(self.pidfile)

	def start(self, daemonize=True):
		"""
		Start the daemon
		"""
		# Check for a pidfile to see if the daemon is already running
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if pid:
			message = "pidfile {0} already exist. Daemon already running?\n"
			sys.stderr.write(message.format(self.pidfile))
			sys.exit(1)
		
		if daemonize:
			# Start the daemon
			self.daemonize()
		self.run()

	def stop(self):
		"""
		Stop the daemon
		"""
		# Get the pid from the pidfile
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if not pid:
			message = "pidfile {0} does not exist. Daemon not running?\n"
			sys.stderr.write(message.format(self.pidfile))
			return # not an error in a restart

		# Try killing the daemon process
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError, err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print str(err)
				sys.exit(1)

	def restart(self):
		"""
		Restart the daemon
		"""
		self.stop()
		self.start()

	def status(self):
		"""
		Check if the daemon is currently running.
		Requires procfs, so it will only work on POSIX compliant OS'.
		"""
		# Get the pid from the pidfile
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if not pid:
			return False

		try:
			return os.path.exists("/proc/{0}".format(pid))
		except OSError:
			return False

	def run(self):
		"""
		You should override this method when you subclass Daemon. It will be called after the process has been
		daemonized by start() or restart().
		"""
