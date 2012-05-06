# $Id: plugin_dns.py,v 1.4 2012/05/06 05:49:41 phil Exp $
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
# $Log: plugin_dns.py,v $
# Revision 1.4  2012/05/06 05:49:41  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:33  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:13:27  bruno
# get the right commands
#
# Revision 1.19  2010/09/07 23:53:03  bruno
# star power for gb
#
# Revision 1.18  2010/07/27 20:24:38  bruno
# bug fixes
#
# Revision 1.17  2010/06/30 17:37:33  anoop
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
# Revision 1.16  2009/06/26 19:02:15  bruno
# alias fix.
#
# thanks to Mike Hallock of UIUC for the fix.
#
# Revision 1.15  2009/05/26 23:04:42  bruno
# mo' bugs
#
# Revision 1.14  2009/05/26 21:36:48  bruno
# fix from scott hamilton for subnets that have prefixes larger than 24 bits.
#
# Revision 1.13  2009/05/01 19:07:04  mjk
# chimi con queso
#
# Revision 1.12  2009/03/21 22:22:55  bruno
#  - lights-out install of VM frontends with new node_rolls table
#  - nuked 'site' columns and tables from database
#  - worked through some bugs regarding entities
#
# Revision 1.11  2009/03/13 21:19:16  bruno
# no more riding the shortname
#
# Revision 1.10  2009/03/04 21:31:44  bruno
# convert all getGlobalVar to getHostAttr
#
# Revision 1.9  2008/10/18 00:55:58  mjk
# copyright 5.1
#
# Revision 1.8  2008/09/22 18:34:31  bruno
# vlan fix for the case where a vlan interface is configured with and IP
# but with no hostname
#
# Revision 1.7  2008/08/29 22:12:35  bruno
# fix for reverse.rocks.domain.*.local
#
# Revision 1.6  2008/07/22 00:34:41  bruno
# first whack at vlan support
#
# Revision 1.5  2008/03/06 23:41:40  mjk
# copyright storm on
#
# Revision 1.4  2008/02/19 23:20:24  bruno
# katz made me do it.
#
# Revision 1.3  2007/09/14 18:48:24  bruno
# if there is no short name for an appliance, then don't make an alias for
# it in /var/named/rocks.domain
#
# Revision 1.2  2007/08/08 22:23:34  bruno
# also import reverse domain local entries
#
# Revision 1.1  2007/08/08 22:14:41  bruno
# moved 'dbreport named' and 'dbreport dns' to rocks command line
#
#

import rocks.commands
import subprocess

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'dns'

	def run(self, args):
		o = self.owner.command('report.zones', [])
		p1 = subprocess.Popen(
			['/opt/rocks/bin/rocks','report','script'], 
			stdin=subprocess.PIPE, stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)
		out = p1.communicate(o)[0]
		p2 = subprocess.Popen(['/bin/sh'], stdin=subprocess.PIPE,
			stdout=None, stderr=None)

		p2.communicate(out)
