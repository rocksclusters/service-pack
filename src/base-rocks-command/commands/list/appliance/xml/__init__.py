# $Id: __init__.py,v 1.4 2012/05/06 05:49:27 phil Exp $
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
# Revision 1.4  2012/05/06 05:49:27  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:23  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:19  bruno
# get the right commands
#
# Revision 1.15  2010/09/07 23:52:54  bruno
# star power for gb
#
# Revision 1.14  2009/05/01 19:06:57  mjk
# chimi con queso
#
# Revision 1.13  2008/12/20 01:06:15  mjk
# - added appliance_attributes
# - attributes => node_attributes
# - rocks set,list,remove appliance attr
# - eval shell for conds has a special local dictionary that allows
#   unresolved variables (attributes) to evaluate to None
# - need to add this to solaris
# - need to move UserDict stuff into pylib and remove cut/paste code
# - need a drink
#
# Revision 1.12  2008/10/18 00:55:49  mjk
# copyright 5.1
#
# Revision 1.11  2008/03/06 23:41:37  mjk
# copyright storm on
#
# Revision 1.10  2007/07/04 01:47:38  mjk
# embrace the anger
#
# Revision 1.9  2007/06/27 23:59:23  bruno
# more cleanup.
#
# phil, commence head shaking.
#
# Revision 1.8  2007/06/19 16:42:41  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.7  2007/06/16 02:39:51  mjk
# - added list roll commands (used for docbook)
# - docstrings should now be XML
# - added parser for docstring to ASCII or DocBook
# - ditched Phil's Network regex stuff (will come back later)
# - updated several docstrings
#
# Revision 1.6  2007/06/07 21:23:04  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.5  2007/05/31 19:35:42  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.4  2007/05/11 18:33:15  mjk
# - fix list host profiles
# - [hosts] -> [host(s)]
#
# Revision 1.3  2007/05/10 20:37:01  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.2  2007/02/27 01:53:58  mjk
# - run(self, args) => run(self, flags, args)
# - replaced rocks list host xml with more complete code
# - replaced rocks lust node xml with kpp shell (not a command now)
#
# Revision 1.1  2007/01/17 19:31:19  anoop
# new command line function
# rocks list appliance xml <membership>
#

import rocks.commands

class Command(rocks.commands.list.appliance.command):

	"""
	Lists the XML profile for a given appliance type. This is useful
	for high level debugging but will be missing any host specific
	variables. It cannot be used to pass into 'rocks list host profile'
	to create a complete Kickstart/Jumpstart profile.
	
	<arg optional='1' type='string' name='appliance' repeat='1'>
	Optional list of appliance names.
	</arg>
		
	<example cmd='list appliance xml compute'>
	Lists the XML profile for a compute appliance.
	</example>

	<example cmd='list appliance xml'>
	Lists the XML profile for all appliance types.
	</example>
	"""

	def run(self, params, args):

		self.beginOutput()
		for app in self.getApplianceNames(args):
			self.db.execute("""select node from appliances
				where name='%s'""" % app)
			try:
				(node, ) = self.db.fetchone()
			except TypeError:
				self.abort('no such appliance "%s"' %
					app)
			if node:
				xml = self.command('list.node.xml', [node])
				for line in xml.split('\n'):
					self.addOutput(app, line)
		self.endOutput(padChar='')

