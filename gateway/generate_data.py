import json
import random

REFERENCE_GENOME = []
with open("./reference_genome.json", "r") as f:
    REFERENCE_GENOME = json.load(f)
    
FILENAME_PREFIX = './data/tinygex_S1_L00'
FILENAME_INFIX = '_R'
FILENAME_SUFFIX = '_001.fastq'
LANES = 2

SEQUENCE_IDENTIFIER_PREFIX = '@A00228:279:HFWFVDMXX:'
R1_SEQUENCE_IDENTIFIER_SUFFIX = ':TILE_NUMBER:X:Y 1:N:0:0'
R2_SEQUENCE_IDENTIFIER_SUFFIX = ':TILE_NUMBER:X:Y 3:N:0:0'

GENES = ('FIG1','MGFA','PET')
VARIANTS = ((random.randint(0,1),random.randint(0,1)),(random.randint(0,1),random.randint(0,1)),(random.randint(0,1),random.randint(0,1)))
CELL_EXPRESSION_LEVELS = ((100,10,50),(50,100,10),(10,50,100))
CELLS_PER_CELLTYPE = 3
SKIP_RATE = 0.05
DUPLICATION_RATE = 0.05
NT_READ_ERROR_RATE = 0.02

writeData = {}

class ExceptionHandler(Exception):
    pass

def generateRandomSequence(length: int) -> str:
    """Returns a string of randomized nucleotides of the provided length.

    generateRandomSequence(0) --> ''
    generateRandomSequence(1) --> 'C'
    generateRandomSequence(10) --> 'CATGCTAGTC'
    
    """
    nucleotides = ('A','T','C','G')
    sequence = ''
    for i in range(length):
        sequence += nucleotides[random.randint(0,3)]
    return sequence

def mutateSequence(sequence: str, mutationRate: float) -> str:
    """Returns a provided nucleotide sequence with random mutations.

    Mutation rate is provided as a float argument as exactness is not necessary. Mutation may return original nucleotide, as again exactness is not necessary.

    mutateSequence('G', 1) --> 'G'
    mutateSequence('G', 1) --> 'C'
    mutateSequence('CATGCTAGTC', 0.5) --> 'TACCATAGAC'
    mutateSequence('CATGCTAGTC', 0.) --> 'CATGCTAGTC'

    """
    if mutationRate == 0:
        return sequence
    sequence = list(sequence)
    for index, char in enumerate(sequence):
        mutate = random.randint(1, 1 / mutationRate)
        if mutate == 1:
            sequence[index] = generateRandomSequence(1)
    return "".join(sequence)

def generateQualityValues(length: int) -> str:
    """Returns a string of nucleotide read quality scores

    generateQualityValues(0) --> ''
    generateQualityValues(2) --> 'FF'
    generateQualityValues(10) --> 'FFFFFFFFFF'
    
    """
    if length == 0:
        return ''
    return 'F' * length

def randomizedLane(lanes) -> str:
    """Returns a random lane number from the provided number of lanes

    randomizedLane(1) --> 1
    randomizedLane(5) --> 3
    
    """
    if lanes == 0:
        raise ExceptionHandler('No lanes found') 
    return str(random.randint(1, lanes))

def main():
    for cellTypeIndex, cellType in enumerate(CELL_EXPRESSION_LEVELS):
        for i in range(CELLS_PER_CELLTYPE):
            barcode = generateRandomSequence(18)
            for index, gene in enumerate(GENES):
                for transcript in range(CELL_EXPRESSION_LEVELS[cellTypeIndex][index]):
                    skip = random.randint(1, 1 / SKIP_RATE)

                    if skip == 1:
                        continue

                    duplicate = random.randint(1, 1 / DUPLICATION_RATE)
                    umi = generateRandomSequence(10)
                    referenceSequence = REFERENCE_GENOME[index]['data']['variants'][VARIANTS[index][random.randint(0,1)]]['sequence']
                    readStart = random.randint(0,len(referenceSequence) - 91)
                    readSequence = referenceSequence[readStart:readStart + 91]
                    readSequence = mutateSequence(readSequence, NT_READ_ERROR_RATE)
                    lane = randomizedLane(LANES)

                    r1SequenceData = (
                        f'{SEQUENCE_IDENTIFIER_PREFIX + lane + R1_SEQUENCE_IDENTIFIER_SUFFIX}\n'
                        f'{barcode + umi}\n'
                        '+\n'
                        f'{generateQualityValues(len(barcode + umi))}\n'
                    )

                    r2SequenceData = (
                        f'{SEQUENCE_IDENTIFIER_PREFIX + lane + R2_SEQUENCE_IDENTIFIER_SUFFIX}\n'
                        f'{readSequence}\n'
                        '+\n'
                        f'{generateQualityValues(len(readSequence))}\n'
                    )

                    if  FILENAME_PREFIX + lane + FILENAME_INFIX + '1' + FILENAME_SUFFIX in writeData.keys():
                        writeData[FILENAME_PREFIX + lane + FILENAME_INFIX + '1' + FILENAME_SUFFIX] = writeData[FILENAME_PREFIX + lane + FILENAME_INFIX + '1' + FILENAME_SUFFIX] + r1SequenceData
                    else: 
                        writeData[FILENAME_PREFIX + lane + FILENAME_INFIX + '1' + FILENAME_SUFFIX] = r1SequenceData

                    if  FILENAME_PREFIX + lane + FILENAME_INFIX + '2' + FILENAME_SUFFIX in writeData.keys():
                        writeData[FILENAME_PREFIX + lane + FILENAME_INFIX + '2' + FILENAME_SUFFIX] = writeData[FILENAME_PREFIX + lane + FILENAME_INFIX + '2' + FILENAME_SUFFIX] + r2SequenceData
                    else: 
                        writeData[FILENAME_PREFIX + lane + FILENAME_INFIX + '2' + FILENAME_SUFFIX] = r2SequenceData

                    if duplicate == 1:
                        readSequence = mutateSequence(readSequence, NT_READ_ERROR_RATE)
                        lane = randomizedLane(LANES)

                        r2SequenceData = (
                            f'{SEQUENCE_IDENTIFIER_PREFIX + lane + R2_SEQUENCE_IDENTIFIER_SUFFIX}\n'
                            f'{readSequence}\n'
                            '+\n'
                            f'{generateQualityValues(len(readSequence))}\n'
                        )

                        writeData[FILENAME_PREFIX + lane + FILENAME_INFIX + '1' + FILENAME_SUFFIX] = writeData[FILENAME_PREFIX + lane + FILENAME_INFIX + '1' + FILENAME_SUFFIX] + r1SequenceData

                        writeData[FILENAME_PREFIX + lane + FILENAME_INFIX + '2' + FILENAME_SUFFIX] = writeData[FILENAME_PREFIX + lane + FILENAME_INFIX + '2' + FILENAME_SUFFIX] + r2SequenceData

    for key in writeData.keys():
        with open(key, 'w') as file:
            file.write(writeData[key])

if __name__ == "__main__":
   main()