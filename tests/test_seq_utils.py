from unittest import TestCase

from Bio import AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from tests.from_msa import make_alignment
from make_prg.seq_utils import get_interval_seqs, has_empty_sequence


class TestGetIntervals(TestCase):
    def test_ambiguous_bases_one_seq(self):
        alignment = AlignIO.MultipleSeqAlignment([SeqRecord(Seq("RWAAT"))])
        result = get_interval_seqs(alignment)
        expected = {"GAAAT", "AAAAT", "GTAAT", "ATAAT"}
        self.assertEqual(set(result), expected)

    def test_ambiguous_bases_one_seq_with_repeated_base(self):
        alignment = AlignIO.MultipleSeqAlignment([SeqRecord(Seq("RRAAT"))])
        result = get_interval_seqs(alignment)
        expected = {"GAAAT", "AAAAT", "GGAAT", "AGAAT"}
        self.assertEqual(set(result), expected)

    def test_first_sequence_in_is_first_sequence_out(self):
        alignment = AlignIO.MultipleSeqAlignment(
            [SeqRecord(Seq("TTTT")), SeqRecord(Seq("AAAA")), SeqRecord(Seq("CC-C")),]
        )
        result = get_interval_seqs(alignment)
        expected = ["TTTT", "AAAA", "CCC"]
        self.assertEqual(expected, result)


class TestEmptySeq(TestCase):
    def test_sub_alignment_with_empty_sequence(self):
        msa = make_alignment(["TTAGGTTT", "TTA--TTT", "GGA-TTTT"])
        self.assertTrue(has_empty_sequence(msa, [3, 4]))
