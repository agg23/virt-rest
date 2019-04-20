import libvirt

def getConnection():
    conn = libvirt.open(None)
    if conn is None:
        print('Failed to open connection to the hypervisor')

    return conn