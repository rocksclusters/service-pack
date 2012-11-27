# $Id: __init__.py,v 1.5 2012/11/27 00:49:15 phil Exp $
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
# Revision 1.5  2012/11/27 00:49:15  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/05/06 05:49:22  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:19  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:15  bruno
# get the right commands
#
# Revision 1.2  2010/09/07 23:52:50  bruno
# star power for gb
#
# Revision 1.1  2010/06/15 19:35:43  bruno
# commands to:
#  - manage public keys
#  - start/stop a service
#
#

import os
import rocks.commands

class Command(rocks.commands.add.host.command):
	"""
	Add a public key for a host. One use of this public key is to 
	authenticate messages sent from remote services.

	<arg type='string' name='host'>
	Host name of machine
	</arg>
	
	<param type='string' name='key'>
	A public key. This can be the actual key or it can be a path name to
	a file that contains a public key (e.g., /tmp/public.key).
	</param>
	"""

	def run(self, params, args):
		key, = self.fillParams([ ('key', ) ])

		if not key:
			self.abort('must supply a public key')

		if len(args) == 0:
			self.abort('must supply a host')

		hosts = self.getHostnames(args)

		if len(hosts) > 1:
			self.abort('must supply only one host')

		host = hosts[0]

		#
		# see if the key is a file name
		#
		if os.path.exists(key):
			file = open(key, 'r')
			public_key = file.read()
			file.close()
		else:
			public_key = key

		#
		# check if the key already exists
		#
		rows = self.db.execute("""select * from public_keys where
			node = (select id from nodes where name = '%s') and
			public_key = '%s' """ % (host, public_key))

		if rows == 1:
			self.abort('the public key already exists for host %s'
				% host)

		#
		# add the key
		#
		self.db.execute("""insert into public_keys (node, public_key)
			values ((select id from nodes where name = '%s'),
			'%s') """ % (host, public_key))

