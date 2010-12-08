# $Id: __init__.py,v 1.2 2010/12/08 00:13:18 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# Revision 1.2  2010/12/08 00:13:18  bruno
# get the right commands
#
# Revision 1.8  2010/09/07 23:52:53  bruno
# star power for gb
#
# Revision 1.7  2009/05/01 19:06:57  mjk
# chimi con queso
#
# Revision 1.6  2008/10/18 00:55:49  mjk
# copyright 5.1
#
# Revision 1.5  2008/08/18 21:16:06  mjk
# - Added cols arg to list help (cols=0 means no line wrapping)
# - Added help verb as a rocks help | grep XXX shortcut
#

import string
import rocks.commands

class command(rocks.commands.Command):

	MustBeRoot = 0

	
class Command(command):
	"""
	List help for the command line client.  With no arguments it lists
	all the commands available.  Otherwise it will list the subset
	of command with the specified string (see examples).

	<arg type='string' name='command'>
	The substring matched against all commands.
	</arg>

	<example cmd='help'>
	Alias for 'rocks list help'
	</example>

	<example cmd='help viz'>
	Lists all the commands with the string 'viz' in the name.
	</example>

	<example cmd='help list host'>
	Lists all the commands with the string 'list host' in the name.
	</example>
	"""

	def run(self, params, args):

		help = self.command('list.help', [ 'cols=0' ])
		sub  = string.join(args)

		if not args:
			self.addText(help)
		else:
			for line in help.split('\n'):
				if line:
					if string.find(line, sub) >= 0:
						self.addText('%s\n' % line)
		
