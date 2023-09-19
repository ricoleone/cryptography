#######################################################################################
# Name:        genQRRMS
# Description: generates all possible quadgrams from the given text file
#              Returns a dictionary with all digrams found in the text as keys and their 
#              frequency of occurance as the value
#              (Future enhancements: filename as parameter and N the number of grams to return)
# Input:       enter the text file, type of Ngram to produce 2 for BIgrams, 3 for TRIgrams, 
#              and 4 for QUADgrams, the number of Ngrams to output, where the default is all found
# Author:      Rico Leone
# Date:        February 28, 2023
#######################################################################################
from math import log10
import itertools
import frequency_analysis as fa
def genQGRMS(Qfile, n=0 ):
  qgrams = {}
  f = open(Qfile, 'r')
  for line in f:
    key,counts = line.split(" ") 
    qgrams[key.upper()] = float(counts)

  sum = 0.0
  for v in qgrams.values():
    sum += float(v)
  for key in qgrams.keys():
    qgrams[key] = log10(float(qgrams.get(key))/sum)

  qgrams = fa.alpha_order(qgrams)
  if n > 0:
    qgrams = dict(itertools.islice(qgrams.items(), n))
  print("QGRAMS RETURNED = ", len(qgrams), " ", "qgrams")
  return sum, qgrams