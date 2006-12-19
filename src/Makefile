# $Id: Makefile,v 1.3 2006/12/19 22:21:50 bruno Exp $
#
# @Copyright@
# 
# 				Rocks
# 		         www.rocksclusters.org
# 		        version 4.2.1 (Cydonia)
# 
# Copyright (c) 2006 The Regents of the University of California. All
# rights reserved.
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
# 	"This product includes software developed by the Rocks 
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".
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

PKGS		= roll-kernel-mini-httpd roll-kernel-rocks-boot \
			roll-base-rocks-bittorrent roll-base-anaconda
SRCDIRS		= usersguide

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
roll-kernel-rocks-boot:	roll-kernel-mini-httpd
	mkdir $@
	(cd $@; cp -R ../../../kernel/src/rocks-boot/* . ; make rpm)

roll-kernel-mini-httpd:
	mkdir $@
	(cd $@; cp -R ../../../kernel/src/mini_httpd/* . ; make rpm)

roll-base-anaconda:	roll-base-rocks-bittorrent
	mkdir $@
	(cd $@; cp -R ../../../base/src/anaconda/* .)
	(cd $@/updates.img; make rpm)

roll-base-rocks-bittorrent:
	mkdir $@
	(cd $@; cp -R ../../../base/src/bittorrent/* . ; make rpm)

