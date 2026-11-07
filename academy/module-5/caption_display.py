import re
PAIRS={'Module Five':'Module 5','O Q':'OQ','Annex Fifteen':'Annex 15','Annex Eleven':'Annex 11','three point two seconds':'3.2 seconds','four seconds':'4 seconds','plus zero point four degrees Celsius':'+0.4 °C','zero point five degrees Celsius':'0.5 °C','zero point six':'0.6','zero point four':'0.4','zero point two':'0.2','ninety one point seven percent':'91.7%','half-degree':'0.5-degree'}
def display(text):
 for a,b in PAIRS.items():text=text.replace(a,b)
 return text
def speech(text):
 for a,b in [('91.7%','ninety one point seven percent'),('3.2','three point two'),('+0.4','plus zero point four'),('0.4','zero point four'),('0.2','zero point two'),('0.5','zero point five'),('0.6','zero point six'),('Annex 15','Annex Fifteen'),('Annex 11','Annex Eleven'),('V-201','V two zero one'),('°C','degrees Celsius')]:text=text.replace(a,b)
 for word in ['DQ','IQ','OQ','PQ','URS','GMP','FAT','CSV']:
  text=re.sub(r'\b'+word+r'\b',' '.join(word),text)
 return text
