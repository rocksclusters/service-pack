#
# $Id: Makefile,v 1.17 2013/02/08 02:30:29 clem Exp $
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
# $Log: Makefile,v $
# Revision 1.17  2013/02/08 02:30:29  clem
# adding new version of zfs
#
# when simple things make your life impossible, half a day behind this stupid
# addition....
#
# Revision 1.16  2013/02/06 01:15:18  clem
# Needs to mkdir all the directory for the RPMS
#
# Revision 1.15  2013/02/05 17:27:27  clem
# added the bio/perl stuff to the service-pack
#
# some minor reformatting
#
# Revision 1.14  2013/02/02 07:22:18  clem
# now it properly compiles all the required packages
#
# Revision 1.13  2012/11/27 00:49:12  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.12  2012/05/06 05:49:20  phil
# Copyright Storm for Mamba
#
# Revision 1.11  2011/07/23 02:31:17  phil
# Viper Copyright
#
# Revision 1.10  2010/12/07 23:52:15  bruno
# the start of SP 5.4.1
#
# Revision 1.9  2010/09/07 23:53:24  bruno
# star power for gb
#
# Revision 1.8  2009/08/12 23:02:45  bruno
# fixes for 5.2.2
#
# Revision 1.6  2009/05/01 19:07:22  mjk
# chimi con queso
#
# Revision 1.5  2008/10/18 00:56:13  mjk
# copyright 5.1
#
# Revision 1.4  2008/03/06 23:41:57  mjk
# copyright storm on
#
# Revision 1.3  2007/06/23 04:04:00  mjk
# mars hill copyright
#
# Revision 1.2  2006/12/13 23:17:17  bruno
# add the mechanism to disable all previous service-pack rolls and enable
# the latest one.
#
# this is needed when installing the service-pack roll on-the-fly and when
# a previous version of the service-pack roll is present.
#
# Revision 1.1  2006/10/06 23:33:45  bruno
# first draft
#
#


PROFILES = condor base ganglia zfs-linux
ROCKSROOT.ABSOLUTE = $(shell cd $(ROCKSROOT); pwd)
ARCH.BIN = $(ROCKSROOT.ABSOLUTE)/bin/arch
ARCH = $(shell $(ARCH.BIN))


roll::
	mkdir -p RPMS/noarch;
	mkdir -p RPMS/$(ARCH);
	for i in $(PROFILES); do\
		bash buildprofile.sh $$i||exit2;\
	done

-include $(ROLLSROOT)/etc/Rolls.mk
include Rolls.mk



clean::
	rm -f _arch
