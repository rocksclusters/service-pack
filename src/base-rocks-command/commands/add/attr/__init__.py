# $Id: __init__.py,v 1.3 2011/07/23 02:31:18 phil Exp $
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
# Revision 1.3  2011/07/23 02:31:18  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:14  bruno
# get the right commands
#
# Revision 1.4  2010/09/07 23:52:50  bruno
# star power for gb
#
# Revision 1.3  2010/07/31 01:02:02  bruno
# first stab at putting in 'shadow' values in the database that non-root
# and non-apache users can't read
#
# Revision 1.2  2009/11/18 23:34:49  bruno
# cleanup help section
#
# Revision 1.1  2009/06/19 21:07:21  mjk
# - added dumpHostname to dump commands (use localhost for frontend)
# - added add commands for attrs
# - dump uses add for attr (does not overwrite installer set attrs)A
# - do not dump public or private interfaces for the frontend
# - do not dump os/arch host attributes
# - fix various self.about() -> self.abort()
#

import stat
import time
import sys
import string
import rocks.commands

class Command(rocks.commands.add.command):
	"""
	Adds a global attribute for all nodes

	<arg type='string' name='attr'>
	Name of the attribute
	</arg>

	<arg type='string' name='value'>
	Value of the attribute
	</arg>
	
	<param type='string' name='attr'>
	same as attr argument
	</param>

	<param type='string' name='value'>
	same as value argument
	</param>

	<example cmd='add attr sge False'>
	Adds the sge attribution and sets it to False.
	</example>

	<related>list attr</related>
	<related>remove attr</related>
	"""

	def run(self, params, args):

		(args, attr, value) = self.fillPositionalArgs(('attr', 'value'))
		if not attr:
			self.abort('missing attribute name')
		if not value:
			self.abort('missing value of attribute')

		rows = self.db.execute("""select * from global_attributes
			where attr='%s'""" % attr)
		if rows:
			self.abort('attribute "%s" exists' % attr)

		shadow, = self.fillParams([ ('shadow', 'n') ])

		if self.str2bool(shadow):
			s = "'%s'" % value
			v = 'NULL'
		else:
			s = 'NULL'
			v = "'%s'" % value

		self.db.execute("""insert into global_attributes
			values ('%s', %s, %s)""" % (attr, v, s))

