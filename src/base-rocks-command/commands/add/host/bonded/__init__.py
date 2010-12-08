# $Id: __init__.py,v 1.2 2010/12/08 00:13:15 bruno Exp $
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
# Revision 1.2  2010/12/08 00:13:15  bruno
# get the right commands
#
# Revision 1.4  2010/09/07 23:52:50  bruno
# star power for gb
#
# Revision 1.3  2010/04/30 22:02:13  bruno
# changed 'subnet' parameter to 'network'
#
# Revision 1.2  2010/04/20 19:33:04  bruno
# more bonding tweaks
#
# Revision 1.1  2010/04/20 17:22:35  bruno
# initial support for channel bonding
#
#


import rocks.commands

class Command(rocks.commands.add.host.command):
	"""
	Add a channel bonded interface for a host

	<arg type='string' name='host'>
	Host name of machine
	</arg>
	
	<param type='string' name='channel'>
	The channel name (e.g., "bond0").
	</param>

	<param type='string' name='interfaces'>
	The physical interfaces that will be bonded. The interfaces
	can be a comma-separated list (e.g., "eth0,eth1") or a space-separated
	list (e.g., "eth0 eth1").
	</param>

	<param type='string' name='ip'>
	The IP address to assign to the bonded interface.
	</param>

	<param type='string' name='network'>
	The network to be assigned to this interface. This is a named network
	(e.g., 'private') and must be listable by the command
	'rocks list network'.
	</param>

	<param type='string' name='name' optional='1'>
	The host name associated with the bonded interface. If name is not
	specified, then the interface get the internal host name
	(e.g., compute-0-0).
	</param>

	<example cmd='add host bonded compute-0-0 channel=bond0
		interfaces=eth0,eth1 ip=10.1.255.254 network=private'>
	Adds a bonded interface named "bond0" to compute-0-0 by bonding
	the physical interfaces eth0 and eth1, it assigns the IP address
	10.1.255.254 to bond0 and it associates this interface to the private
	network.
	</example>
	"""

	def run(self, params, args):
		(channel, interfaces, ip, network, name) = self.fillParams([
			('channel', ),
			('interfaces', ),
			('ip', ),
			('network', ),
			('name', ) ])
		
		hosts = self.getHostnames(args)

		if len(hosts) == 0:
			self.abort('host required')
		if len(hosts) > 1:
			self.abort('only one host required')
	
		host = hosts[0]

		if not name:
			#
			# if name is not supplied, then give it the host name
			#
			name = host
		
		if not channel:
			self.abort('channel required')
		if not interfaces:
			self.abort('interfaces required')
		if not ip:
			self.abort('ip required')
		if not network:
			self.abort('network required')
		
		#
		# check if the network exists
		#
		rows = self.db.execute("""select name from subnets where
			name = '%s'""" % (network))

		if rows == 0:
			self.abort('network "%s" not in the database. Run "rocks list network" to get a list of valid networks.')

		ifaces = []
		if ',' in interfaces:
			#
			# comma-separated list
			#
			for i in interfaces.split(','):
				ifaces.append(i.strip())
		else:
			#
			# assume it is a space-separated list
			#
			for i in interfaces.split():
				ifaces.append(i.strip())
			
		#
		# check if the physical interfaces exist
		#
		for i in ifaces:
			rows = self.db.execute("""select net.device from
				networks net, nodes n where
				net.device = '%s' and n.name = '%s' and
				net.node = n.id""" % (i, host))

			if rows == 0:
				self.abort('interface "%s" does not exist for host "%s"' % (i, host))

		#
		# ok, we're good to go
		#
		# add the bonded interface
		#
		self.command('add.host.interface',
			(host, channel, 'ip=%s' % ip, 'module=bonding',
			'name=%s' % name, 'subnet=%s' % network))

		#
		# clear out all networking info from the physical interfaces and
		# then associate the interfaces with the bonded channel
		#
		for i in ifaces:
			self.command('set.host.interface.subnet',
				(host, i, 'subnet=NULL'))
			self.command('set.host.interface.ip',
				(host, i, 'ip=NULL'))
			self.command('set.host.interface.name',
				(host, i, 'name=NULL'))

			self.command('set.host.interface.channel',
				(host, i, 'channel=%s' % channel))

