"""Phrase-aware caption segmentation; preserve every source word in order."""
import re,textwrap
from functools import lru_cache
BAD_END=set('a an the of to with for from and or in on at by as its their this that'.split())
STARTS=set('and but while because when where which whether if rather not instead including without'.split())
def chunks(text):
 for sentence in re.split(r'(?<=[.!?])\s+',text):
  words=sentence.split();N=len(words)
  @lru_cache(None)
  def solve(start):
   if start==N:return (0,())
   best=None
   for end in range(start+4,N+1):
    phrase=' '.join(words[start:end]);lines=textwrap.wrap(phrase,42)
    if len(phrase)>76 or len(lines)>2:break
    tail=solve(end)
    if tail is None:continue
    cost=(len(phrase)-58)**2/100
    if end<N:
     last=words[end-1].lower().strip('.,:;!?');nxt=words[end].lower().strip('.,:;!?')
     cost+=35 if last in BAD_END else 0
     cost-=12 if words[end-1].endswith((',', ';', ':')) or nxt in STARTS else 0
     cost+=15 if nxt in {'of','to','with','for','from'} else 0
    option=(cost+tail[0],(phrase,)+tail[1])
    if best is None or option[0]<best[0]:best=option
   return best
  result=solve(0)
  if result is None:raise ValueError('Cannot caption sentence without short fragments: '+sentence)
  yield from result[1]
