# $Id: plugin_wordpress.py,v 1.1 2010/12/07 23:52:30 bruno Exp $
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
# $Log: plugin_wordpress.py,v $
# Revision 1.1  2010/12/07 23:52:30  bruno
# the start of SP 5.4.1
#
# Revision 1.5  2010/09/07 23:53:02  bruno
# star power for gb
#
# Revision 1.4  2010/07/08 23:45:18  bruno
# password setting fixes
#
# Revision 1.3  2009/09/30 19:44:05  bruno
# make sure password changing code accesses the rocks foundation database
#
# Revision 1.2  2009/05/01 19:07:04  mjk
# chimi con queso
#
# Revision 1.1  2009/02/10 20:41:46  bruno
# change the root password for various cluster services
#
#

import MySQLdb
import rocks.password
import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'wordpress'


	def run(self, args):
		if len(args) != 2:
			return

		old_password = args[0]
		new_password = args[1]

		#
		# create a new password
		#
		pw = rocks.password.Password()
		newpw = pw.create_password(new_password)

		try:
			#
			# now update the password in the 'wordpress' database
			#
			link = MySQLdb.connect(host='localhost', user='root',
				db='wordpress', passwd='%s' % old_password,
				unix_socket='/var/opt/rocks/mysql/mysql.sock')

			cursor = link.cursor()

			sqlcmd = """update wp_users set user_pass = '%s' where
				user_login = 'admin' """ % (newpw)

			cursor.execute(sqlcmd)
		except:
			#
			# if we can't connect to the wordpress database, then
			# just continue
			#
			pass

		#
		# store it in the rocks database
		# 
		self.owner.command('set.attr',
			[ 'Kickstart_PrivatePortableRootPassword', newpw ] )

