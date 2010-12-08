# $Id: __init__.py,v 1.2 2010/12/08 00:13:24 bruno Exp $
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
# Revision 1.2  2010/12/08 00:13:24  bruno
# get the right commands
#
# Revision 1.6  2010/09/07 23:53:01  bruno
# star power for gb
#
# Revision 1.5  2009/05/01 19:07:03  mjk
# chimi con queso
#
# Revision 1.4  2008/10/18 00:55:57  mjk
# copyright 5.1
#
# Revision 1.3  2008/03/06 23:41:39  mjk
# copyright storm on
#
# Revision 1.2  2008/02/21 20:24:38  bruno
# fix help
#
# Revision 1.1  2008/01/23 19:05:35  bruno
# can now add kernel boot parameters to the running configuration with the rocks
# command line
#
#

import sys
import string
import rocks.commands
import os

class Command(rocks.commands.set.host.command):
	"""
	Set the boot flags for a host. The boot flags will applied to the
	configuration file that a host uses to boot the running kernel. For
	example, if a node uses GRUB as its boot loader, the boot flags will 
	part of the 'append' line.
	
	<arg type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, then the
	global bootflag will be set.
	</arg>

	<param type='string' name='flags'>
	The boot flags to set for the host.
	</param>
		
	<example cmd='set host bootflags compute-0-0 flags="mem=1024M"'>
	Apply the kernel boot flags "mem=1024M" to compute-0-0.
	</example>
	"""

	def addBootflags(self, nodeid, flags):
		#
		# is there already an entry in the bootflags table
		#
		rows = self.db.execute("""select id from bootflags where
			node = %d""" % (nodeid))

		if rows < 1:
			#
			# insert a new row
			#
			self.db.execute("""insert into bootflags (node, flags)
				values(%s, "%s")""" % (nodeid, flags))
		else:
			#
			# update the existing row
			#
			bootflagsid, = self.db.fetchone()

			self.db.execute("""update bootflags set flags = "%s"
				where id = %s""" % (flags, bootflagsid))

		return


	def run(self, params, args):
		if len(args) == 0:
			hosts = []
		else:
			hosts = self.getHostnames(args)

		(flags, ) = self.fillParams( [('flags', )] )
			
		if not flags:
			self.abort('must supply the flags')

		if not hosts:
			#
			# set the global (all nodes) configuration
			#
			self.addBootflags(0, flags)

		else:
			for host in hosts:
				#
				# get the node id from the nodes table
				#
				self.db.execute("""select id from nodes where
					name='%s'""" % (host))
				hostid, = self.db.fetchone()

				self.addBootflags(hostid, flags)

