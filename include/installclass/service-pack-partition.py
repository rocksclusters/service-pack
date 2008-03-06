# $Id: service-pack-partition.py,v 1.3 2008/03/06 23:41:57 mjk Exp $
#
# Manipulate RedHat installer for disk partitioning.
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# $Log: service-pack-partition.py,v $
# Revision 1.3  2008/03/06 23:41:57  mjk
# copyright storm on
#
# Revision 1.2  2007/06/23 04:04:00  mjk
# mars hill copyright
#
# Revision 1.1  2006/12/13 22:49:59  bruno
# fix for the /tmp/sdb error dialog window problem.
#
# this is the problem that had the workaround of specifying 'nousbstorage'
# on the command line.
#
# Revision 1.29  2006/09/11 22:46:57  mjk
# monkey face copyright
#
# Revision 1.28  2006/08/10 00:09:24  mjk
# 4.2 copyright
#
# Revision 1.27  2006/07/12 22:17:17  bruno
# take steps to make sure the rpm database is cleared before we install
# packages. this addresses the issue we saw with the initscripts package and
# how it wasn't creating all the appropriate links under /etc/rc.d/
#
# Revision 1.26  2006/06/22 22:10:13  bruno
# added a 4 GB /var partition
# bumped root to 8 GB
#
# Revision 1.25  2006/02/28 19:54:09  bruno
# better array length checking
#
# Revision 1.24  2005/11/30 19:31:32  bruno
# software raid fixes
#
# Revision 1.23  2005/11/20 01:33:45  bruno
# more partitioning fixes
#
# Revision 1.22  2005/10/26 03:45:26  bruno
# add 'gptDrive' method that determines if a drive is using GPT as its
# partition method. currently GPT is used on some itaniums, but not all.
#
# thanks to roy dragseth for access to his ia64 test cluster in order to
# develop the fix.
#
# Revision 1.21  2005/10/12 18:08:28  mjk
# final copyright for 4.1
#
# Revision 1.20  2005/10/10 18:13:35  bruno
# more software raid corner case handling
#
# Revision 1.19  2005/10/07 18:05:39  bruno
# more software raid corner case fixes
#
# Revision 1.18  2005/09/30 20:52:28  bruno
# support for only partitioning the first drive.
#
# this is the default for frontends.
#
# for all other nodes, the user can specify the flag
# 'force-default-root-disk-only' in between the part XML tags.
#
# Revision 1.17  2005/09/28 22:46:27  bruno
# bug fixes for frontend installs with mixed IDE and SCSI drives including
# some of these drives being configured as software RAID(s).
#
# Revision 1.16  2005/09/19 22:08:35  bruno
# partitioning tuning.
#
# - the frontend and NAS appliance will no longer nuke all partitions before
#   the partitioning screen
# - a NAS appliance always displays the partitioning screen
# - added a nas-exports node to make it easier for people to customize
#   their export directories on NAS appliances
# - hardened the software raid partitioning code
#
# Revision 1.15  2005/09/16 01:02:08  mjk
# updated copyright
#
# Revision 1.14  2005/08/31 23:11:46  bruno
# harden up the code that tries to send the node's partition info back to
# the frontend
#
# Revision 1.13  2005/08/06 22:40:52  bruno
# make a null entry in case if a disk has no partitions.
#
# this starts the enables the partition matching code to start.
#
# Revision 1.12  2005/07/27 01:54:36  bruno
# checkpoint
#
# Revision 1.11  2005/07/20 20:56:43  bruno
# the second half of the fix for bug 150.
#
# Revision 1.9  2005/06/22 17:02:27  bruno
# software raid reinstallation fix
#
# Revision 1.8  2005/05/24 21:21:47  mjk
# update copyright, release is not any closer
#
# Revision 1.7  2005/04/29 05:06:35  bruno
# partitioning once again works on i386/x86_64 (instability was caused by
# the ia64 checkins).
#
# Revision 1.6  2005/04/28 21:47:23  bruno
# partitioning function updates in order to support itanium.
#
# itanics need 'parted' as 'sfdisk' only looks at block 0 on a disk and
# itanics put their real partition info in block 1 (this is the GPT partitioning
# scheme)
#
# Revision 1.5  2005/04/14 23:24:29  bruno
# make sure fstype and mountpoint are labeled 'swap' -- this makes sure the
# database values for swap match those on the physical node.
#
# Revision 1.4  2005/04/14 17:06:39  bruno
# fixes for ia64 disk partitioning
#
# Revision 1.3  2005/04/13 01:36:42  fds
# Less verbose, and unhide USB devices when we need to.
#
# Revision 1.2  2005/04/12 01:53:59  fds
# Fix USB installs on linux 2.6.
#
# Revision 1.1  2005/03/18 00:14:08  fds
# Moved Bruno's Partition classes to their own partition.py file. Added
# support functions for USB keys. All nodes run a postAction() now.
#
# Revision 1.4  2005/03/15 23:54:51  bruno
# force-default fixes
#
# Revision 1.3  2005/03/14 19:27:49  bruno
# harden up the posting of partitions to the frontend's database
#
# Revision 1.2  2005/03/12 00:01:50  bruno
# minor checkin
#
# Revision 1.1  2005/03/01 00:22:25  mjk
# moved to base roll
#
# Revision 1.20  2005/02/14 21:55:01  bruno
# support for phil's phartitioning phun

