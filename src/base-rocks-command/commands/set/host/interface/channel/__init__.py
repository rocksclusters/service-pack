# $Id: __init__.py,v 1.1 2010/12/07 23:52:28 bruno Exp $
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
# Revision 1.1  2010/12/07 23:52:28  bruno
# the start of SP 5.4.1
#
# Revision 1.2  2010/09/07 23:53:01  bruno
# star power for gb
#
# Revision 1.1  2010/04/20 17:22:36  bruno
# initial support for channel bonding
#
#

import string
import rocks.commands

class Command(rocks.commands.set.host.command):
	"""
	Sets the channel for a named interface.

	<arg type='string' name='host' repeat='1'>
	One or more hosts.
	</arg>
	
	<arg type='string' name='iface'>
 	Interface that should be updated. This may be a logical interface or 
 	the MAC address of the interface.
 	</arg>

 	<arg type='string' name='channel'>
	The channel for an interface. Use channel=NULL to clear.
	</arg>
 	
	<param type='string' name='iface'>
	Can be used in place of the iface argument.
	</param>

	<param type='string' name='channel'>
	Can be used in place of the channel argument.
	</param>
	
	<example cmd='set host interface channel compute-0-0 iface=eth1 channel="bond0"'>
	Sets the channel for eth1 to be "bond0" (i.e., it associates eth1 with
	the bonded interface named "bond0").
	</example>
	
	<example cmd='set host interface channel compute-0-0 iface=eth1 channel=NULL'>
	Clear the channel entry.
	</example>
	"""
	
	def run(self, params, args):

		(args, iface, channel) = self.fillPositionalArgs(
			('iface', 'channel'))
			
		if not len(args):
			self.abort('must supply host')
		if not iface:
			self.abort('must supply iface')
		if not channel:
			self.abort('must supply channel')

		if string.upper(channel) == 'NULL':
			channel = 'NULL'

		for host in self.getHostnames(args):
			self.db.execute("""update networks, nodes set 
				networks.channel=NULLIF('%s','NULL') where
				nodes.name='%s' and networks.node=nodes.id and
				(networks.device='%s' or networks.mac='%s')""" %
				(channel, host, iface, iface))

