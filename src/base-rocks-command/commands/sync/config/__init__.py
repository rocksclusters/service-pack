# $Id: __init__.py,v 1.5 2012/11/27 00:49:29 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# Revision 1.5  2012/11/27 00:49:29  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/05/06 05:49:40  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:32  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:27  bruno
# get the right commands
#
# Revision 1.8  2010/11/19 23:56:00  bruno
# convert dhcp configuration to output XML
#
# lookup the private interface name and write it to /etc/sysconfig/dhcpd
#
# Revision 1.7  2010/09/07 23:53:03  bruno
# star power for gb
#
# Revision 1.6  2009/05/01 19:07:04  mjk
# chimi con queso
#
# Revision 1.5  2008/11/03 23:02:52  bruno
# bug fix where insert-ethers --replace causes an exception to be printed.
#
# Revision 1.4  2008/10/31 23:00:44  mjk
# fix addText call
#
# Revision 1.3  2008/10/18 00:55:58  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:41:40  mjk
# copyright storm on
#
# Revision 1.1  2007/07/02 18:41:01  bruno
# added 'rocks sync config' (insert-ethers --update) and more sync cleanup
#
#

import os
import sys
import string
import rocks.file
import rocks.commands


class Command(rocks.commands.sync.command):
	"""
	For each system configuration file controlled by Rocks, first
	rebuild the configuration file by extracting data from the
	database, then restart the relevant services.

	<example cmd='sync config'>
	Rebuild all configuration files and restart relevant services.
	</example>
	"""

	def run(self, params, args):
		#
		# don't call insert-ethers if insert-ethers is already
		# running. this can occur when one replaces a node
		# (insert-ethers calls 'rocks remove host' which calls
		# rocks sync config).
		#
		if not os.path.exists('/var/lock/insert-ethers'):

			#
			# run the plugins 
			#
			self.runPlugins()

			cmd = '/opt/rocks/sbin/insert-ethers --update'
			for line in os.popen(cmd).readlines():
				self.addText(line)
