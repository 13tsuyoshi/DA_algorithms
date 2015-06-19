"""
Tests for matching algorithms.
"""
from numpy.testing import assert_array_equal

from da_algorithms import gale_shapley


class TestDeferredAcceptance:

    def setUp(self):
        '''Setup preference order lists'''
        # Males' preference orders over females [0, 1, 2] and unmatched
        m_unmatched = 3
        self.m_prefs = [[0, 1, 2, m_unmatched],
                        [2, 0, 1, m_unmatched],
                        [1, 2, 0, m_unmatched],
                        [2, 0, 1, m_unmatched]]
        # Females' preference orders over males [0, 1, 2, 3] and unmatched
        f_unmatched = 4
        self.f_prefs = [[2, 0, 1, 3, f_unmatched],
                        [0, 1, 2, 3, f_unmatched],
                        [2, f_unmatched, 1, 0, 3]]

        # Unique stable matching
        self.m_matched = [0, 1, 2, m_unmatched]
        self.f_matched = [0, 1, 2]

    def test_male_proposal(self):
        m_matched_computed, f_matched_computed = \
            gale_shapley(self.m_prefs, self.f_prefs)
        assert_array_equal(m_matched_computed, self.m_matched)
        assert_array_equal(f_matched_computed, self.f_matched)

    def test_female_proposal(self):
        f_matched_computed, m_matched_computed = \
            gale_shapley(self.f_prefs, self.m_prefs)
        assert_array_equal(m_matched_computed, self.m_matched)
        assert_array_equal(f_matched_computed, self.f_matched)


if __name__ == '__main__':
    import sys
    import nose

    argv = sys.argv[:]
    argv.append('--verbose')
    argv.append('--nocapture')
    nose.main(argv=argv, defaultTest=__file__)
