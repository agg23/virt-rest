import libvirt

def getConnection():
    conn = libvirt.openReadOnly(None)
    if conn is None:
        print('Failed to open connection to the hypervisor')

    return conn