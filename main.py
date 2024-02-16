import sys
import collections
import tiktoken
import functools


def convertINT16To2Chr(input): #could be replaced with bit shifting.  probably faster w/ bit shifts?
    output = ""
    buffer1 = int(input / 256)
    buffer2 = input - (buffer1 * 256)
    output = [chr(buffer1), chr(buffer2)]
    return(output)



def main(inputFile): #trying out elimination of redundant output gathering phase.  maybe not so redundant.  i think this is too hard to read...
    output = {}    
    output['tokenizer used'] = tiktoken.get_encoding('gpt2')
    output['original text'] = inputFile.read()

    buffer = output['original text'].split(" ")
    splits = list(map(lambda x: ' '.join(buffer[x:x+100]), range(0, len(buffer), 100)))
    tokenSets = list(map(lambda x: output['tokenizer used'].encode(x), splits))
    output['monolithic token stream'] = list(functools.reduce(lambda x, y: x + y, tokenSets, []))    
    tokenConversionBuffer = list(map(lambda x: convertINT16To2Chr(x), output['monolithic token stream']))
    output['compress ready data'] = ''.join(tokenConversionBuffer)    
    groups = list(map(lambda x: output['monolithic token stream'][x:x+100], range(0, len(output['monolithic token stream']), 100)))            
    output['decoded data'] = functools.reduce(lambda x, y: x + output['tokenizer used'].decode(y), groups, "")        
    return(output)



def basicStatistics(inputData):
    output = {}
    inputFileSize = len(inputData['original text'])
    tokenCount = len(inputData['monolithic token stream'])
    dataVolume = tokenCount * 2
    estimatedMinFileSize = tokenCount * (inputData['tokenizer used'].n_vocab / (2**16)) * 2
    frequencies = dict(collections.Counter(inputData['monolithic token stream']))
    distinctTokenCount = len(frequencies)
    commonElements = dict(filter(lambda x: x[1] > 32, frequencies.items()))
    uncommonElements = dict(filter(lambda x: x[1] < 32, frequencies.items()))
    topElementsSum = functools.reduce(lambda x, y: x + y[1], commonElements.items(), 0)
    bottomElementsSum = functools.reduce(lambda x, y: x + y[1], uncommonElements.items(), 0)
    topElementsCount = len(commonElements)
    bottomElementsCount = len(uncommonElements)
    topElementsSumProp = topElementsSum / tokenCount
    bottomElementsSumProp = bottomElementsSum / tokenCount
    topElementsCountProp = topElementsCount / distinctTokenCount
    bottomElementsCountProp = bottomElementsCount / distinctTokenCount
    
    output['input file size'] = str(inputFileSize) + "B"
    output['token count'] = tokenCount,
    output['tokenized data volume'] = str(dataVolume) + "B",
    output['estimated minimum file size'] = str(estimatedMinFileSize) + "B",
    output['distinct token count'] = distinctTokenCount,
    output['top elements total / proportion of tokens'] = (topElementsSum, topElementsSumProp),
    output['bottom elements total  / proportion of tokens'] = (bottomElementsSum, bottomElementsSumProp),
    output['top elements distinct count / proportion of distinct tokens'] = (topElementsCount, topElementsCountProp),
    output['bottom elements count / proportion of distinct tokens'] = (bottomElementsCount, bottomElementsCountProp)
    return(output)
    


def comparator(inputData):
    output = {}

    return(output)



if __name__ == "__main__":
    inputTextName = sys.argv[1]
    compressedOutputName = sys.argv[2]
    decodedOutputName = sys.argv[3]
    inputFileHandle = open(inputTextName, 'r')    
    testOutput = open(compressedOutputName, 'w')
    decodeTest = open(decodedOutputName, 'w')

    resultsBuffer = main(inputFileHandle)
    statsResults = basicStatistics(resultsBuffer)
    comparisonResults = comparator(resultsBuffer)

    print(statsResults['stats'])
    print(comparisonResults['results'])

    testOutput.write(resultsBuffer['compress ready data'])
    decodeTest.write(resultsBuffer['decoded data'])    
    inputFileHandle.close
    testOutput.close()
    decodeTest.close()
