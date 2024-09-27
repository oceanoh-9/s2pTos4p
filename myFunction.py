import numpy as np

class mixSpar():
    def __init__(self,
    S11: np.ndarray,
    S12: np.ndarray,
    S13: np.ndarray,
    S14: np.ndarray,
    S21: np.ndarray,
    S22: np.ndarray,
    S23: np.ndarray,
    S24: np.ndarray,
    S31: np.ndarray,
    S32: np.ndarray,
    S33: np.ndarray,
    S34: np.ndarray,
    S41: np.ndarray,
    S42: np.ndarray,
    S43: np.ndarray,
    S44: np.ndarray,
    order: str = "seq",):
        """
        after initialization, this class will generate mixed-mode S-parameters as object attributes
        input 4x4 S-parameters of a 4-port network
        order: default is "seq" for sequential, "even" for even-odd
        """
        self.S11 = S11
        self.S12 = S12
        self.S13 = S13
        self.S14 = S14
        self.S21 = S21
        self.S22 = S22
        self.S23 = S23
        self.S24 = S24
        self.S31 = S31
        self.S32 = S32
        self.S33 = S33
        self.S34 = S34
        self.S41 = S41
        self.S42 = S42
        self.S43 = S43
        self.S44 = S44
        self.order = order
        self.genMixdSpar()
        return

    def genMixdSpar(self):
        HALF: float = 0.5
        if self.order == "seq":
            S11 = self.S11
            S12 = self.S12
            S13 = self.S13
            S14 = self.S14
            S21 = self.S21
            S22 = self.S22
            S23 = self.S23
            S24 = self.S24
            S31 = self.S31
            S32 = self.S32
            S33 = self.S33
            S34 = self.S34
            S41 = self.S41
            S42 = self.S42
            S43 = self.S43
            S44 = self.S44
        elif self.order == "even":
            S11 = self.S11
            S12 = self.S13
            S13 = self.S12
            S14 = self.S14
            S21 = self.S31
            S22 = self.S33
            S23 = self.S32
            S24 = self.S34
            S31 = self.S21
            S32 = self.S23
            S33 = self.S22
            S34 = self.S24
            S41 = self.S41
            S42 = self.S43
            S43 = self.S42
            S44 = self.S44
        else:
            raise ValueError("order must be 'seq' or 'even'")
        self.SDD11: np.ndarray = np.multiply(HALF, (S11-S13-S31+S33))
        self.SDD12: np.ndarray = np.multiply(HALF, (S12-S14-S32+S34))
        self.SDD21: np.ndarray = np.multiply(HALF, (S21-S23-S41+S43))
        self.SDD22: np.ndarray = np.multiply(HALF, (S22-S24-S42+S44))

        self.SDC11: np.ndarray = np.multiply(HALF, (S11+S13-S31-S33))
        self.SDC12: np.ndarray = np.multiply(HALF, (S12+S14-S32-S34))
        self.SDC21: np.ndarray = np.multiply(HALF, (S21+S23-S41-S43))
        self.SDC22: np.ndarray = np.multiply(HALF, (S22+S24-S42-S44))

        self.SCD11: np.ndarray = np.multiply(HALF, (S11-S13+S31-S33))
        self.SCD12: np.ndarray = np.multiply(HALF, (S12-S14+S32-S34))
        self.SCD21: np.ndarray = np.multiply(HALF, (S21-S23+S41-S43))
        self.SCD22: np.ndarray = np.multiply(HALF, (S22-S24+S42-S44))

        self.SCC11: np.ndarray = np.multiply(HALF, (S11+S13+S31+S33))
        self.SCC12: np.ndarray = np.multiply(HALF, (S12+S14+S32+S34))
        self.SCC21: np.ndarray = np.multiply(HALF, (S21+S23+S41+S43))
        self.SCC22: np.ndarray = np.multiply(HALF, (S22+S24+S42+S44))
        return
