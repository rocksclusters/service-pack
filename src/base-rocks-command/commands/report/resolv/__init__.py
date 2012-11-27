# $Id: __init__.py,v 1.5 2012/11/27 00:49:25 phil Exp $
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
# Revision 1.5  2012/11/27 00:49:25  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/05/06 05:49:37  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:29  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:24  bruno
# get the right commands
#
# Revision 1.4  2010/09/07 23:53:00  bruno
# star power for gb
#
# Revision 1.3  2010/06/30 17:37:33  anoop
# Overhaul of the naming system. We now support
# 1. Multiple zone/domains
# 2. Serving DNS for multiple domains
# 3. No FQDN support for network names
#    - FQDN must be split into name & domain.
#    - Each piece information will go to a
#      different table
# Hopefully, I've covered the basics, and not broken
# anything major
#
# Revision 1.2  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.1  2009/03/04 20:15:31  bruno
# moved 'dbreport hosts' and 'dbreport resolv' into the command line
#
#

import rocks.commands

class command(rocks.commands.HostArgumentProcessor,
		rocks.commands.report.command):

	def searchdomain(self):
		"""Prints the domain and search entries."""

		s = 'search '
		# First add the private network entry.
		self.db.execute('select dnszone from ' +\
			'subnets where name="private"')
		private_domain, = self.db.fetchone()
		s += private_domain

		# Add the remaining network searches after
		self.db.execute('select dnszone from ' +\
			'subnets where name!="private"')
		for (zone, ) in self.db.fetchall():
			s += ' %s' % zone

		print s	

	def nameservers(self, servers):
		"""Prints a comma-separated list of name servers
		in the resolv.conf style."""

		if servers:
			for server in servers.split(','):
				print 'nameserver', server


class Command(command):
	"""
	Report for /etc/resolv.conf for public side nodes.

	<example cmd='report resolv'>
	Outputs data for /etc/resolv.conf for the frontend.
	</example>
	"""

	def run(self, param, args):
		"""Defines the resolv.conf for public side nodes."""
		
		self.searchdomain()
		print 'nameserver 127.0.0.1'
		self.nameservers(self.db.getHostAttr('localhost',
			'Kickstart_PublicDNSServers'))

