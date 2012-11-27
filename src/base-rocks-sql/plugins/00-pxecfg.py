#
# insert-ethers plugin module for generating pxelinux cfg files

# $Id: 00-pxecfg.py,v 1.5 2012/11/27 00:49:30 phil Exp $
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
# $Log: 00-pxecfg.py,v $
# Revision 1.5  2012/11/27 00:49:30  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/05/06 05:49:41  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:33  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:14:38  bruno
# get the right files
#
# Revision 1.9  2010/09/07 23:53:09  bruno
# star power for gb
#
# Revision 1.8  2009/05/08 22:20:05  anoop
# uses the node_attributes table to determine the OS to be installed on the
# node, instead of the nodes table.
# Also uses the new command line tools
#
# Revision 1.7  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.6  2008/12/17 00:19:21  anoop
# insert-ethers plugin now uses rocks add host bootaction instead of pxeaction
#
# Revision 1.5  2008/12/15 22:27:22  bruno
# convert pxeboot and pxeaction tables to boot and bootaction tables.
#
# this enables merging the pxeaction and vm_profiles tables
#
# Revision 1.4  2008/10/18 00:56:03  mjk
# copyright 5.1
#
# Revision 1.3  2008/09/18 17:44:13  bruno
# fix bruno bug
#
# Revision 1.2  2008/09/09 23:10:46  bruno
# added some solaris/sunos changes for anoop
#
# Revision 1.1  2008/08/28 18:12:45  anoop
# Now solaris installations use pxelinux to chainload pxegrub. This
# way we can keep generation of pxelinux files controlled through
# "rocks add host pxeaction" and thus keep the content of
# pxelinux files consistent and managed.
#

import os
import sys
import string
import rocks.sql
import popen2

class Plugin(rocks.sql.InsertEthersPlugin):
	"Controls the PXE configuration when nodes are added and removed."

	def added(self, nodename, id):
		cmd = ("/opt/rocks/bin/rocks report "
			"host attr %s | grep os\: | "
			"cut -f2 -d:" %(nodename))
		r,w = popen2.popen2(cmd)
		w.close()
		osname = r.read().strip()
		if osname == 'sunos':
			for action in [ 'install_sol', 'rescue_sol' ]:
				cmd = ("/opt/rocks/bin/rocks add "
					"bootaction action='%s' " 
					"kernel='kernel pxegrub.0'"
					%(action))

				os.system(cmd)

			cmd  = ('/opt/rocks/bin/rocks set '
				'host installaction '
				'%s install_sol'% (nodename))
			os.system(cmd)

		os.system("/opt/rocks/bin/rocks set host boot " + \
			"%s action=%s" % (nodename, "install"))

	def removed(self, nodename, id):
		pass

	def update(self):
		pass

	def done(self):
		pass

	def restart(self):
		pass

