# $Id: __init__.py,v 1.4 2012/05/06 05:49:31 phil Exp $
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
# Revision 1.4  2012/05/06 05:49:31  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:26  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:22  bruno
# get the right commands
#
# Revision 1.9  2010/09/07 23:52:57  bruno
# star power for gb
#
# Revision 1.8  2009/05/01 19:07:00  mjk
# chimi con queso
#
# Revision 1.7  2009/02/12 05:17:01  bruno
# typo
#
# Revision 1.6  2008/10/18 00:55:55  mjk
# copyright 5.1
#
# Revision 1.5  2008/07/08 21:45:40  bruno
# sync the config after hosts are removed
#
# Revision 1.4  2008/03/06 23:41:38  mjk
# copyright storm on
#
# Revision 1.3  2008/02/01 20:52:27  bruno
# use plugins to support removing all database entries for a host.
#
# Revision 1.2  2007/06/25 23:24:36  bruno
# added a command to remove the PXE boot configuration for a node that
# is removed with insert-ethers
#
#

import rocks.commands

class command(rocks.commands.HostArgumentProcessor,
		rocks.commands.remove.command):
	pass

class Command(command):
	"""
	Remove a host from the database. This command will remove all
	related database rows for each specified host.

	<arg type='string' name='host' repeat='1'>
	List of hosts to remove from the database.
	</arg>

	<example cmd='remove host compute-0-0'>
	Remove the compute-0-0 from the database.
	</example>
	"""

	def run(self, params, args):
		if len(args) < 1:
			self.abort('must supply at least one host')

		for host in self.getHostnames(args):
			self.runPlugins(host)

		#	
		# sync the config when done
		#	
		self.command('sync.config')

