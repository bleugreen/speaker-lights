class SmoothList:
    def __init__(self, length=1, ceilDecay=0.99999, meanFrames=2):
        self.data = []
        self.max = []
        self.ceilDecay = ceilDecay
        self.meanFrames = meanFrames
        self.maxIdx = 0
        for i in range(length):
            self.data.append(0)
            self.max.append(0)

    def update(self, rawData):
        i=0
        max = 0
        self.maxIdx = 0
        for val in rawData:
            if(val > max):
                max = val
                self.maxIdx = i
            if(val > self.max[i]):
                self.max[i] = val
            else:
                self.max[i] *= self.ceilDecay
            nVal = val / self.max[i]
            self.data[i] = ((self.meanFrames*self.data[i])+nVal)/(self.meanFrames+1)
            i += 1

    def get(self, idx):
        if idx < len(self.data):
            return self.data[idx]

    def len(self):
        return len(self.data)