import os


def get_fat_mounts():
    fat_mounts = []
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
