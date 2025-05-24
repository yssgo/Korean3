# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from korean import Korean

s = Korean('안녕세상아')
print(s[0])
print('>>> 안')

c1 = Korean.Syllable(letter='안')
print(c1)
print('>>> 안')

c2 = Korean.Syllable(phoneme_onset='ㅇ', phoneme_nucleus='ㅏ', phoneme_coda='ㄴ')
print(c2)
print('>>> 안')

### 초,중,종성 추출
s = Korean('안녕세상아')
print(s[0].phoneme_onset)
print('>>> ㅇ')

print(s[0].phoneme_nucleus)
print('>>> ㅏ')

print(s[0].phoneme_coda)
print('>>> ㄴ')

### 초,중,종성 변경

s = Korean('안녕세상아')
s[0].phoneme_coda = 'ㄹ'
s[0].combine()
print(s[0])
print('>>> 알')

s.join()
print(s)
print('>>> 알녕세상아')

c = Korean.Syllable(letter='우')
c.phoneme_nucleus += 'ㅓ'
c.combine()
print(c)
print('>>> 워')

# * CMU Dictionary - <http://www.speech.cs.cmu.edu/cgi-bin/cmudict>

from cmuToKorean import CMUToKorean

result = CMUToKorean.convert(u'MIDDLE', u'M IH1 D AH0 L')

for v in result:
    print(v)

print('>>> 미덜')
print('>>> 미델')
print('>>> 미들')
