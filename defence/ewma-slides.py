@extends("ewma.sme")
class EWMA(Network):
    def wire(self, indata, outdata, *args, **kwargs):
        count = len(indata)
        alpha = 0.1

        stream = ExternalBus("stream")
        output = ExternalBus("output")

        logger = Logger("Logger", [output],
                        [], count, outdata)
        self.tell(logger)
        source = Source("Source", [], [stream],
                        indata, count)
        self.tell(source)

class Source(External):
    def setup(self, ins, outs, data, count):
        self.map_outs(outs, "out")
        self.data = data
        self.count = count
        self.gen = self._datagen()

    def _datagen(self):
        for e in self.data:
            yield e

    def run(self):
        self.out["val"] = next(self.gen)
        self.out["valid"] = 1


class Logger(External):
    def setup(self, ins, outs, count, results):
        self.map_ins(ins, "data")
        self.results = results
        self.curpos = 0

    # Save data to array

def main():
    sme = SME()
    with open(data_file, 'rb') as f:
        indata = np.load(f)
    outdata = np.zeros(indata.shape)
    sme.network = EWMA("EWMA", indata, outdata)
    sme.network.clock(255)
    x = np.linspace(0, 0.5, len(indata))
    p = plt.plot(x, indata, x, outdata)
    pylab.show()

if __name__ == "__main__":
    main()
