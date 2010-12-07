# $Id: __init__.py,v 1.1 2010/12/07 23:52:29 bruno Exp $
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
# Revision 1.1  2010/12/07 23:52:29  bruno
# the start of SP 5.4.1
#
# Revision 1.3  2010/10/06 19:41:10  phil
# Document and interpret linux-only options: dhcp, noreport.
# Needed by EC2.
#
# Revision 1.2  2010/09/07 23:53:01  bruno
# star power for gb
#
# Revision 1.1  2010/04/19 22:56:58  bruno
# new
#
#

import string
import rocks.commands

class Command(rocks.commands.set.host.command):
	"""
	Sets the options for a device module for a named interface. On Linux,
	this will get translated to an entry in /etc/modprobe.conf.

	<arg type='string' name='host' repeat='1'>
	One or more hosts.
	</arg>
	
	<arg type='string' name='iface'>
 	Interface that should be updated. This may be a logical interface or 
 	the MAC address of the interface.
 	</arg>
 	
	<param type='string' name='iface'>
	Can be used in place of the iface argument.
	</param>

	<param type='string' name='options'>
	The options for an interface. Use options=NULL to clear.
	In Rocks 5.4 (linux): options='dhcp' or options='noreport' have
	special meaning. Bonded interfaces use options field to set up
	bonding options.
	</param>
	
	<example cmd='set host interface options compute-0-0 iface=eth1 options="Speed=10"'>
	Sets the option "Speed=10" for eth1 on e1000 on host compute-0-0.
	</example>
	
	<example cmd='set host interface options compute-0-0 iface=eth1 options=NULL'>
	Clear the options entry.
	</example>

	<example cmd='set host interface options compute-0-0 iface=eth0 options="dhcp"'>
	Linux only: Configure eth0 interface for DHCP instead of static.
	</example>

	<example cmd='set host interface options compute-0-0 iface=eth0 options="noreport"'>
	Linux only:  Tell rocks report host interface to ignore this interface
	when writing configuration files
	</example>
	
	"""
	
	def run(self, params, args):

		(args, iface, options) = self.fillPositionalArgs(
			('iface', 'options'))
			
		if not len(args):
			self.abort('must supply host')
		if not iface:
			self.abort('must supply iface')
		if not options:
			self.abort('must supply options')

		if string.upper(options) == 'NULL':
			options = 'NULL'

		for host in self.getHostnames(args):
			self.db.execute("""update networks, nodes set 
				networks.options=NULLIF('%s','NULL') where
				nodes.name='%s' and networks.node=nodes.id and
				(networks.device='%s' or networks.mac='%s')""" %
				(options, host, iface, iface))

