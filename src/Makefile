# $Id: Makefile,v 1.8 2009/07/18 00:17:50 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# Revision 1.8  2009/07/18 00:17:50  bruno
# push the changes made the mecurial repository back into the cvs one.
#
# this is the code for SP 5.2.1
#
# Revision 1.7  2009/05/01 19:07:22  mjk
# chimi con queso
#
# Revision 1.6  2008/10/18 00:56:13  mjk
# copyright 5.1
#
# Revision 1.5  2008/03/06 23:41:57  mjk
# copyright storm on
#
# Revision 1.4  2007/06/23 04:04:00  mjk
# mars hill copyright
#
# Revision 1.3  2006/12/19 22:21:50  bruno
# get the dependencies right
#
# Revision 1.2  2006/12/16 21:01:31  bruno
# more goodies for the service pack roll
#
# Revision 1.1  2006/10/06 23:33:45  bruno
# first draft
#
#

PKGS		= roll-area51-profile roll-area51-tripwire-config \
			roll-area51-tripwire roll-base-profile\
			roll-base-command roll-base-sql roll-base-kickstart \
			roll-ganglia-ganglia \
			roll-ganglia-monitor-core roll-ganglia-rocks-command \
			roll-ganglia-webfrontend-addons roll-sge-ganglia \
			roll-xen-rocks-command
SRCDIRS		= usersguide
RELEASE		= 5.2.1

default:	rpm

copyright rpm::	$(PKGS)
	for i in $(SRCDIRS) ; do \
		(cd $$i; make $@) ; \
	done

clean::
	for i in $(SRCDIRS) ; do \
		(cd $$i; make $@) ; \
	done
	rm -rf $(PKGS) $(EXTRA_PKGS)

#
# this is a bit messy, but order matters
#
roll-area51-profile:
	mkdir -p ../RPMS/noarch
	(								\
		cd ../../area51 ;					\
		make ROLLNAME=area51 RELEASE=$(RELEASE) profile 	\
	)
	cp ../../area51/RPMS/noarch/roll-area51-kickstart*rpm ../RPMS/noarch/

roll-area51-tripwire-config:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../area51/src/tripwire-config/* . ;		\
		make RELEASE=$(RELEASE) rpm				\
	)

roll-area51-tripwire:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../area51/src/tripwire/* . ;		\
		make RELEASE=$(RELEASE) rpm				\
	)

roll-base-profile:
	mkdir -p ../RPMS/noarch
	(								\
		cd ../../base ;						\
		make ROLLNAME=base RELEASE=$(RELEASE) profile ;		\
	)
	cp ../../base/RPMS/noarch/roll-base-kickstart*rpm ../RPMS/noarch/

roll-base-command:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../base/src/command/* . ;			\
		make RELEASE=$(RELEASE) rpm				\
	)

roll-base-sql:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../base/src/sql/* . ;			\
		make RELEASE=$(RELEASE) rpm				\
	)

roll-base-kickstart:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../base/src/kickstart/* . ;			\
		make RELEASE=$(RELEASE) rpm				\
	)

roll-ganglia-ganglia:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../ganglia/src/ganglia/* . ;		\
		make RELEASE=$(RELEASE) rpm				\
	)

roll-ganglia-monitor-core:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../ganglia/src/monitor-core/* . ;		\
		make RELEASE=$(RELEASE) rpm				\
	)
roll-ganglia-rocks-command:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../ganglia/src/rocks-command/* . ;		\
		make RELEASE=$(RELEASE) rpm				\
	)

roll-ganglia-webfrontend-addons:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../ganglia/src/webfrontend-addons/* . ;	\
		make RELEASE=$(RELEASE) rpm				\
	)

roll-sge-ganglia:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../sge/src/ganglia/* . ;			\
		make RELEASE=$(RELEASE) rpm				\
	)

roll-xen-rocks-command:
	mkdir $@
	(								\
		cd $@ ;							\
		cp -R ../../../xen/src/rocks-command/* . ;		\
		make RELEASE=$(RELEASE) rpm				\
	)

