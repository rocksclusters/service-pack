#!/bin/bash
#
# Script to backup the mysql Cluster database, and 
# check in changes to RCS.
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
# $Log: backup-cluster-db.sh,v $
# Revision 1.4  2012/05/06 05:49:41  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2011/07/23 02:31:33  phil
# Viper Copyright
#
# Revision 1.2  2010/12/08 00:14:38  bruno
# get the right files
#
# Revision 1.13  2010/09/07 23:53:09  bruno
# star power for gb
#
# Revision 1.12  2009/05/14 23:41:12  bruno
# change the database backup to use the foundation
#
# Revision 1.11  2009/05/01 19:07:09  mjk
# chimi con queso
#
# Revision 1.10  2008/10/18 00:56:03  mjk
# copyright 5.1
#
# Revision 1.9  2008/03/06 23:41:45  mjk
# copyright storm on
#
# Revision 1.8  2007/07/15 01:39:17  phil
# explicitly set HOME so that the connection to mysql can done using
# root's .my.cnf file, which contains the apache password.
#
# Revision 1.7  2007/06/23 04:03:25  mjk
# mars hill copyright
#
# Revision 1.6  2006/09/11 22:47:28  mjk
# monkey face copyright
#
# Revision 1.5  2006/08/10 00:09:45  mjk
# 4.2 copyright
#
# Revision 1.4  2005/10/12 18:08:46  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:02:25  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:22:00  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:03:17  mjk
# moved from core to base
#
# Revision 1.1  2004/04/13 03:21:05  fds
# Daily mysql cluster backup to RCS (phil's idea).
#
#

export HOME=/root
cd /var/db

/opt/rocks/bin/mysqldump -u apache --opt cluster > mysql-backup-cluster

# To check in multiple versions, you need to have a lock on the
# file. RCS will automatically ignore checkins for unchanged files.
ci -l -t-'Rocks Cluster Database' -m`date +"%Y-%m-%d"` mysql-backup-cluster > /dev/null 2>&1
