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
    inputfile = open(inputfile)
    lines = inputfile.readlines()
    inputfile.close()
    lines = lines[2:-1]  # only lines without headers and final bracket
    parsedlines = []
    for line in lines:
        el = line.strip().split()  # casting
        el[0] = float(el[0])
        el[2] = int(el[2])
        el[3] = int(el[3])
        parsedlines.append(el)
    df = pd.DataFrame(data=parsedlines, columns=['del', 'mes', 'pit', 'vel'])
    # 1 Final dataset copy of NoteONs
    note_on_df = df[df['vel'] > 0]
    out_df = pd.DataFrame(data=note_on_df, columns=['del', 'mes', 'pit', 'vel', 'dur'])
    final_df = pd.DataFrame(columns=['del', 'mes', 'pit', 'vel', 'dur'])
    ddl = 0
    for i in xrange(len(out_df)):
        # Finding the indexes of NOTEON and NOTEOFF
        non = out_df.irow(i)
        non_pit = non.pit
        non_idx = non.name

        nof = df.loc[non_idx:][(df.loc[non_idx:]['vel'] == 0) & (df.loc[non_idx:]['pit'] == non_pit)].irow(0)
        nof_idx = nof.name
        # duration of note is the sum of all delays between ]NOTEON, NOTEFF]
        dur = sum(df[non_idx + 1:nof_idx + 1]['del'])
        # new delay time depends if its a note or a chord
        if df.loc[non_idx, 'del'] == 0:
            # if it's a chord, ddl = 0
            ddl = 0
        else:
            # if it's a note, ddl = current ddl + previous ddl>0
            for j in xrange(non_idx, 0, -1):
                if df.loc[j - 1, 'del'] != 0:
                    prev_ddl = df.loc[j - 1, 'del']
                    ddl = df.loc[non_idx, 'del'] + prev_ddl
                    break
        final_df.loc[i] = ddl, 'mnote', non_pit, 80, dur
        # print("ddl: {4}, dur: {2}, non_idx: {0}, nof_idx: {1}, pit: {3}").format(non_idx, nof_idx, dur, non_pit, ddl)

    final_df.loc[0, 'del'] = note_on_df.loc[0, 'del']
    return final_df


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
