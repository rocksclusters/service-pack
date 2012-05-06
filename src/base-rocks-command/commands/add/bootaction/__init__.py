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
# Revision 1.3  2011/07/23 02:31:18  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:14  bruno
# get the right commands
#
# Revision 1.4  2010/09/07 23:52:50  bruno
# star power for gb
#
# Revision 1.3  2010/04/14 14:40:26  bruno
# changed 'host bootaction' to 'bootaction' in the documentation portion of
# the commands
#
# Revision 1.2  2009/05/01 19:06:54  mjk
# chimi con queso
#
# Revision 1.1  2009/02/12 21:40:05  bruno
# make the bootaction global
#
#

import sys
import string
import rocks.commands
import os

class Command(rocks.commands.HostArgumentProcessor, rocks.commands.add.command):
	"""
	Add a bootaction specification to the system.
	
	<param type='string' name='action'>
	Label name for the bootaction. You can see the bootaction label names by
	executing: 'rocks list bootaction [host(s)]'.
	</param>
	
	<param type='string' name='kernel'>
	The name of the kernel that is associated with this boot action.
	</param>

	<param type='string' name='ramdisk'>
	The name of the ramdisk that is associated with this boot action.
	</param>
	
	<param type='string' name='args'>
	The second line for a pxelinux definition (e.g., ks ramdisk_size=150000
	lang= devfs=nomount pxe kssendmac selinux=0)
	</param>
	
	<example cmd='add bootaction action=os kernel="localboot 0"'>
	Add the 'os' bootaction.
	</example>
	
	<example cmd='add bootaction action=memtest command="memtest"'>
	Add the 'memtest' bootaction.
	</example>
	"""

	def addBootAction(self, action, kernel, ramdisk, bootargs):
		#
		# is there already an entry in the bootaction table
		#
		rows = self.db.execute("""select id from bootaction where
			action = '%s'""" % (action))
		if rows < 1:
			#
			# insert a new row
			#
			cols = {}
			cols['action'] = '"%s"' % (action)

			if kernel != None:
				cols['kernel'] = '"%s"' % (kernel)
			if ramdisk != None:
				cols['ramdisk'] = '"%s"' % (ramdisk)
			if bootargs != None:
				cols['args'] = '"%s"' % (bootargs)

			self.db.execute('insert into bootaction '
				'(%s) ' % (string.join(cols.keys(), ',')) + \
				'values '
				'(%s) ' % (string.join(cols.values(), ',')))
		else:
			#
			# update the existing row
			#
			bootactionid, = self.db.fetchone()

			query = 'update bootaction set action = "%s" ' \
				% (action)

			if kernel != None:
				query += ', kernel = "%s" ' % (kernel) 
			if ramdisk != None:
				query += ', ramdisk = "%s" ' % (ramdisk) 
			if bootargs != None:
				query += ', args = "%s" ' % (bootargs)

			query += 'where id = %s' % (bootactionid)

			self.db.execute(query)

		return


	def run(self, params, args):
		(action, kernel, ramdisk, bootargs) = self.fillParams(
			[('action', ), 
			('kernel', ),
			('ramdisk', ),
			('args', )])
			
		if not action:
			self.abort('must supply an action')

		self.addBootAction(action, kernel, ramdisk, bootargs)

		#	
		# regenerate all the pxe boot configuration files
		# including the default.
		#
		self.command('set.host.boot', self.getHostnames())

