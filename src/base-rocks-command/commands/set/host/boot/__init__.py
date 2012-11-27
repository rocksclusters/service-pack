# $Id: __init__.py,v 1.5 2012/11/27 00:49:26 phil Exp $
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
# Revision 1.5  2012/11/27 00:49:26  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/05/06 05:49:38  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:30  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:24  bruno
# get the right commands
#
# Revision 1.8  2010/09/07 23:53:01  bruno
# star power for gb
#
# Revision 1.7  2010/05/24 17:41:55  bruno
# fix help doc.
#
# Revision 1.6  2009/05/01 19:07:03  mjk
# chimi con queso
#
# Revision 1.5  2009/02/13 20:21:12  bruno
# make sure physical hosts look at the 'runaction' or 'installaction'
# columns in the nodes table in order to reference the correct bootaction.
#
# Revision 1.4  2009/01/16 23:58:15  bruno
# configuring the boot action and writing the boot files (e.g., PXE host config
# files and Xen config files) are now done in exactly the same way.
#
#

import rocks.commands

class Command(rocks.commands.set.host.command):
	"""
	Set a bootaction for a host. A hosts action can be set to 'install' 
	or to 'os' (also, 'run' is a synonym for 'os').

	<arg type='string' name='host' repeat='1'>
	One or more host names.
	</arg>

	<param type='string' name='action'>
	The label name for the bootaction. This must be one of: 'os',
	'install', or 'run'.

	If no action is supplied, then only the configuration file for the
	list of hosts will be rewritten.
	</param>
		
	<example cmd='set host boot compute-0-0 action=os'>
	On the next boot, compute-0-0 will boot the profile based on its
	"run action". To see the node's "run action", execute:
	"rocks list host compute-0-0" and examine the value in the
	"RUNACTION" column.
	</example>
	"""

	def updateBoot(self, host, action):
		#
		# is there already an entry in the boot table
		#
		nrows = self.db.execute("""select b.id from boot b, nodes n
			where n.name = '%s' and n.id = b.node""" % host)

		if nrows < 1:
			#
			# insert a new row
			#
			self.db.execute("""insert into boot (node, action)
				values((select id from nodes where name = '%s'),
				"%s") """ % (host, action))
		else:
			#
			# update an existing row
			#
			bootid, = self.db.fetchone()

			self.db.execute("""update boot set action = "%s"
				where id = %s """ % (action, bootid))
		return

	def run(self, params, args):
		(action,) = self.fillParams([('action', )])
		
		if not len(args):
			self.abort('must supply host')

		if action not in [ 'os', 'run', 'install', None ]:
			self.abort('invalid action. action must be ' +
				'"os", "run" or "install"')

		for host in self.getHostnames(args):
			if action:
				self.updateBoot(host, action)

			#
			# run the plugins
			# 
			self.runPlugins(host)

