# $Id: __init__.py,v 1.1 2010/12/07 23:52:20 bruno Exp $
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
# Revision 1.1  2010/12/07 23:52:20  bruno
# the start of SP 5.4.1
#
# Revision 1.5  2010/09/07 23:52:53  bruno
# star power for gb
#
# Revision 1.4  2010/05/20 00:31:44  bruno
# gonna get some serious 'star power' off this commit.
#
# put in code to dynamically configure the static-routes file based on
# networks (no longer the hardcoded 'eth0').
#
# Revision 1.3  2009/06/19 21:07:34  mjk
# - added dumpHostname to dump commands (use localhost for frontend)
# - added add commands for attrs
# - dump uses add for attr (does not overwrite installer set attrs)A
# - do not dump public or private interfaces for the frontend
# - do not dump os/arch host attributes
# - fix various self.about() -> self.abort()
#
# Revision 1.2  2009/05/01 19:06:57  mjk
# chimi con queso
#
# Revision 1.1  2009/03/13 21:10:49  mjk
# - added dump route commands
#


import rocks.commands


class Command(rocks.commands.dump.host.command):
	"""
	"""

	def run(self, params, args):
		for host in self.getHostnames(args):
			self.db.execute("""
				select r.network, r.netmask, r.gateway,
				r.subnet from node_routes r, nodes n where
				r.node=n.id and n.name='%s'""" % host)

			for n, m, g, s in self.db.fetchall():
				if s:
					rows = self.db.execute("""select name
						from subnets where id = %s"""
						% s)
					if rows == 1:
						g, = self.db.fetchone()

				self.dump('add host route %s %s %s netmask=%s'
					% (self.dumpHostname(host), n, g, m))

