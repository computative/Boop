import numpy as np

class Identifier:
    # the metric must be symmetric and zero on equal items
    def __init__(self, sequences, metric):
        self.metric = metric
        self._sequences = {}
        for seq in sequences:
            if seq not in self:
                self._sequences[len(self._sequences)] = seq

    def __contains__(self, seq):
        for _seq in self._sequences.values():
            if len(_seq) == len(seq):
                if not any([self.metric(item, _item) for item, _item in zip(seq, _seq) ]):
                    return True
        return False

    def seq(key):
        if key in self._sequences:
            return self._sequences[key]
        return None
    
    def key(self, seq):
        for _key, _seq in self._sequences.items():
            if len(seq) == len(_seq):
                if not any(map(self.metric, seq, _seq)):
                    return _key
        return None

    def outward(self, seq):
        maps = np.zeros( (len(self._sequences), len(seq)) , dtype=int)
        for _key, _seq in self._sequences.items():
            for i, item in enumerate(seq):
                p = np.infty
                for j, _item in enumerate(_seq):
                    proposal = self.metric(item, _item)
                    if proposal < p:
                        p = proposal
                        maps[_key, i] = j
        #cols correspond to identifications across _sequences with elements of seq
        return maps 

    def inward(self, seq):
        maps = []
        for _key, _seq in self._sequences.items():
            row = np.zeros(len(_seq)).tolist()
            for j, _item in enumerate(_seq):
                p = np.infty
                for i, item in enumerate(seq):
                    proposal = self.metric(item, _item)
                    if proposal < p:
                        p = proposal
                        row[j] = i
            maps.append(row)
        return maps
    
if __name__ == "__main__":

    from difflib import SequenceMatcher
    metric = lambda x, y: 1.0 - SequenceMatcher(None, x.lower(), y.lower()).ratio()
    sequences = [["Europe", "North America", "Africa", "Latin America"],
                ["Europa", "Afrika", "Amerika", "Oceania"]]
    idr = Identifier(sequences, metric)
    outmaps = idr.outward(sequences[0])
    inmaps = idr.inward(sequences[1])
    print(outmaps.tolist())
    print(inmaps)
