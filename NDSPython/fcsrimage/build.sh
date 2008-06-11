#!/bin/sh
# build.sh output.img sourcedatadir
# 
# Builds a FAT disk image from a given directory.
# 
#

# calculate size of image needed
SIZE=`du "$2"|cut -f1|tail -n1`

# add 64KB for an overlay
SIZE=`expr $SIZE + 64`

# create empty file
echo Creating image
./zero "$1" $SIZE

# format FAT fs
echo Formatting as FAT12
mkfs.vfat -F 12 "$1"

# make a temp dir for mounting
sudo rm -rf _disktmp
mkdir _disktmp

# mount the image
echo Mounting Image
sudo mount -o loop "$1" _disktmp

# copy data into image
echo Copying Data
sudo cp -r "$2"/* _disktmp

# unmount image
echo Unmounting
sudo umount _disktmp

# remove mount point
rmdir _disktmp

# 'bless' the image so it is recognized by FCSR driver, and sets up SRAM overlay
echo Blessing image
./bless "$1"

echo "$SIZE KB FAT image built as $1 from $2\n"
file "$1"
