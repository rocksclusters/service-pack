# $Id: __init__.py,v 1.2 2010/12/08 00:13:27 bruno Exp $
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
# Revision 1.2  2010/12/08 00:13:27  bruno
# get the right commands
#
# Revision 1.2  2010/09/07 23:53:03  bruno
# star power for gb
#
# Revision 1.1  2010/06/07 23:50:12  bruno
# added a command to swap two interfaces
#
#

import rocks.commands

class Command(rocks.commands.swap.host.command):
	"""
	Swaps two host interfaces in the database.

	<arg type='string' name='host'>
	Host name of machine
	</arg>

	<param type='string' name='ifaces'>
	Two comma-separated interface names (e.g., ifaces="eth0,eth1").
	</param>

	<param type='boolean' name='sync-config'>
	If "yes", then run 'rocks sync config' at the end of the command.
	The default is: yes.
	</param>
	"""

	def swap(self, host, old_mac, old_iface, new_mac, new_iface):
		#
		# swap two interfaces
		#
		rows = self.db.execute("""select id,module,options from
			networks where mac = '%s' and node = (select id from
			nodes where name = '%s') """ % (old_mac, host))
		if rows != 1:
			return

		(old_id, old_module, old_options) = self.db.fetchone()

		rows = self.db.execute("""select id,module,options from
			networks where mac = '%s' and node = (select id from
			nodes where name = '%s') """ % (new_mac, host))
		if rows != 1:
			return

		(new_id, new_module, new_options) = self.db.fetchone()

		self.db.execute("""update networks set mac = '%s',
			device = '%s' where id = %s""" % (old_mac, old_iface,
			new_id))

		self.db.execute("""update networks set mac = '%s',
			device = '%s' where id = %s""" % (new_mac, new_iface,
			old_id))

		if old_module:
			self.db.execute("""update networks set module = '%s'
				where id = %s""" % (old_module, new_id))
		if new_module:
			self.db.execute("""update networks set module = '%s'
				where id = %s""" % (new_module, old_id))
		if old_options:
			self.db.execute("""update networks set options = '%s'
				where id = %s""" % (old_options, new_id))
		if new_options:
			self.db.execute("""update networks set options = '%s'
				where id = %s""" % (new_options, old_id))


	def run(self, params, args):
		ifaces, sync_config = self.fillParams([
			('ifaces', None),
			('sync-config', 'yes')
			])

		syncit = self.str2bool(sync_config)

		if not ifaces:
			self.abort('must supply two interfaces')

		iface = ifaces.split(',')
		if len(iface) != 2:
			self.abort('must supply two interfaces')
		
		hosts = self.getHostnames(args)
		if len(hosts) != 1:	
			self.abort('must supply only one host')
		host = hosts[0]

		mac = []

		self.db.execute("""select mac from networks where node =
			(select id from nodes where name = '%s') and
			device = '%s' """ % (host, iface[0]))

		m, = self.db.fetchone()
		mac.append(m)

		self.db.execute("""select mac from networks where node =
			(select id from nodes where name = '%s') and
			device = '%s' """ % (host, iface[1]))

		m, = self.db.fetchone()
		mac.append(m)

		self.swap(host, mac[0], iface[0], mac[1], iface[1])

		if syncit:
			self.command('sync.config')	

