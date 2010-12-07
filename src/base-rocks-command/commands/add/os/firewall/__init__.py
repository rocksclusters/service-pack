# $Id: __init__.py,v 1.1 2010/12/07 23:52:17 bruno Exp $
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
# Revision 1.1  2010/12/07 23:52:17  bruno
# the start of SP 5.4.1
#
# Revision 1.3  2010/09/07 23:52:50  bruno
# star power for gb
#
# Revision 1.2  2010/05/07 23:13:32  bruno
# clean up the help info for the firewall commands
#
# Revision 1.1  2010/05/04 22:04:15  bruno
# more firewall commands
#
#

import rocks.commands
import rocks.commands.add
import rocks.commands.add.firewall

class Command(rocks.commands.add.firewall.command,
	rocks.commands.add.os.command):

	"""
	Add a firewall rule for an OS type.

	<arg type='string' name='os'>
	OS type (e.g., 'linux', 'sunos').
	</arg>

	<param type='string' name='service'>
	The service identifier, port number or port range. For example
	"www", 8080 or 0:1024.
	</param>

	<param type='string' name='protocol'>
	The protocol associated with the service. For example, "tcp" or "udp".
	</param>
	
        <param type='string' name='network'>
        The network this rule should be applied to. This is a named network
        (e.g., 'private') and must be one listed by the command
        'rocks list network'.
	</param>

        <param type='string' name='output-network' optional='1'>
        The output network this rule should be applied to. This is a named
	network (e.g., 'private') and must be one listed by the command
        'rocks list network'.
	</param>

        <param type='string' name='chain'>
	The iptables 'chain' this rule should be applied to (e.g.,
	INPUT, OUTPUT, FORWARD).
	</param>

        <param type='string' name='action'>
	The iptables 'action' this rule should be applied to (e.g.,
	ACCEPT, REJECT, DROP).
	</param>
	"""

	def run(self, params, args):
		(service, network, outnetwork, chain, action, protocol, flags,
			comment) = self.fillParams([
				('service', ),
				('network', ),
				('output-network', ),
				('chain', ),
				('action', ),
				('protocol', ),
				('flags', ),
				('comment', )
			])

		if len(args) == 0:
			self.abort('must supply at least one OS type')

		(service, network, outnetwork, chain, action, protocol, flags,
			comment) = self.checkArgs(service, network,
			outnetwork, chain, action, protocol, flags, comment)

		oses = self.getOSNames(args)

		for os in oses:
			sql = "os = '%s' and" % os

			self.checkRule('os_firewall', sql, service,
				network, outnetwork, chain, action, protocol,
				flags, comment)

		#
		# all the rules are valid, now let's add them
		#
		for os in oses:
			self.insertRule('os_firewall', 'os, ', '"%s", ' % os,
				service, network, outnetwork, chain, action,
				protocol, flags, comment)