import sys
import os
import os.path
import string
import tempfile
import isys
from userauth_text import *
from kickstart import *
from text import *
from product import *
from dispatch import installSteps

#
# default file system type
#
fstype = 'ext3'		

import re

class RocksPartition:

	mountpoints = []
	unknown_disks = []
	sfdisk = ''
	e2label = ''
	saved_fstab = ''
	baseinstclass = None
	raidinfo = []
	skipdevices = []

	
	def skipDevice(self, dev):
		if dev and dev not in self.skipdevices:
			self.skipdevices.append(dev)


	def findMntInFstab(self, identifier):
		if not os.path.exists(self.saved_fstab):
			return ''

		file = open(self.saved_fstab, 'r')
		lines = file.readlines()
		file.close()

		for line in lines:
			l = string.split(line)
			if len(l) > 0:
				if l[0] == identifier:
					return l[1]

		return ''


	def findFsTypeInFstab(self, mntpoint):
		if not os.path.exists(self.saved_fstab):
			return ''

		file = open(self.saved_fstab, 'r')
		lines = file.readlines()
		file.close()

		for line in lines:
			l = string.split(line)
			if len(l) > 2:
				if l[1] == mntpoint:
					return l[2]

		return ''


	def getRaidInfo(self):
		import isys
		import raid
		import partedUtils

		diskset = partedUtils.DiskSet()
		diskset.openDevices()

		#
		# get a list of non-skipped drives
		#
		drives = []
		for drive in isys.hardDriveDict().keys():
			if not drive in diskset.skippedDisks:
				drives.append(drive)

		try:
			self.raidinfo = raid.startAllRaid(drives)
		except:
			pass

		log('ROCKS:getRaidInfo:raidinfo:%s ' % (self.raidinfo))

		diskset.closeDevices()

		return

	
	def stopRaid(self):
		import raid

		try:
			raid.stopAllRaid(self.raidinfo)
		except:
			pass

		return


	def sortDisks(self, x, y):
		#
		# make sure software raid partition specifications are last
		#
		if len(x) > 1 and x[0:2] == 'md':
			return 1
		if len(y) > 1 and y[0:2] == 'md':
			return -1

		return 0
		

	def getRaidDevice(self, partition_device):
		raiddevice = ''

		for info in self.raidinfo:
			if len(info) > 3:
				(device, partitions, raidlevel,
							num_partitions) = info

				if partition_device in partitions:
					raiddevice = device
					break

		return raiddevice


	def getRaidName(self, partition_device):
		raidname = ''

		for info in self.raidinfo:
			if len(info) > 3:
				(device, partitions, raidlevel,
							num_partitions) = info

				if partition_device in partitions:
					raidname = 'raid.%s' % partition_device
					break

		return raidname


	def getRaidPartitions(self, raid_device):
		raidparts = ''

		for info in self.raidinfo:
			if len(info) > 3:
				(device, partitions, raidlevel,
							num_partitions) = info

				if raid_device == device and \
							len(partitions) > 0:

					for part in partitions:
						raidparts += 'raid.%s ' % (part)

					break

		return raidparts


	def getRaidLevel(self, raid_device):
		level = -1

		for info in self.raidinfo:
			if len(info) > 3:
				(device, partitions, raidlevel,
							num_partitions) = info

				if raid_device == device:
					level = raidlevel
					break

		return level


	def getRaidMountPoint(self, raidpartition):
		raidmountpoint = ''

		raiddevice = self.getRaidDevice(raidpartition)
		log('ROCKS:getRaidMountPoint:raiddevice: %s' % (raiddevice))

		nodepartinfo = self.getNodePartInfo()
		log('ROCKS:getRaidMountPoint:nodepartinfo: %s' % (nodepartinfo))

		if not nodepartinfo.has_key(raiddevice):
			return ''

		for node in nodepartinfo[raiddevice]:
			if len(node) == 1:
				continue

			(nodedevice, nodesectorstart, nodepartsize,
				nodepartid, nodefstype, nodebootflags,
				 nodepartflags, nodemntpoint) = node

			if nodedevice == raiddevice:
				raidmountpoint = nodemntpoint
				break

		log('ROCKS:getRaidMountPoint:raidmountpoint: %s' %
							(raidmountpoint))

		return raidmountpoint


	def getPartitionDevices(self):
		devnames = []

		file = open('/proc/partitions', 'r')
		lines = file.readlines() 
		file.close()

		for line in lines[2:]:
			tokens = string.split(line)

			if len(tokens) > 3:
				major = tokens[0]       
				minor = tokens[1]
				blocks = tokens[2]
				devname = tokens[3]

				if devname in self.skipdevices:
					continue
				
				if devname != '':
					devnames.append(devname)

		return devnames


	def getDisks(self):
		#
		# make sure the software raid info is loaded
		#
		self.getRaidInfo()

		disks = []
		for devname in self.getPartitionDevices():
			#
			# find all the device names (not partition names)
			#
			addit = 1
			for disk in disks:
				if len(disk) <= len(devname) and \
						disk == devname[0:len(disk)]:
					addit = 0
					break

			if addit:
				disks.append(devname)

		#
		# make sure the software raid devices are at the end of
		# the list. we do this by sorting them.
		#
		disks.sort(self.sortDisks)

		log('ROCKS:getDisks:disks:%s ' % (disks))

		return disks


	def isRaidStarted(self):
		for devname in self.getPartitionDevices():
			if len(devname) > 2 and devname[0:2] == 'md':
				return 1

		return 0


	def getDevice(self, str):
		device = ''

		a = string.split(str, '/dev/')
		if len(a) > 1:
			device = a[1]

		return string.strip(device)


	def getSectorStart(self, str):
		sectorstart = ''

		a = string.split(str, '=')
		if len(a) > 1 and string.strip(a[0]) == 'start':
			sectorstart = a[1]
		else:
			sectorstart = a[0]

		return string.strip(sectorstart)


	def getPartitionSize(self, str):
		partitionsize = ''

		a = string.split(str, '=')
		if len(a) > 1 and string.strip(a[0]) == 'size':
			partitionsize = a[1]
		else:
			partitionsize = a[0]

		return string.strip(partitionsize)


	def getPartId(self, str):
		partid = ''

		a = string.split(str, '=')
		if len(a) > 1 and string.strip(a[0]) == 'Id':
			partid = a[1]
		else:
			partid = a[0]
		
		return string.strip(partid)


	def getFsType(self, mntpoint):
		return self.findFsTypeInFstab(mntpoint)


	def getBootFlags(self, str):
		return string.strip(str)
		

	def getMountPoint(self, devicename):
		mntpoint = self.findMntInFstab('/dev/' + devicename)

		if mntpoint == '':
			#
			# see if the device is part of a raidset
			#
			mntpoint = self.getRaidName(devicename)

		if mntpoint == '':
			cmd = self.e2label + ' /dev/%s ' % (devicename) + \
								'2> /dev/null'
			label = os.popen(cmd).readlines()

			label = string.join(label)
			id = 'LABEL=%s' % (label[:-1])

			mntpoint = self.findMntInFstab(id)

		return mntpoint


	def formatPartedNodePartInfo(self, devname, info):
		#
		# this function parses partition info from 'parted'
		#
		partinfo = []
		isDisk = 0

		for line in info:
			l = string.split(line[:-1])

			if len(l) > 2 and re.match('[0-9]+', l[0]):
				device = devname + l[0]
				isDisk = 1
			else:
				if len(l) > 1 and l[0] == 'Disk':
					isDisk = 1
				continue

			sectorstart = l[1]
			partitionsize = l[2]
			partid = ''

			if len(l) > 3:
				fstype = l[3]
			else:
				fstype = ''
			bootflags = ''

			if fstype == 'linux-swap':
				mntpoint = 'swap'
			else:
				mntpoint = self.getMountPoint(device)


			# print 'formatPartedNodePartInfo:l: ', l

			partinfo.append('%s,%s,%s,%s,%s,%s,%s,%s\n' %
					(device, sectorstart, partitionsize,
						partid, fstype, bootflags, '',
								mntpoint))

			# print 'formatPartedNodePartInfo:partinfo: ', partinfo

		if partinfo == [] and isDisk:
			#
			# this disk has no partitions, create a
			# dummy null entry for it
			#
			partinfo = [ '%s,,,,,,,\n' % (devname) ]

		return partinfo


	def formatNodePartInfo(self, devname, info):
		#
		# this function parses partition info from 'sfdisk'
		#
		partinfo = []
		isDisk = 0

		for line in info:
			l = string.split(line, ',')

			device = ''
			sectorstart = ''
			partitionsize = ''
			partid = ''
			fstype = ''
			bootflags = ''
			mntpoint = ''

			# print 'formatNodePartInfo:l:', l

			if len(l) > 2:
				a = string.split(l[0])
				if len(a) > 2:
					device = self.getDevice(a[0])
					if len(a) == 3:
						sectorstart = \
						self.getSectorStart(a[2])
					elif len(a) == 4:
						sectorstart = \
						self.getSectorStart(a[3])
					mntpoint = self.getMountPoint(device)

				partitionsize = self.getPartitionSize(l[1])
				partid = self.getPartId(l[2])
				fstype = self.getFsType(mntpoint)

			if len(l) > 3:
				bootflags = self.getBootFlags(l[3])

			if partid == '82':
				fstype = 'swap'
				mntpoint = 'swap'

			if device != '':
				partinfo.append('%s,%s,%s,%s,%s,%s,%s,%s\n' %
					(device, sectorstart, partitionsize,
						partid, fstype, bootflags, '',
								mntpoint))

			if len(l) == 1 and l[0] == 'No partitions found\n':
				isDisk = 1
				
		if partinfo == [] and isDisk:
			#
			# this disk has no partitions, create a
			# dummy null entry for it
			#
			partinfo = [ '%s,,,,,,,\n' % (devname) ]

		return partinfo


	def parsePartInfo(self, info):
		n = string.split(info, ',')

		if len(n) != 8:
			return ('', '', '', '', '', '', '', '')

		device = string.strip(n[0])
		sectorstart = string.strip(n[1])
		partitionsize = string.strip(n[2])
		partid = string.strip(n[3])
		fstype = string.strip(n[4])
		bootflags = string.strip(n[5])
		partflags = string.strip(n[6])
		mntpoint = string.strip(n[7])

		return (device, sectorstart, partitionsize, partid, 
			fstype, bootflags, partflags, mntpoint)


	def hasUSBkey(self):
		"""Returns the device name if we have a usb key drive 
		plugged in, 0 otherwise."""

		if self.haveusb is None:
			self.skipdevices = []
			dev=self.findFile('/rocks-usbkey')
			if dev:
				self.haveusb = dev
			else:
				self.haveusb = 0
		return self.haveusb


	def findFile(self, srcfile):
		"""Like saveFile, but does not depend on the existance
		of the targetfile. If srcfile was found on any attached
		disk, returns the device name. If not, returns None."""

		tmpname = tempfile.mktemp()
		rc = self.saveFile(srcfile, tmpname)
		if os.path.exists(tmpname):
			os.unlink(tmpname)
		return rc


	def saveFile(self, srcfile, targetfile):
		"""If srcfile exists on any mountable drive, save it to
		targetfile. If src exists twice, the first found is used.
		If srcfile was found returns the device name it was on, 
		if not or target file exists, returns None."""

		if os.path.exists(targetfile):
			return None

		retval = None
		mountpoint = tempfile.mktemp()
		os.makedirs(mountpoint)

		origfile = mountpoint + srcfile

		directory = os.path.dirname(targetfile)
		if not os.access(directory, os.F_OK):
			os.makedirs(directory)

		for devname in self.getPartitionDevices():
			os.system('mount /dev/%s %s' % (devname, mountpoint) + \
							' > /dev/null 2>&1')

			if os.path.exists(origfile):
				oldfile = open(origfile, 'r')
				newfile = open(targetfile, 'w+')
				newfile.write(oldfile.read())
				newfile.close()
				oldfile.close()
				retval = devname

			os.system('umount %s 2> /dev/null' % (mountpoint))

			if os.path.exists(targetfile):
				break

		try:
			os.removedirs(mountpoint)
		except:
			pass

		return retval


	def gptDrive(self, devname):
		#
		# if this is a drive with a GPT format, then return '1'
		#
		retval = 0

		cmd = '/mnt/runtime/usr/sbin/parted' \
			+ ' /dev/%s' % (devname) \
			+ ' print -s 2> /dev/null'

		label = 'Disk label type:'
		for line in os.popen(cmd).readlines():

			if len(line) > len(label) and \
						line[0:len(label)] == label:

				l = string.split(line)
				if len(l) > 3 and l[3] == 'gpt':
					retval = 1
					break

		return retval


	def getNodePartInfo(self):
		arch = os.uname()[4]

		partinfo = []
		nodedisks = {}

		#
		# Skip USB drives if present
		#
		usbdev = self.hasUSBkey()
		if usbdev:
			#log("ROCKS:found usb drive at %s" % usbdev)
			self.skipDevice(usbdev)

		for devname in self.getDisks():
			log('ROCKS:getNodePartInfo: devname:%s' % (devname))

			use_sfdisk = 1	

			if len(devname) > 2 and devname[0:2] == 'md':
				#
				# fabricate an sfdisk entry for a software
				# raid device
				#
				raidparts = self.getRaidPartitions(devname)
				if raidparts != '':
					str = '/dev/%s : ' % (devname)
					str += 'start=0, size=0, Id=0'
					str += ', %s\n' % (raidparts)
				
					sfdiskinfo = []
					sfdiskinfo.append(str)
			else:
				if self.gptDrive(devname):
					cmd = '/mnt/runtime/usr/sbin/parted' \
						+ ' /dev/%s' % (devname) \
						+ ' print -s 2> /dev/null'
					use_sfdisk = 0
				else: 
					cmd = self.sfdisk + \
						' -d /dev/%s' % (devname) \
							+ ' 2> /dev/null'

				sfdiskinfo = os.popen(cmd).readlines()

				log('ROCKS:getNodePartInfo: sfdiskinfo:%s' % \
					(sfdiskinfo))

			if len(sfdiskinfo) > 0:
				if use_sfdisk:
					i = self.formatNodePartInfo(devname,
						sfdiskinfo)
				else:
					i = self.formatPartedNodePartInfo(
							devname, sfdiskinfo)

				#print 'i:', i
				partinfo += i

		if partinfo != '':
			log('ROCKS:getNodePartInfo: partinfo:%s' % (partinfo))

			for node in partinfo:
				#print 'ROCKS:getNodePartInfo: node:%s' % (node)

				n = self.parsePartInfo(node)

				(nodedevice, nodesectorstart, nodepartitionsize,
					nodepartid, nodefstype, nodebootflags,
					nodepartflags, nodemntpoint) = n

				if (len(nodedevice) > 2) and \
						(nodedevice[0:2] == 'md'):

					nodepartflags = '--level=%d' % \
						self.getRaidLevel(nodedevice)

					n = (nodedevice, nodesectorstart,
						nodepartitionsize,
						nodepartid, nodefstype,
						nodebootflags,
						nodepartflags, nodemntpoint)

				if nodedevice != '':
					key = ''
					for disk in self.getDisks():
						if len(disk) <= len(nodedevice) and disk == nodedevice[0:len(disk)]:
							key = disk
							break

					if key != '':
						if not nodedisks.has_key(key):
							nodedisks[key] = [n]
						else:
							nodedisks[key].append(n)

		log('ROCKS:getNodePartInfo:nodedisks:%s' % (nodedisks))
		return nodedisks


	def compareDiskInfo(self, dbpartinfo, nodepartinfo):
		for db in dbpartinfo:
			if len(db) == 1:
				continue

			(dbdevice, dbsectorstart, dbpartsize, dbpartid, 
				dbfstype, dbbootflags, dbpartflags,
					dbmntpoint) = db

			found = 0
			for node in nodepartinfo:
				if len(node) == 1:
					continue

				(nodedevice, nodesectorstart, nodepartsize,
					nodepartid, nodefstype, nodebootflags,
					 nodepartflags, nodemntpoint) = node

				# print 'compareDiskInfo:node: ', node
				# print 'compareDiskInfo:db: ', db

				if dbsectorstart == nodesectorstart and \
					dbpartsize == nodepartsize and \
					dbpartid == nodepartid and \
					dbfstype == nodefstype and \
					dbbootflags == nodebootflags and \
					dbpartflags == nodepartflags and \
					dbmntpoint == nodemntpoint:

					found = 1
					break

			if not found:
				return 0

		return 1


	def addPartitions(self, id, nodepartinfo, format):
		arch = os.uname()[4]

		#
		# for each partition on a drive, build a partition
		# specification for anaconda
		#
		log('ROCKS:addPartitions:nodepartinfo:%s' % (nodepartinfo))
		for node in nodepartinfo:
			if len(node) == 1:
				continue

			(nodedevice, nodesectorstart, nodepartitionsize,
				nodepartid, nodefstype, nodebootflags,
					nodepartflags, nodemntpoint) = node

			if arch == 'ia64':
				if nodefstype == 'fat32':
					nodefstype = 'vfat'
				elif nodefstype == 'linux-swap':
					nodefstype = 'swap'

			# log('ROCKS:addPartitions:node:%s' % (node))
			# log('ROCKS:addPartitions:format:%s' % (format))

			if nodemntpoint == '':
				continue

			#
			# only add raid partitions if they have a mountpoint
			# defined by their respective 'md' device.
			#
			# anaconda will crash if there is not a valid
			# mountpoint for the md device
			#
			if nodepartid == 'fd':
				if not self.getRaidMountPoint(nodedevice):
					continue

			args = [ nodemntpoint ]

			if len(nodemntpoint) > 3 and \
						nodemntpoint[0:4] == 'raid':
				#
				# never format a software raid partition and
				# always set its size to 1
				# 
				args.append('--noformat')
				args += [ '--size', '1' ]
			elif (nodemntpoint != '/' and nodemntpoint != '/var') \
					and not format:
				args.append('--noformat')
			else:
				if nodefstype == '':
					args += [ '--fstype', self.fstype ]
				else:
					args += [ '--fstype', nodefstype ]

			israid = 0

			if len(nodedevice) > 2 and nodedevice[0:2] == 'md':
				israid = 1

				args += [ "--device=%s" % (nodedevice) ]

				if nodepartflags != '':
					args += [ nodepartflags ]

				args += [ '--useexisting' ]

				for part in string.split(nodebootflags):
					if len(part) > 3 and \
							part[0:4] == 'raid':

						args.append(part) 
			else:
				args += [ "--onpart", nodedevice ]

			if israid:
				log('ROCKS:addPartitions:raidargs:%s ' % (args))

				KickstartBase.defineRaid(
						self.baseinstclass, id, args)
			else:
				log('ROCKS:addPartitions:args:%s' % (args))
				KickstartBase.definePartition(
						self.baseinstclass, id, args)

			self.mountpoints.append(nodemntpoint)

		return


	def isRootDiskConfigured(self):
		retval = 0

		if '/' in self.mountpoints:
			retval = 1

		return retval


	def partitionDriveWithParted(self, drive, partinfo):
		#
		# before we partition, we'll need to remove all partitions
		#
		nodepartinfo = self.getNodePartInfo()
		try:
			for part in nodepartinfo[drive]:
				(device, sectorstart, partitionsize, partid, 
					fstype, bootflags, partflags,
							mntpoint) = part
				a = re.search('[0-9]+$', device)
				if a:
					minor = device[a.start():a.end()]
				else:
					continue
				
				cmd = '/mnt/runtime/usr/sbin/parted' \
						+ ' /dev/%s' % (drive) \
						+ ' rm %s -s' % (minor) 
						# + ' 2> /dev/null'

				#print 'partitionDriveWithParted:cmd: ', cmd
				os.system(cmd)
		except:
			pass

		#
		# now lay down the partitions
		#
		for part in partinfo:
			(device, sectorstart, partitionsize, partid, 
				fstype, bootflags, partflags, mntpoint) = part

			if sectorstart == '0' and partitionsize == '0' \
							and fstype == '':
				#
				# this is an empty partition. do nothing as
				# we removed all partitions above
				#
				continue

			cmd = '/mnt/runtime/usr/sbin/parted' \
				+ ' /dev/%s mkpart primary' % (drive) \
				+ ' %s' % (sectorstart) \
				+ ' %s -s' % (partitionsize)
					# + ' 2> /dev/null'

			# print 'partitionDriveWithParted:cmd: ', cmd
			os.system(cmd)

		return


	def partitionDriveWithSfdisk(self, drive, partinfo):
		#
		# for each partition on a physical drive, convert the
		# partition info into an sfdisk input file
		#
		file = open('/tmp/sfdisk.info', 'w')
		file.write('unit: sectors\n')

		for part in partinfo:
			(device, sectorstart, partitionsize, partid, 
				fstype, bootflags, partflags, mntpoint) = part

			str = '/dev/%s : ' % (device)
			str += 'start=%s, ' % (sectorstart)
			str += 'size=%s, ' % (partitionsize)
			str += 'Id=%s' % (partid)
			if bootflags != '':
				str += ', %s' % (bootflags)
			str += '\n'

			file.write(str)

		file.close()

		#
		# call sfdisk to write the disk partition info
		#
		cmd = '/mnt/runtime/usr/sbin/sfdisk --force ' + \
			'/dev/%s < /tmp/sfdisk.info > /dev/null 2>&1' % (drive)

		os.system(cmd)

		return


	def partitionDrive(self, drive, partinfo):
		#
		# don't try partition software raid devices
		#
		# log('ROCKS:partitionDrive:', drive)

		if drive == 'md':
			return

		if self.gptDrive(drive):
			self.partitionDriveWithParted(drive, partinfo)
		else:
			self.partitionDriveWithSfdisk(drive, partinfo)

		return


	def nukeRaid(self, drive):
		import isys

		for info in self.raidinfo:
			if len(info) > 3:
				(device, partitions, raidlevel,
							num_partitions) = info

			if device == drive:
				log('ROCKS:nukeRaid:device (%s)' % (device))

				#
				# wipe the superblock from each drive in
				# the raid set
				#
				for part in partitions:
					isys.wipeRaidSB('/dev/' + part)	

		#
		# re-read the raidinfo this will update the nuked software
		# raid structure
		#
		self.getRaidInfo()

		return


	def nukePartitions(self, drive, partinfo):
		log('ROCKS:nukePartitions:drive:%s' % (drive))

		if len(drive) > 1 and drive[0:2] == 'md':
			self.nukeRaid(drive)
			return

		nukepartinfo = []

		for part in partinfo: 
			(device, sectorstart, partitionsize, partid,
				fstype, bootflags, partflags, mntpoint) = part

			sectorstart = '0'
			partitionsize = '0'
			partid = '0'
			fstype = ''
			bootflags = ''
			partflags = ''
			mntpoint = ''

			nukepartinfo.append((device, sectorstart,
				partitionsize, partid, fstype,
				bootflags, partflags, mntpoint))

		self.partitionDrive(drive, nukepartinfo)

		return


	def nukeDiskPartitions(self, nukeall=0):
		#
		# if nukeall == 1, then remove all partitions from every
		# drive attached to the system.
		#
		# if nukeall == 0, then only remove all partitions from the
		# first drive.
		#
		log('ROCKS:nukeDiskPartitions:nukeall:%d' % (nukeall))

		nodepartinfo = self.getNodePartInfo()

		for drive in self.getDisks():
			if drive in nodepartinfo.keys():
				self.nukePartitions(drive, nodepartinfo[drive])

				self.addUnknownDisk(drive)

				if nukeall == 0:
					return

		return


	def getFreeGreedyPartition(self):
		basename = '/state/partition'

		i = 1
		while 1:
			nextname = '%s%d' % (basename, i)
			if nextname not in self.mountpoints:
				return nextname

			i = i + 1

		return ''


	def defaultDataDisk(self, disk, id):
		#
		# greedy partitioning
		#
		greedy_partname = self.getFreeGreedyPartition()

		args = [ greedy_partname, "--size", "1",
			"--fstype", self.fstype, 
			"--grow", "--ondisk", disk ]

		KickstartBase.definePartition(self.baseinstclass, id, args)

		self.mountpoints.append(greedy_partname)
		log('ROCKS:defaultDataDisk:args:%s' % (args))

		return

		
	def defaultRootDisk(self, disk, id):
		arch = os.uname()[4]

		if arch == 'ia64':
			args = [ "/boot/efi" , "--size" , "1000",
				"--fstype", "vfat", 
				"--ondisk", disk ]
			KickstartBase.definePartition(self.baseinstclass,
								id, args)
			self.mountpoints.append('/boot/efi')
			log('ROCKS:defaultRootDisk:args:%s' % (args))

		args = [ "/" , "--size" , RocksGetPartsize('root'),
			"--fstype", self.fstype, 
			"--ondisk", disk ]
		KickstartBase.definePartition(self.baseinstclass, id, args)
		self.mountpoints.append('/')
		log('ROCKS:defaultRootDisk:args:%s' % (args))

		args = [ "/var" , "--size" , RocksGetPartsize('var'),
			"--fstype", self.fstype, 
			"--ondisk", disk ]
		KickstartBase.definePartition(self.baseinstclass, id, args)
		self.mountpoints.append('/var')
		log('ROCKS:defaultRootDisk:args:%s' % (args))

		args = [ "swap" , "--size" , RocksGetPartsize('swap'),
			"--ondisk", disk ]
		KickstartBase.definePartition(self.baseinstclass, id, args)
		log('ROCKS:defaultRootDisk:args:%s' % (args))

		#
		# greedy partitioning
		#
		self.defaultDataDisk(disk, id)

		return


	def isRocksDisk(self, partinfo, touchit = 0):
		retval = 0

		mountpoint = tempfile.mktemp()
		os.makedirs(mountpoint)

		for part in partinfo:
			(dev,start,size,id,fstype,bootflags,partflags,mnt) = \
				part

			devname = '/dev/%s' % (dev)
			os.system('mount %s %s' % (devname, mountpoint) + \
							' > /dev/null 2>&1')

			try:
				filename = mountpoint + '/.rocks-release'

				if touchit == 1:
					os.system('touch %s' % filename)

				if os.path.exists(filename):
					retval = 1
			except:
				pass

			os.system('umount %s' % (mountpoint) +
							' > /dev/null 2>&1')

			if retval == 1:
				break

		try:
			os.removedirs(mountpoint)
		except:
			pass

		return retval


	def isLinuxSoftwareRaidPartition(self, partinfo):
		#
		# if one of the partitions has a linux raid autodetect
		# partition, then flag this as a linux software raid disk.
		#
		retval = 0

		for part in partinfo:
			(dev,start,size,id,fstype,bootflags,partflags,mnt) = \
				part

			if id == 'fd' or dev[0:2] == 'md':
				retval = 1

		return retval


	def addUnknownDisk(self, disk):
		if disk not in self.unknown_disks:
			self.unknown_disks.append(disk)
		return


	def getUnknownDisks(self):
		return self.unknown_disks


	def __init__(self, baseinstclass, id, fstype, sfdisk, e2label, fstab):
		#
		# read the current partition info from the physical disks
		# on the installing node
		#
		self.baseinstclass = baseinstclass

		#
		# default file system type for new partitions
		#
		self.fstype = fstype

		#
		# full pathnames to utilities
		#
		self.sfdisk = sfdisk
		self.e2label = e2label

		#
		# full pathnames to files
		#
		self.saved_fstab = fstab

		self.haveusb = None

		return


