all: generate_ioctl vfat_ioctl.py

generate_ioctl: generate_ioctl.c

vfat_ioctl.py: generate_ioctl
	./generate_ioctl > vfat_ioctl.py
