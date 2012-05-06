# $Id: __init__.py,v 1.4 2012/05/06 05:49:22 phil Exp $
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
# Revision 1.4  2012/05/06 05:49:22  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:19  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:15  bruno
# get the right commands
#
# Revision 1.5  2010/09/07 23:52:50  bruno
# star power for gb
#
# Revision 1.4  2010/05/11 22:28:15  bruno
# more tweaks
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

import string
import rocks.commands

class command(rocks.commands.HostArgumentProcessor, rocks.commands.add.command):
	def serviceCheck(self, service):
		#
		# a service can look like:
		#
		#	reserved words: all, nat
		#       named service: ssh
		#       specific port: 8069
		#       port range: 0:1024
		#
		if service in [ 'all', 'nat' ]:
			#
			# valid
			#
			return

		if service[0] in string.digits:
			#
			# if the first character is a number, then assume
			# this is a port or port range:
			#
			ports = service.split(':')
			if len(ports) > 2:
				msg = 'port range "%s" is invalid. ' % service
				msg += 'it must be "integer:integer"'
				self.abort(msg)

			for a in ports:
				try:
					i = int(a)
				except:
					msg = 'port specification "%s" ' % \
						service
					msg += 'is invalid. '
					msg += 'it must be "integer" or '
					msg += '"integer:integer"'
					self.abort(msg)

		#
		# if we made it here, then the service definition looks good
		#
		return


	def checkArgs(self, service, network, outnetwork, chain, action,
		protocol, flags, comment):

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

		#
		# check if the network exists
		#
		if network == 'all':
			network = 0
		elif network:
			rows = self.db.execute("""select id from subnets where
				name = '%s'""" % (network))

			if rows == 0:
				self.abort('network "%s" not in the database. Run "rocks list network" to get a list of valid networks.' % network)

			network, = self.db.fetchone()
		else:
			network = 'NULL'

		if outnetwork == 'all':
			outnetwork = 0
		elif outnetwork:
			rows = self.db.execute("""select id from subnets where
				name = '%s'""" % (outnetwork))

			if rows == 0:
				self.abort('output-network "%s" not in the database. Run "rocks list network" to get a list of valid networks.')

			outnetwork, = self.db.fetchone()
		else:
			outnetwork = 'NULL'

		self.serviceCheck(service)

		action = action.upper()
		chain = chain.upper()

		if protocol:
			protocol = '"%s"' % protocol
		else:
			protocol = 'NULL'

		if flags:
			flags = '"%s"' % flags
		else:
			flags = 'NULL'

		if comment:
			comment = '"%s"' % comment
		else:
			comment = 'NULL'

		return (service, network, outnetwork, chain, action,
			protocol, flags, comment)


	def checkRule(self, table, extrawhere, service, network, outnetwork,
		chain, action, protocol, flags, comment):

		rows = self.db.execute("""select * from %s where %s
			service = '%s' and action = '%s' and chain = '%s' and
			if ('%s' = 'NULL', insubnet is NULL,
				insubnet = %s) and
			if ('%s' = 'NULL', outsubnet is NULL,
				outsubnet = %s) and
			if ('%s' = 'NULL', protocol is NULL,
				protocol = %s) and
			if ('%s' = 'NULL', flags is NULL,
				flags = %s) """ % (table, extrawhere, service,
			action, chain, network, network, outnetwork,
			outnetwork, protocol, protocol, flags, flags))

		if rows:
			self.abort('firewall rule already exists')


	def insertRule(self, table, extracol, extraval, service, network,
		outnetwork, chain, action, protocol, flags, comment):

		#
		# all input has been verified. add the row
		#
		self.db.execute("""insert into %s
			(%s insubnet, outsubnet, service, protocol,
			action, chain, flags, comment) values (%s %s, %s,
			'%s', %s, '%s', '%s', %s, %s)""" %
			(table, extracol, extraval, network, outnetwork,
			service, protocol, action, chain, flags, comment))


class Command(command):
	"""
	Add a global firewall rule for the all hosts in the cluster.

	<param type='string' name='service'>
	The service identifier, port number or port range. For example
	"www", 8080 or 0:1024.
	</param>

	<param type='string' name='protocol'>
	The protocol associated with the rule. For example, "tcp" or "udp".
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
		
		(service, network, outnetwork, chain, action, protocol, flags,
			comment) = self.checkArgs(service, network,
			outnetwork, chain, action, protocol, flags, comment)

		self.checkRule('global_firewall', '', service, network,
			outnetwork, chain, action, protocol, flags, comment)

		self.insertRule('global_firewall', '', '', service, network,
			outnetwork, chain, action, protocol, flags, comment)
			
