# $Id: __init__.py,v 1.4 2012/05/06 05:49:39 phil Exp $
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
# Revision 1.4  2012/05/06 05:49:39  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:31  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:26  bruno
# get the right commands
#
# Revision 1.11  2010/09/07 23:53:02  bruno
# star power for gb
#
# Revision 1.10  2009/05/01 19:07:03  mjk
# chimi con queso
#
# Revision 1.9  2008/10/18 00:55:57  mjk
# copyright 5.1
#
# Revision 1.8  2008/03/06 23:41:40  mjk
# copyright storm on
#
# Revision 1.7  2007/07/04 01:47:40  mjk
# embrace the anger
#
# Revision 1.6  2007/06/19 16:42:43  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.5  2007/06/16 02:39:51  mjk
# - added list roll commands (used for docbook)
# - docstrings should now be XML
# - added parser for docstring to ASCII or DocBook
# - ditched Phil's Network regex stuff (will come back later)
# - updated several docstrings
#
# Revision 1.4  2007/06/13 21:47:47  phil
# 1. allow wildcarded network names
# 2. only return those names actually found in the database
#
# Revision 1.3  2007/06/13 20:50:33  phil
# Reverse order of arguments. Document on next checkin
#
# Revision 1.2  2007/06/12 19:15:11  mjk
# - simpler set network commands
# - added remove network
#
# Revision 1.1  2007/06/12 01:10:42  mjk
# - 'rocks add subnet' is now 'rocks add network'
# - added set network subnet|netmask
# - added list network
# - other cleanup
#
# Revision 1.2  2007/06/07 21:23:03  mjk
# - command derive from verb.command class
# - default is MustBeRoot
# - list.command / dump.command set MustBeRoot = 0
# - removed plugin non-bugfix
#
# Revision 1.1  2007/05/30 20:10:53  anoop
# Added rocks add subnet - Command adds a subnet to the subnets table
# in the database. Is currently beta

import rocks.commands


class Command(rocks.commands.NetworkArgumentProcessor,
	rocks.commands.set.command):
	"""
	Sets the network mask for one or more named networks .

	<arg type='string' name='network' repeat='1'> 
	One or more named networks that should have the defined netmask.
	</arg>
	
	<arg type='string' name='netmask'>
	Netmask that named networks should have.
	</arg>
	
	<param type='string' name='netmask'>
	Can be used in place of netmask argument.
	</param>

	<example cmd='set network netmask optiputer 255.255.255.0'>
	Sets the netmask for the "optiputer" network to a class-c address
	space.
	</example>

	<example cmd='set network netmask optiputer netmask=255.255.255.0'>
	Same as above.
	</example>

	<example cmd='set network netmask optiputer cavewave 255.255.0.0'>
	Sets the netmask for the "optiputer" and "cavewave" networks to
	a class-b address space.
	</example>
	
	<related>add network</related>
	<related>set network subnet</related>
	"""

        def run(self, params, args):
        	(args, netmask) = self.fillPositionalArgs(('netmask',))
        	
        	if not len(args):
        		self.abort('must supply network')
		if not netmask:
			self.abort('must supply netmask')
			        	
        	for network in self.getNetworkNames(args):
			self.db.execute("""update subnets set netmask='%s' where
				subnets.name='%s'""" % (netmask, network))

