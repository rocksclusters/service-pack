# $Id: __init__.py,v 1.3 2011/07/23 02:31:28 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# Revision 1.3  2011/07/23 02:31:28  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:23  bruno
# get the right commands
#
# Revision 1.5  2010/09/07 23:52:58  bruno
# star power for gb
#
# Revision 1.4  2010/05/20 00:31:45  bruno
# gonna get some serious 'star power' off this commit.
#
# put in code to dynamically configure the static-routes file based on
# networks (no longer the hardcoded 'eth0').
#
# Revision 1.3  2009/06/02 17:28:12  bruno
# added all missing doc strings
#
# Revision 1.2  2009/05/01 19:07:01  mjk
# chimi con queso
#
# Revision 1.1  2009/03/13 22:19:56  mjk
# - route commands done
# - cleanup of rocks.host plugins
#

import rocks.commands

class Command(rocks.commands.remove.os.command):
	"""
	Remove a static route for an OS type.

	<arg type='string' name='os'>
	The OS type (e.g., 'linux', 'sunos', etc.). This argument is required.
	</arg>

	<param type='string' name='address'>
	The address of the static route to remove. This argument is required.
	</param>

	<param type='string' name='address'>
	Can be used in place of the 'address' argument.
	</param>

	<example cmd='remove os route linux 1.2.3.4'>
	Remove the static route for the OS 'linux' that has the
	network address '1.2.3.4'.
	</example>
	"""

	def run(self, params, args):
		(args, address) = self.fillPositionalArgs(('address', ))

		if not address:
			self.abort('address required')
		if len(args) == 0:
			self.abort('must supply at least one OS type')

		for os in self.getOSNames(args):
			self.db.execute("""delete from os_routes where 
			os = '%s' and network = '%s'""" % (os, address))

