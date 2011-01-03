#
# $Id: Makefile,v 1.1 2011/01/03 19:00:30 bruno Exp $
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
# $Log: Makefile,v $
# Revision 1.1  2011/01/03 19:00:30  bruno
# fixed a memory leak in gmetric.
#
# every time we called the gmetric method, it would call a function that
# parsed gmond.conf and that function would allocate memory to store the parsed
# data. we need to free that structure after the metric is sent.
#
#

ARCH=`uname -i`
REDHAT.ROOT	= ../../../../../../../../
PATCH_ROLL_NAME	= base
PATCH_PKG_NAME	= ganglia-pylib


include ../../sp-version.mk

rpm:
	if [ "$(USER)" == "root" ] ; \
	then \
		echo ;\
		echo -e "\tERROR : to build this package, you need to set" ;\
		echo -e "\tthe USER environmental variable to user other" ;\
		echo -e "\tthan 'root'." ;\
		echo -e "\tThis is because a CVS checkout is performed" ;\
		echo -e "\tduring the building of this package." ;\
		echo ;\
		exit -1 ;\
	fi

	cvs -d $(USER)@fyp.rocksclusters.org:/home/cvs/CVSROOT checkout	\
		-r ROCKS_5_4 \
		rocks/src/roll/$(PATCH_ROLL_NAME)/src/$(PATCH_PKG_NAME)
	cd patch-files && find . -type f | grep -v CVS | cpio -pduv ../
	(cd rocks/src/roll/$(PATCH_ROLL_NAME)/src/$(PATCH_PKG_NAME); \
		mkdir -p ../../RPMS/$(ARCH) ;\
		make SP_VERSION=$(SP_VERSION) clean rpm ;\
		mkdir -p $(REDHAT.ROOT)/RPMS/$(ARCH)/ ;\
		cp ../../RPMS/$(ARCH)/*rpm $(REDHAT.ROOT)/RPMS/$(ARCH)/ ;\
	)

clean::
	rm -rf rocks

