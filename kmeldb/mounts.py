import os
try:
    import psutil
except ImportError:
    print('Falling back to parsing mounts output')
    HAVE_PSUTIL = False
else:
    print('Using psutil')
    HAVE_PSUTIL = True


def get_fat_mounts():
    # global HAVE_PSUTIL
    # HAVE_PSUTIL = False

    fat_mounts = []

    if HAVE_PSUTIL:
        partitions = psutil.disk_partitions()
        for part in partitions:
            if 'fat' in part.fstype:
                fat_mounts.append((part.mountpoint, part.fstype, part.device))
    else:
        mounts = os.popen('mount')
        for line in mounts.readlines():
            device, ign1, mount_point, ign2, filesystem, options = line.split()
            if 'fat' in filesystem:
                fat_mounts.append((mount_point, filesystem, device))
    return fat_mounts


def main():
    mounts = get_fat_mounts()
    for mount in mounts:
        print(mount)


if __name__ == '__main__':
    main()
