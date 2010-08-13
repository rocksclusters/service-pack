ROLL			= service-pack
NAME    		= roll-$(ROLL)-usersguide
VERSION			= 5.3.1
RELEASE 		= 0

RPM.ARCH		= noarch

SUMMARY_COMPATIBLE	= $(VERSION)
SUMMARY_MAINTAINER	= Rocks Group
SUMMARY_ARCHITECTURE	= i386, x86_64

ROLL_REQUIRES		= base kernel service-pack
ROLL_CONFLICTS		=

