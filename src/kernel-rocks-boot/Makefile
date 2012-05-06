#
# $Id: Makefile,v 1.3 2012/05/06 05:49:41 phil Exp $
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
# $Log: Makefile,v $
# Revision 1.3  2012/05/06 05:49:41  phil
# Copyright Storm for Mamba
#
# Revision 1.2  2011/07/23 02:31:33  phil
# Viper Copyright
#
# Revision 1.1  2010/12/14 19:33:24  bruno
# add the new tracker client into initrd inside the rocks-boot RPMS.
#
# also, make it easy to change the version number of the service pack roll and
# have all the RPMs 'release' number match the version number of the roll
#
#

ARCH=`uname -i`
REDHAT.ROOT	= ../../../../../../../../

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
		-r ROCKS_5_4 rocks/src/roll/kernel/src/rocks-boot
	cd patch-files && find . -type f | grep -v CVS | cpio -pduv ../
	(cd rocks/src/roll/kernel/src/rocks-boot ; 			\
		mkdir -p ../../RPMS/$(ARCH) ;\
		cp $(REDHAT.ROOT)/RPMS/$(ARCH)/rocks-tracker*rpm \
			../../RPMS/$(ARCH)/ ;\
		make SP_VERSION=$(SP_VERSION) clean rpm ;\
		pwd ; \
		cp ../../RPMS/$(ARCH)/*rpm $(REDHAT.ROOT)/RPMS/$(ARCH)/ ;\
	)

clean::
	rm -rf rocks

