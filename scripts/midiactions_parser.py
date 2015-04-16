from optparse import OptionParser
import pandas as pd


def durationparser(inputfile):
    """
    Parse an AnteScofo midiactions score in order to retrieve the
    duration of a MIDI Note event from the time difference between its
    NOTE ON and NOTE OFF. It also adds this relative (to the tempo)
    duration to the midiaction.
    E.g.
    ; delay msgrecvr pitch velocity
    to
    ; delay msgrecvr pitch velocity duration

    """
    # 1. All data in a single dataframe
    inputfile = open(inputfile)
    lines = inputfile.readlines()
    lines = lines[2:-1]  # only lines without headers and final bracket
    parsedlines = []
    for line in lines:
        el = line.strip().split()  # for casting
        el[0] = float(el[0])
        el[2] = int(el[2])
        el[3] = int(el[3])
        parsedlines.append(el)
    df = pd.DataFrame(data=parsedlines, columns=['del', 'mes', 'pit', 'vel'])
    print df
    # 2. For each NOTE ON, search for its NOTE OFF


if __name__ == "__main__":
    """
    """
    usage = "usage: %prog [options] inputfile outputfile"
    opts = OptionParser(usage=usage)
    options, args = opts.parse_args()

    inputfile = args[0]
    outputfile = args[1]

    parsedlines = durationparser(inputfile)

