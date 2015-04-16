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
        el = line.strip().split()  # casting
        el[0] = float(el[0])
        el[2] = int(el[2])
        el[3] = int(el[3])
        parsedlines.append(el)
    df = pd.DataFrame(data=parsedlines, columns=['del', 'mes', 'pit', 'vel'])
    dfd = pd.DataFrame(columns=['del', 'mes', 'pit', 'vel', 'dur'])  # new dataframe with duration
    note_on_df = df[df['vel'] > 0]   # dataframe of NOTEONs only
    for i in xrange(len(note_on_df)):
        non = note_on_df.irow(i)
        non_idx = non.name  # index of this NOTE ON in the dataframe
        pit = non.pit  # note pitch value
        # and search for the next index with pitch value 0 in the original df
        aln_df = df.loc[non_idx:]  # all notes dataframe staring at the index of the NOTE ON
        # search for the next NOTE index with [pitch == pit, vel = 00]
        nof = aln_df.loc[non_idx:][(aln_df.loc[non_idx:]['vel'] == 0) & (aln_df.loc[non_idx:]['pit'] == pit)].irow(0)
        nof_idx = nof.name
        #  the final duration for a NOTE ON is given by adding all delays between ]NOTEON idx, NOTEOFF idx]
        dur = sum(df[non_idx + 1:nof_idx + 1]['del'])
        dfd.loc[i] = note_on_df.irow(i)  #  store the NOTEON and duration in a new dataframe
        dfd.loc[i, 'dur'] = dur
    return dfd

if __name__ == "__main__":
    """
    """
    usage = "usage: %prog [options] inputfile outputfile"
    opts = OptionParser(usage=usage)
    options, args = opts.parse_args()

    inputfile = args[0]
    outputfile = args[1]

    parsedlines = durationparser(inputfile)
    parsedlines.to_csv(outputfile, header=False, index=False)
