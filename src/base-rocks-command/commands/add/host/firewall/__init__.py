# $Id: __init__.py,v 1.3 2011/07/23 02:31:19 phil Exp $
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
# Revision 1.3  2011/07/23 02:31:19  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:15  bruno
# get the right commands
#
# Revision 1.6  2010/09/07 23:52:50  bruno
# star power for gb
#
# Revision 1.5  2010/05/27 00:11:32  bruno
# firewall fixes
#
# Revision 1.4  2010/05/25 21:23:46  bruno
# more firewall fixes
#
# Revision 1.3  2010/05/07 23:13:32  bruno
# clean up the help info for the firewall commands
#
# Revision 1.2  2010/05/04 22:04:14  bruno
# more firewall commands
#
# Revision 1.1  2010/04/30 22:07:16  bruno
# first pass at the firewall commands. we can do global and host level
# rules, that is, we can add, remove, open (calls add), close (also calls add),
# list and dump the global rules and the host-specific rules.
#
#

import rocks.commands
import rocks.commands.add
import rocks.commands.add.firewall

class Command(rocks.commands.add.firewall.command):
	"""
	Add a firewall rule for the specified hosts.

	<arg type='string' name='host'>
	Host name of machine
	</arg>

	<param type='string' name='service'>
	The service identifier, port number or port range. For example
	"www", 8080 or 0:1024.
	</param>

	<param type='string' name='protocol'>
	The protocol associated with the service. For example, "tcp" or "udp".
	</param>
	
        <param type='string' name='network'>
        The network this rule service should be applied to. This is a named
	network (e.g., 'private') and must be one listed by the command
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

        <param type='string' name='flags'>
	Optional flags associated with this rule. An example flag is:
	"-m state --state RELATED,ESTABLISHED".
	</param>

        <param type='string' name='comment'>
	A comment associated with this rule. The comment will be printed
	directly above the rule in the firewall configuration file.
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
			self.abort('must supply at least one host')

		(service, network, outnetwork, chain, action, protocol, flags,
			comment) = self.checkArgs(service, network,
			outnetwork, chain, action, protocol, flags, comment)

		hosts = self.getHostnames(args)

		for host in hosts:
			sql = """node = (select id from nodes where
				name = '%s') and""" % host

			self.checkRule('node_firewall', sql, service, network,
				outnetwork, chain, action, protocol, flags,
				comment)

		#
		# all the rules are valid, now let's add them
		#
		for host in hosts:
			sql = "(select id from nodes where name='%s'), " % host

			self.insertRule('node_firewall', 'node, ', sql, service,
				network, outnetwork, chain, action, protocol,
				flags, comment)
