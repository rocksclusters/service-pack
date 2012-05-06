# $Id: __init__.py,v 1.4 2012/05/06 05:49:27 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.4  2012/05/06 05:49:27  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:23  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:19  bruno
# get the right commands
#
# Revision 1.14  2010/09/07 23:52:55  bruno
# star power for gb
#
# Revision 1.13  2009/05/01 19:06:58  mjk
# chimi con queso
#
# Revision 1.12  2008/10/18 00:55:49  mjk
# copyright 5.1
#
# Revision 1.11  2008/08/18 21:16:06  mjk
# - Added cols arg to list help (cols=0 means no line wrapping)
# - Added help verb as a rocks help | grep XXX shortcut
#
# Revision 1.10  2008/03/06 23:41:37  mjk
# copyright storm on
#
# Revision 1.9  2007/07/05 17:25:03  mjk
# fix help
#
# Revision 1.8  2007/07/04 01:47:38  mjk
# embrace the anger
#
# Revision 1.7  2007/06/19 16:42:41  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.6  2007/06/07 21:23:04  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.5  2007/05/25 03:12:30  mjk
# - help takes a flag instead of an argument
# - added bash/readline completion
#
# Revision 1.4  2007/05/10 20:37:01  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.3  2007/02/27 01:53:58  mjk
# - run(self, args) => run(self, flags, args)
# - replaced rocks list host xml with more complete code
# - replaced rocks lust node xml with kpp shell (not a command now)
#
# Revision 1.2  2007/02/08 17:31:25  mjk
# Added root check for root-only commands
# Added syslog tracking to record changes to the cluster
#
# Revision 1.1  2006/12/17 20:19:47  mjk
# moving commands around again
#
# Revision 1.3  2006/12/06 23:47:46  mjk
# fix addText call
#
# Revision 1.2  2006/12/06 23:45:11  mjk
# added xxxText methods
#
# Revision 1.1  2006/11/22 02:15:46  mjk
# working version
#


import os
import sys
import string
import rocks.file
import rocks.commands


class Command(rocks.commands.list.command):
	"""The Help Command print the usage of all the registered
	Commands.
	
	<param optional='1' type='string' name='subdir'>
	Relative of Python commands for listing help.  This is used internally
	only.
	</param>
	
	<example cmd='list help'>
	List help for all commands
	</example>
	
	<example cmd='list help subdir=list/host'>
	List help for all commands under list/host
	</example>
	"""

	def run(self, params, args):

		# Because this command is called directly from the rock.py
		# code we need to provide the params argument.  This is the
		# only command where we need to include this argument.
		
		(subdir, cols) = self.fillParams([('subdir', ),
						  ('cols', 80) ],
						 params)
		
		if subdir:
			filepath = os.path.join(rocks.commands.__path__[0],
				subdir)
			modpath  = 'rocks.commands.%s' % \
				string.join(subdir.split(os.sep), '.')
		else:
			filepath = rocks.commands.__path__[0]
			modpath  = 'rocks.commands'
		
		tree = rocks.file.Tree(filepath)
		dirs = tree.getDirs()
		dirs.sort()

		if os.environ.has_key('COLUMNS'):
			cols = os.environ['COLUMNS']
			
		for dir in dirs:
			if not dir:
				continue
				
			module = '%s.%s' % \
				(modpath, string.join(dir.split(os.sep),'.'))
			__import__(module)
			module = eval(module)
			
			try:
				o = getattr(module, 'Command')(None)
			except AttributeError:
				continue
		
			if o.MustBeRoot and not self.isRootUser():
				continue

			# Format the brief usage to fit within the
			# width of the user's window (default to 80 cols)
			
			cmd = string.join(dir.split(os.sep),' ')
			l   = len(cmd) + 1
			s   = ''
			for arg in o.usage().split():
				if l + len(arg) < cols or cols == 0:
					s += '%s ' % arg
					l += len(arg) + 1 # space
				else:
					s += '\n\t%s ' % arg
					l  = len(arg) + 9 # tab + space

			self.addText('%s %s\n' % (cmd, s))


