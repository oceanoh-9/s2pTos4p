import skrf as rf
import numpy as np


def s2pfileTos4pfile(path_21: str, path_31: str, path_32: str, path_41: str, path_42: str, path_43: str, 
                     fileNameToSave: str, unit: str="Hz"):
    """
    This function is used to convert 6 s2p files to a 4-port s4p file
    ----------------
    parameters:
    path_21: str
        path of s2p file which contains S11, S12, S21, S22
    path_31: str
        path of s2p file which contains S11, S13, S31, S33
    path_32: str
        path of s2p file which contains S22, S23, S32, S33
    path_41: str
        path of s2p file which contains S11, S14, S41, S44
    path_42: str
        path of s2p file which contains S22, S24, S42, S44
    path_43: str
        path of s2p file which contains S33, S34, S43, S44
    fileNameToSave: str
        the name of output s4p file
    frequency: str
        the unit of frequency, default is "Hz", can be "GHz", "MHz", "kHz"
    """
    network_Port2ToPort1 = rf.Network(path_21)
    network_Port3ToPort1 = rf.Network(path_31)
    network_Port3ToPort2 = rf.Network(path_32)
    network_Port4ToPort1 = rf.Network(path_41)
    network_Port4ToPort2 = rf.Network(path_42)
    network_Port4ToPort3 = rf.Network(path_43)


    # check if these snp file have same number of frequency
    if (
        len(network_Port2ToPort1.f) != len(network_Port3ToPort1.f)
        or len(network_Port2ToPort1.f) != len(network_Port3ToPort2.f)
        or len(network_Port2ToPort1.f) != len(network_Port4ToPort1.f)
        or len(network_Port2ToPort1.f) != len(network_Port4ToPort2.f)
        or len(network_Port2ToPort1.f) != len(network_Port4ToPort3.f)
    ):
        print("Error: these s2p files have different number of frequency")
        return
    frequency = network_Port2ToPort1.f
    num_frequency = len(network_Port2ToPort1.f)

    # S4P contains all s-parameters of final 4-ports s-parameters
    S4P = np.zeros(shape = [num_frequency, 4, 4], dtype = complex)

    S_Port2ToPort1 = network_Port2ToPort1.s
    S4P[:, 0, 0] = S_Port2ToPort1[:, 0, 0]  # S11
    S4P[:, 0, 1] = S_Port2ToPort1[:, 0, 1]  # S12
    S4P[:, 1, 0] = S_Port2ToPort1[:, 1, 0]  # S21
    S4P[:, 1, 1] = S_Port2ToPort1[:, 1, 1]  # S22
    print("import S11, S12, S21, S22 from " + path_21 + " to S4P")
    """
    S_Port2ToPort1  contains :
    *S11 *S12 S13 S14 
    *S21 *S22 S23 S24
     S31  S32 S33 S34
     S41  S42 S43 S44
    """

    S_Port3ToPort1 = network_Port3ToPort1.s
    """
    S_Port3ToPort1  contains :
    *S11 S12 *S13 S14 
     S21 S22  S23 S24
    *S31 S32 *S33 S34
     S41 S42  S43 S44
    """
    S4P[:, 0, 2] = S_Port3ToPort1[:, 0, 1]  # S13
    S4P[:, 2, 2] = S_Port3ToPort1[:, 0, 0]  # S33
    S4P[:, 2, 0] = S_Port3ToPort1[:, 1, 1]  # S31
    print("import S13, S33, S31 from " + path_31 + " to S4P")

    S_Port3ToPort2 = network_Port3ToPort2.s
    """
    S_Port3ToPort2  contains :
    S11  S12  S13 S14 
    S21 *S22 *S23 S24
    S31 *S32 *S33 S34
    S41  S42  S43 S44
    """
    S4P[:, 1, 2] = S_Port3ToPort2[:, 0, 1]  # S23
    S4P[:, 2, 1] = S_Port3ToPort2[:, 1, 0]  # S32
    print("import S23, S32 from " + path_32 + " to S4P")

    S_Port4ToPort1 = network_Port4ToPort1.s
    """
    S_Port4ToPort1  contains :
    *S11 S12 S13 *S14 
     S21 S22 S23  S24
     S31 S32 S33  S34
    *S41 S42 S43 *S44
    """
    S4P[:, 0, 3] = S_Port4ToPort1[:, 0, 1]  # S14
    S4P[:, 3, 3] = S_Port4ToPort1[:, 0, 0]  # S44
    S4P[:, 3, 0] = S_Port4ToPort1[:, 1, 1]  # S41
    print("import S14, S44, S41 from " + path_41 + " to S4P")

    S_Port4ToPort2 = network_Port4ToPort2.s
    """
    S_Port4ToPort2  contains :
    S11  S12 S13  S14 
    S21 *S22 S23 *S24
    S31  S32 S33  S34
    S41 *S42 S43 *S44
    """
    S4P[:, 1, 3] = S_Port4ToPort2[:, 0, 1]  # S24
    S4P[:, 3, 1] = S_Port4ToPort2[:, 1, 0]  # S42
    print("import S24, S42 from " + path_42 + " to S4P")

    S_Port4ToPort3 = network_Port4ToPort3.s
    """
    S_Port4ToPort3  contains :
    S11 S12  S13  S14 
    S21 S22  S23  S24
    S31 S32 *S33 *S34
    S41 S42 *S43 *S44
    """
    S4P[:, 2, 3] = S_Port4ToPort3[:, 0, 1]  # S34
    S4P[:, 3, 2] = S_Port4ToPort3[:, 1, 0]  # S43
    print("import S34, S43 from " + path_43 + " to S4P")

    # create a 4-port Network object by input S4P and frequency
    network_4port = rf.Network(s=S4P, f=frequency, z0=50)
    network_4port.frequency.unit = unit
    network_4port.write_touchstone(fileNameToSave, form = 'ma')
    print("write S4P to " + fileNameToSave + ".s4p successfully")
    return


if __name__ == "__main__":
    """
    please input 6 s2p files' path
    path_Port2ToPort1 is the path of s2p file which contains S11, S12, S21, S22
    path_Port3ToPort1 is the path of s2p file which contains S11, S13, S31, S33
    path_Port3ToPort2 is the path of s2p file which contains S22, S23, S32, S33
    path_Port4ToPort1 is the path of s2p file which contains S11, S14, S41, S44
    path_Port4ToPort2 is the path of s2p file which contains S22, S24, S42, S44
    path_Port4ToPort3 is the path of s2p file which contains S33, S34, S43, S44
    """
    path_Port2ToPort1 = "./data/21.s2p"
    path_Port3ToPort1 = "./data/31.s2p"
    path_Port3ToPort2 = "./data/32.s2p"
    path_Port4ToPort1 = "./data/41.s2p"
    path_Port4ToPort2 = "./data/42.s2p"
    path_Port4ToPort3 = "./data/43.s2p"

    filename = "4port"
    s2pfileTos4pfile(
        path_Port2ToPort1,
        path_Port3ToPort1,
        path_Port3ToPort2,
        path_Port4ToPort1,
        path_Port4ToPort2,
        path_Port4ToPort3,
        filename,
        unit="kHz"

    )
