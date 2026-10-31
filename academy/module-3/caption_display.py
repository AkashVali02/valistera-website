import re
PAIRS={'E U G M P Annex Eleven':'EU GMP Annex 11','F D A twenty one C F R Part Eleven':'FDA 21 CFR Part 11','I Q':'IQ','Module Three':'Module 3','Module Four':'Module 4','V two zero one':'V-201','D Q':'DQ','G M P':'GMP','U R S':'URS','R zero three':'R-03','S zero seven':'S-07','twenty, forty and sixty degrees Celsius':'20, 40 and 60 °C','plus or minus zero point five degrees Celsius':'±0.5 °C','plus or minus zero point two degrees Celsius':'±0.2 °C','zero point six degrees Celsius':'0.6 °C','zero point five':'0.5','zero point six':'0.6','eighty percent':'80%'}
def display(text):
 for a,b in PAIRS.items():text=text.replace(a,b)
 return text
def speech(text):
 for a,b in [('EU GMP Annex 11','E U G M P Annex Eleven'),('FDA 21 CFR Part 11','F D A twenty one C F R Part Eleven'),('V-201','V two zero one'),('R-03','R zero three'),('S-07','S zero seven'),('DQ','D Q'),('IQ','I Q'),('OQ','O Q'),('PQ','P Q'),('URS','U R S'),('GMP','G M P'),('FAT','F A T'),('CSV','C S V'),('°C','degrees Celsius'),('±','plus or minus ')]:text=text.replace(a,b)
 return text
