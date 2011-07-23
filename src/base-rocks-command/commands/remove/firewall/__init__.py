# $Id: __init__.py,v 1.3 2011/07/23 02:31:26 phil Exp $
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
# Revision 1.3  2011/07/23 02:31:26  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:22  bruno
# get the right commands
#
# Revision 1.5  2010/11/19 16:15:17  bruno
# fix to remove a firewall rule with 'all' as its 'network' or 'output-network'
#
# Revision 1.4  2010/09/07 23:52:57  bruno
# star power for gb
#
# Revision 1.3  2010/05/11 22:28:16  bruno
# more tweaks
#
# Revision 1.2  2010/05/07 23:13:33  bruno
# clean up the help info for the firewall commands
#
# Revision 1.1  2010/04/30 22:07:16  bruno
# first pass at the firewall commands. we can do global and host level
# rules, that is, we can add, remove, open (calls add), close (also calls add),
# list and dump the global rules and the host-specific rules.
#
#

import rocks.commands

class command(rocks.commands.remove.command):
	def deleteRule(self, table, extrawhere, service, network, outnetwork,
		chain, action, protocol):

		if not service:
			self.abort('service required')
		if not network and not outnetwork:
			self.abort('network or output-network required')
		if not chain:
			self.abort('chain required')
		if not action:
			self.abort('action required')
		if not protocol:
			self.abort('protocol required')

		if network:
			if network == 'all':
				inid = '0'
			else:
				rows = self.db.execute("""select id from
					subnets where name = '%s'""" % network)

				if rows == 0:
					self.abort('network "%s" not in ' +
						'database' % network)

				inid, = self.db.fetchone()
		else:
			inid = 'NULL'

		if outnetwork:
			if outnetwork == 'all':
				outid = '0'
			else:
				rows = self.db.execute("""select id from
					subnets where name = '%s'""" %
					outnetwork)

				if rows == 0:
					self.abort('output-network "%s" not ' +
						'in database' % network)

				outid, = self.db.fetchone()
		else:
			outid = 'NULL'

		rows = self.db.execute("""delete from %s where %s
			service = '%s' and if ('%s' = 'NULL', insubnet is NULL,
			insubnet = %s) and if ('%s' = 'NULL', outsubnet is NULL,
			outsubnet = %s) and chain = '%s' and action = '%s' and
			protocol = '%s'""" % (table, extrawhere, service, inid,
			inid, outid, outid, chain, action, protocol))

		if rows == 0:
			netname = []
			if network:
				netname.append(network)
			if outnetwork:
				netname.append(outnetwork)

			self.abort('no service in database that matches %s/%s/%s/%s/%s' % (service, protocol, '/'.join(netname), chain, action)) 



class Command(command):
	"""
	Remove a global firewall rule. To remove a rule,
	one must supply the service, protocol, network, chain and action. See
	"rocks list firewall" for the current global rules.

	<param type='string' name='service'>
	The service identifier, for example "www".
	</param>

        <param type='string' name='protocol'>
        The protocol associated with the service to be removed (e.g, "tcp"
	or "udp").
	</param>

        <param type='string' name='network'>
        The network associated with the rule. This is a
	named network (e.g., 'private') and must be one listed by the command
        'rocks list network'.
	</param>

        <param type='string' name='output-network' optional='1'>
        The output network associated with the rule. This is a
	named network (e.g., 'private') and must be one listed by the command
        'rocks list network'.
	</param>

        <param type='string' name='chain'>
	The chain associated with the rule (e.g., "INPUT").
	</param>

        <param type='string' name='action'>
	The action associated with the rule (e.g., "ACCEPT").
	</param>
	"""

	def run(self, params, args):
		(service, network, outnetwork, chain, action, protocol) = \
			self.fillParams([
				('service', ),
				('network', ),
				('output-network', ),
				('chain', ),
				('action', ),
				('protocol', )
			 ])

		self.deleteRule('global_firewall', '', service, network,
			outnetwork, chain, action, protocol)

