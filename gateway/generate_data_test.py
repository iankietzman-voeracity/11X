from generate_data import generateRandomSequence, generateQualityValues, mutateSequence, randomizedLane

def func(x):
    return x + 1

class TestGenerateRandomSequence:
    def test_length_100(self):
        sequence = generateRandomSequence(100)
        assert len(sequence) == 100
    def test_returns_string(self):
        sequence = generateRandomSequence(0)
        assert isinstance(sequence, str)
    def test_nucleotides(self):
        sequence = generateRandomSequence(100)
        assert sequence.count('A') + sequence.count('T') + sequence.count('C') + sequence.count('G')== 100

class TestGenerateQualityValues:
    def test_length_100(self):
        q_values = generateQualityValues(100)
        assert len(q_values) == 100
    def test_returns_string(self):
        sequence = generateQualityValues(0)
        assert isinstance(sequence, str)
    def test_quality_scores(self):
        q_values = generateQualityValues(100)
        assert q_values.count('F') == 100

class TestRandomizedLane:
    def test_returns_string(self):
        lane = randomizedLane(1)
        assert isinstance(lane, str)
    def test_randomized_lane(self):
        lane = randomizedLane(10)
        assert int(lane) >= 1
        assert int(lane) < 10

class TestMutateSequence:
    def test_length(self):
        sequence = generateRandomSequence(100)
        assert len(mutateSequence(sequence, 0.5)) == 100
    def test_no_mutations(self):
        sequence = generateRandomSequence(100)
        assert mutateSequence(sequence, 0) == sequence
    def test_mutation_nucleotide_randomization_smokescreen(self):
        sequence = mutateSequence(generateRandomSequence(1000), 0.5)
        assert sequence.count('A') + sequence.count('T') + sequence.count('C') + sequence.count('G')== 1000
    def test_mutation_individual_nt_randomization_smokescreen(self):
        """
        Note it is possible for this test to fail and not indicate an underlying issue, but the changes are so EXTREMELY low as to be discounted
        """
        sequence = mutateSequence(generateRandomSequence(1000), 0.5)
        assert sequence.count('A') > 200
        assert sequence.count('A') < 300
        assert sequence.count('T') > 200
        assert sequence.count('T') < 300
        assert sequence.count('C') > 200
        assert sequence.count('C') < 300
        assert sequence.count('G') > 200
        assert sequence.count('G') < 300