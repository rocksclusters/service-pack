# $Id: __init__.py,v 1.3 2011/07/23 02:31:27 phil Exp $
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
# Revision 1.3  2011/07/23 02:31:27  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:22  bruno
# get the right commands
#
# Revision 1.3  2010/09/07 23:52:58  bruno
# star power for gb
#
# Revision 1.2  2009/05/01 19:07:00  mjk
# chimi con queso
#
# Revision 1.1  2008/12/15 22:27:21  bruno
# convert pxeboot and pxeaction tables to boot and bootaction tables.
#
# this enables merging the pxeaction and vm_profiles tables
#
#

import os
import os.path
import string
import rocks.commands

class Command(rocks.commands.remove.host.command):
	"""
	Removes the boot configuration for a host

	<arg type='string' name='host' repeat='1'>
	One or more named hosts.
	</arg>
	
	<example cmd='remove host boot compute-0-0'>
	Removes the boot configuration for host compute-0-0.
	</example>

	<example cmd='remove host boot compute-0-0 compute-0-1'>
	Removes the boot configuration for hosts compute-0-0 and
	compute-0-1.
	</example>
	"""
	
	def run(self, params, args):
		if not len(args):
			self.abort("must supply host")

		for host in self.getHostnames(args):

			self.db.execute("""delete from boot where boot.node =
				(select id from nodes where name='%s')""" % 
				host)
				
			#
			# remove the pxe configuration file
			#
			rows = self.db.execute("""select networks.ip from
				networks, nodes, subnets where
				networks.node = nodes.id and
				subnets.name = 'private' and
				networks.subnet = subnets.id and
				nodes.name = '%s' """ % host)

			for ipaddr, in self.db.fetchall():
				if not ipaddr:
					return

				filename = '/tftpboot/pxelinux/pxelinux.cfg/'
				for i in string.split(ipaddr, '.'):
					hexstr = '%02x' % (int(i))
					filename += '%s' % hexstr.upper()

				if os.path.exists(filename):
					os.unlink(filename)