class RocksDiskSet:

	def __init__(self, diskset, thefsset, baseUrl):
		self.diskset = diskset
		self.baseUrl = baseUrl
		self.thefsset = thefsset
		self.partition = RocksPartition(0, 0, '', 
			'/mnt/runtime/usr/sbin/sfdisk',
			'/mnt/runtime/usr/sbin/e2label', 
			'/tmp/etc/fstab')

		return


	def postPartitionInfo(self, server, req, keyfile, certfile,
								nodepartinfo):
		import httplib

		h = httplib.HTTPSConnection(server, key_file = keyfile,
			cert_file = certfile)
		h.putrequest('GET', req)

		for disk in nodepartinfo.keys():
			for part in nodepartinfo[disk]:
				h.putheader('X-Rocks-PartitionInfo', repr(part))

		try:
			h.endheaders()
			response = h.getresponse()
			status = response.status
		except:
			#
			# assume the error occurred due to an authorization
			# problem
			#
			status = 403
			pass

		h.close()

		return status


	def savePartitions(self):
		import os.path
		import os
		import random
		import time
		import sys

		self.diskset.savePartitions()

		#
		# make sure all the software raid partition configuration info
		# is committed to disk
		#
		for entry in self.thefsset.entries:
			if entry.device.getName() == 'RAIDDevice':
				try:
					entry.device.setupDevice('/tmp')
				except:
					pass

		#
		# tell anaconda to write a temporary /etc/fstab, /etc/raidtab
		# and /etc/mtab'
		#
		try:
			os.makedirs('/tmp/etc')
		except:
			pass
		self.thefsset.write('/tmp')

		#
		# Save certificate keys to connect to parent server.
		#
		self.partition.saveFile('/etc/security/cluster-cert.key',
					'/tmp/security/cluster-cert.key')
		self.partition.saveFile('/etc/security/cluster-cert.crt',
					'/tmp/security/cluster-cert.crt')

		raidstarted = self.partition.isRaidStarted()
		nodepartinfo = self.partition.getNodePartInfo()

		#
		# getNodePartInfo starts all raid devices.
		# 
		# if the raid was not started before we made this call, then
		# make sure we stop it before this routine exits. if we
		# don't, then anaconda can't assign the requested raid
		# partitions
		#
		if not raidstarted:
			self.partition.stopRaid()

		random.seed(int(time.time()))

		#
		# settings when certs exist
		#
		keyfile = '/tmp/security/cluster-cert.key'
		certfile = '/tmp/security/cluster-cert.crt'
		req = '/install/sbin/setDbPartitions.cgi'

		if not os.path.exists(keyfile) or not os.path.exists(certfile):
			#
			# non-cert settings
			#
			keyfile = None
			certfile = None
			req = '/install/sbin/public/setDbPartitions.cgi'

		for i in range(0, 5):
			#
			# try to insert the partition info into the
			# database via https
			#
			try:
				status = self.postPartitionInfo(KickstartHost,
					req, keyfile, certfile, nodepartinfo)
			except:
				status = 403
				pass

			if status == 403 and keyfile != None:
				#
				# on the next retry, do it without certs
				#
				keyfile = None
				certfile = None
				req = '/install/sbin/public/setDbPartitions.cgi'

			if status == 200:
				return

			time.sleep(random.randint(0, 10))
				
		return


	def rocksDiskStamp(self):
		nodepartinfo = self.partition.getNodePartInfo()

		for disk in nodepartinfo.keys():
			self.partition.isRocksDisk(nodepartinfo[disk],
								touchit = 1)

		return


	def __getattr__(self, name):
		return getattr(self.diskset, name)

