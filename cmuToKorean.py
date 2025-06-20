# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from korean import Korean
import abc
import sys
import re
import six

if int(sys.version[0]) < 3:
    StrType = unicode
    UniChr = unichr
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    StrType = str
    UniChr = chr


class CMUToKorean(object):
    class Condition(object):

        @six.add_metaclass(abc.ABCMeta)
        class Interface(object):

            @abc.abstractmethod
            def test(self, map_, map_index, lhs):
                pass

        class IsFirst(Interface):
            def __init__(self):
                pass

            def test(self, map_, map_index, lhs):
                if map_index[0] == 0:
                    if map_index[1] == 0:
                        return True

                return False

        class IsLast(Interface):
            def __init__(self):
                pass

            def test(self, map_, map_index, lhs):
                last_map_index = [len(map_) - 1, len(map_[len(map_) - 1][0]) - 1]

                if map_index[0] == last_map_index[0]:
                    if map_index[1] == last_map_index[1]:
                        return True

                return False

        class IsLastGroup(Interface):
            def __init__(self):
                pass

            def test(self, map_, map_index, lhs):
                if map_index[0] == len(map_) - 1:
                    return True

                return False

        class IsNotExistsLastVowel(Interface):
            def __init__(self):
                pass

            def test(self, map_, map_index, lhs):
                group_index = map_index[0]
                phonetic_index = map_index[1] + 1

                for token_list in map_[group_index:len(map_)]:
                    phonetic_list = token_list[0]
                    for phonetic in phonetic_list[phonetic_index:len(phonetic_list)]:
                        m = re.match(r'(\D+)(\d)?([!])?', phonetic)
                        symbol = m.groups()[0]
                        if symbol in CMUToKorean.vowel_to_korean_dict:
                            return False

                    phonetic_index = 0

                return True

        class IsExistsFrontInVowel(Interface):
            def __init__(self):
                pass

            def test(self, map_, map_index, lhs):
                group_index = map_index[0]
                phonetic_index = map_index[1] + 1

                for token_list in map_[group_index:len(map_)]:
                    phonetic_list = token_list[0]
                    for phonetic in phonetic_list[phonetic_index:len(phonetic_list)]:
                        m = re.match(r'(\D+)(\d)?([!])?', phonetic)
                        symbol = m.groups()[0]
                        if symbol in CMUToKorean.vowel_to_korean_dict:
                            return True
                        else:
                            return False

                    phonetic_index = 0

                return False

        class IsExistsFrontInPhonetic(Interface):
            phonetic = None

            def __init__(self, phonetic):
                self.phonetic = phonetic

            def test(self, map_, map_index, lhs):
                group_index = map_index[0]
                phonetic_index = map_index[1] + 1

                for token_list in map_[group_index:len(map_)]:
                    phonetic_list = token_list[0]
                    for phonetic in phonetic_list[phonetic_index:len(phonetic_list)]:
                        m = re.match(r'(\D+)(\d)?([!])?', phonetic)
                        symbol = m.groups()[0]

                        if symbol == self.phonetic or phonetic == self.phonetic:
                            return True
                        else:
                            return False

                    phonetic_index = 0

                return False

        class IsExistsBackInVowel(Interface):
            def __init__(self):
                pass

            def test(self, map_, map_index, lhs):
                group_index = map_index[0]

                if map_index[1] == 0:
                    if group_index == 0:
                        return False

                    group_index -= 1
                    phonetic_index = len(map_[group_index][0]) - 1
                else:
                    phonetic_index = map_index[1] - 1

                phonetic = map_[group_index][0][phonetic_index]
                m = re.match(r'(\D+)(\d)?([!])?', phonetic)
                symbol = m.groups()[0]

                if symbol in CMUToKorean.vowel_to_korean_dict:
                    return True

                return False

        class IsExistsBackInPhonetic(Interface):
            phonetic = None

            def __init__(self, phonetic):
                self.phonetic = phonetic

            def test(self, map_, map_index, lhs):
                group_index = map_index[0]

                if map_index[1] == 0:
                    if group_index == 0:
                        return False

                    group_index -= 1
                    phonetic_index = len(map_[group_index][0]) - 1
                else:
                    phonetic_index = map_index[1] - 1

                phonetic = map_[group_index][0][phonetic_index]
                m = re.match(r'(\D+)(\d)?([!])?', phonetic)
                symbol = m.groups()[0]

                if symbol == self.phonetic or phonetic == self.phonetic:
                    return True

                return False

        class IsExistsLatestKorean(Interface):
            korean = None

            def __init__(self, korean):
                self.korean = korean

            def test(self, map_, map_index, lhs):
                found = False
                i = 0
                for i in range(1, len(lhs) + 1):
                    if re.search(StrType(r'[ㄱ-ㅎㅏ-ㅣ가-힣]+'), lhs[-i]):
                        found = True
                        break

                if not found:
                    return False

                if lhs[-i] == self.korean:
                    return True

                return False

        class IsExistsMappingWord(Interface):
            alphabet = None

            def __init__(self, alphabet):
                self.alphabet = alphabet

            def test(self, map_, map_index, lhs):
                group_index = map_index[0]

                if re.search(self.alphabet, map_[group_index][1]):
                    return True

                return False

        class RegexPhoneticGroup(Interface):
            regex = None

            def __init__(self, regex):
                self.regex = regex

            def test(self, map_, map_index, lhs):
                group_index = map_index[0]
                if re.search(self.regex, ''.join(map_[group_index][0])):
                    return True

                return False

        class RegexWordGroup(Interface):
            regex = None

            def __init__(self, regex):
                self.regex = regex

            def test(self, map_, map_index, lhs):
                group_index = map_index[0]
                if re.search(self.regex, ''.join(map_[group_index][1])):
                    return True

                return False

        class RegexWordNextGroup(Interface):
            regex = None

            def __init__(self, regex):
                self.regex = regex

            def test(self, map_, map_index, lhs):
                group_index = map_index[0] + 1

                if len(map_) <= group_index:
                    return False

                if re.search(self.regex, ''.join(map_[group_index][1])):
                    return True

                return False

    class Control(object):
        class IF(object):
            chain = []

            def __init__(self, condition, value):
                self.chain = [{'condition': condition, 'value': value}]

            def ELIF(self, condition, value):
                self.chain.append({'condition': condition, 'value': value})
                return self

            def ELSE(self, value):
                self.chain.append(value)
                return self

    vowel_to_korean_dict = {
        'AA': [
            Control
                .IF(Condition.IsExistsMappingWord('O'), ['오', '어', '아'])
                .ELIF(Condition.IsFirst(), '아')
                .ELIF(Condition.IsLast(), ['아', '어'])
                .ELSE(['아', '어'])
        ],

        'AO': ['오', '어'],
        'AE': ['애'],
        'AY': ['아이', '애이', '아이+', '애이+'],

        'AH': [
            Control
                .IF(Condition.IsFirst(),
                    Control
                    .IF(Condition.IsExistsMappingWord('AU'), '어')
                    .ELIF(Condition.IsExistsBackInPhonetic('Z'), ['아', '어', '애'])
                    .ELSE(['어', '애']))
                .ELIF(Condition.IsLast(), ['아', '어'])
                .ELIF(Condition.IsExistsMappingWord('EI'), ['에이', '이'])
                .ELIF(Condition.IsExistsMappingWord('IU'), ['우', '어'])
                .ELIF(Condition.IsExistsMappingWord('IO'), ['어', '오', '아'])
                .ELIF(Condition.IsExistsMappingWord('UA'), ['어', '아'])
                .ELSE(
                    Control
                    .IF(Condition.IsExistsMappingWord('A'),
                        Control
                        .IF(Condition.IsNotExistsLastVowel(),
                            Control
                            .IF(Condition.RegexWordNextGroup(r'.E'), ['애', '이'])
                            .ELSE(['애', '아']))
                        .ELSE(['애', '아']))
                    .ELIF(Condition.IsExistsMappingWord('E'),
                          Control
                          .IF(Condition.IsExistsFrontInPhonetic('N'), ['에', '으'])
                          .ELSE(['에', '어']))
                    .ELIF(Condition.IsExistsMappingWord('U'), ['어', '우'])
                    .ELIF(Condition.IsExistsMappingWord('O'), ['오', '어', '아'])
                    .ELIF(Condition.IsExistsMappingWord('I'),
                          Control
                          .IF(Condition.IsNotExistsLastVowel(), ['이', '으'])
                          .ELSE('이'))
                )
        ],

        'AW': ['아우', '오우', '아우+', '오우+'],

        'EH': ['에'],

        'ER': [
            Control
                .IF(Condition.IsLast(), ['어', '얼'])
                .ELIF(Condition.IsExistsFrontInVowel(), '어/ㄹ')
                .ELSE('어'),

            Control
                .IF(Condition.IsExistsMappingWord('OR'),
                    Control
                    .IF(Condition.IsLast(), ['오', '올'])
                    .ELIF(Condition.IsExistsFrontInVowel(), '오/ㄹ')
                    .ELSE('오'))
        ],

        'EY': ['에이', '에이+', '에'],

        'EY2': ['에이', '에이+'],

        'IH': ['이'],

        'IY': ['이', '이+'],

        'UW': ['우', '우+'],

        'UH': [
            Control
                .IF(Condition.IsExistsMappingWord('EU'), '이우')
                .ELIF(Condition.IsExistsMappingWord('UE'), '우')
                .ELIF(Condition.IsExistsMappingWord('OO'), '우')
                .ELIF(Condition.IsExistsMappingWord('OU'),
                      Control
                      .IF(Condition.IsExistsBackInPhonetic('Y'), ['우', '오', '어'])
                      .ELIF(Condition.IsExistsBackInPhonetic('SH'), ['우', '오', '어'])
                      .ELSE(['우', '오', '어']))
                .ELIF(Condition.IsExistsMappingWord('U'),
                      Control
                      .IF(Condition.IsExistsBackInPhonetic('Y'), ['우', '오', '어'])
                      .ELIF(Condition.IsExistsBackInPhonetic('SH'), ['우', '오', '어'])
                      .ELSE(['우', '어']))
                .ELSE(['오', '어'])
        ],

        'OW': [
            Control
                .IF(Condition.IsExistsMappingWord('OW'),
                    Control
                    .IF(Condition.IsExistsFrontInVowel(), ['오우+', '오'])
                    .ELSE(['오우', '오']))
                .ELSE('오')
        ],

        'OY': ['오이', '오이+']
    } # yapf: disable

    semivowel_to_korean_dict = {
        'W': ['/우+', '우+'],
        'Y': ['이+']
    } # yapf: disable

    consonant_to_korean_dict = {
        'B': ['ㅂ'],
        'D': ['ㄷ'],
        'F': ['ㅍ'],
        'G': ['ㄱ'],
        'K': ['ㅋ'],
        'M': ['ㅁ'],
        'N': ['ㄴ'],
        'P': ['ㅍ'],
        'T': ['ㅌ'],
        'V': ['ㅂ'],
        'HH': ['/ㅎ'],

        'Z': [
            Control
                .IF(Condition.IsExistsLatestKorean('ㄷ'), '-/ㅈ')
                .ELIF(Condition.IsExistsLatestKorean('ㅌ'), '-/ㅊ')
                .ELIF(Condition.IsLast(), ['/ㅈ', '/ㅅ'])
                .ELSE('/ㅈ')
        ],

        'L': [
            Control
                .IF(Condition.IsLast(), 'ㄹ')
                .ELSE('ㄹ^')    # ex) 글랜
        ],

        'R': [
            Control
                .IF(Condition.IsExistsBackInVowel(),
                    Control
                    .IF(Condition.IsExistsFrontInVowel(), '/ㄹ')
                    .ELIF(Condition.IsLast(),
                          Control
                          .IF(Condition.IsExistsLatestKorean('어'),
                              Control
                              .IF(Condition.RegexWordGroup(r'^.*RE$'), 'ㄹ')
                              .ELSE(['', 'ㄹ']))
                          .ELIF(Condition.IsExistsLatestKorean('아'),
                                Control
                                .IF(Condition.RegexWordGroup(r'^.*RE$'), 'ㄹ')
                                .ELSE(['', 'ㄹ']))
                          .ELIF(Condition.IsExistsLatestKorean('오'), ['ㄹ', '얼'])
                          .ELIF(Condition.IsExistsLatestKorean('우'), ['어', '얼'])
                          .ELIF(Condition.IsExistsLatestKorean('에'), ['어', '얼'])
                          .ELIF(Condition.IsExistsLatestKorean('애'), ['어', '얼'])
                          .ELSE(['ㄹ', '어', '얼']))
                    .ELIF(Condition.IsExistsLatestKorean('어'), ['', 'ㄹ'])
                    .ELIF(Condition.IsExistsLatestKorean('아'), ['', 'ㄹ'])
                    .ELIF(Condition.IsExistsLatestKorean('오'), ['', 'ㄹ'])
                    .ELIF(Condition.IsExistsLatestKorean('우'), ['', 'ㄹ'])
                    .ELSE(['ㄹ', '어', '얼']))
                .ELSE('ㄹ')
        ],

        'S': [
            Control
                .IF(Condition.IsFirst(),
                    Control
                    .IF(Condition.IsExistsMappingWord('SS'), '/ㅆ')
                    .ELSE('/ㅅ'))
                .ELIF(
                    Condition.IsExistsBackInPhonetic('T'),
                    Control
                    .IF(Condition.IsExistsMappingWord('Z'), ['-/ㅊ', '/ㅈ'])    # ex) BLITZKRIEG 리츠,맅즈
                    .ELIF(Condition.IsLast(), '-/ㅊ')
                    .ELIF(Condition.RegexPhoneticGroup(r'.+TS.+'), ['-/ㅊ', '-/ㅅ'])    # ex) FTSM 프츠므, 프스므
                    .ELIF(
                        Condition.RegexPhoneticGroup(r'.+TS'),
                        Control
                            .IF(Condition.IsExistsFrontInVowel(), '-/ㅅ')  # ex) ACCOUNTANCY AH0 K AW1 N T AH0 N T S IY2
                            .ELSE('-/ㅊ')
                    )
                    .ELIF(Condition.IsExistsFrontInVowel(), ['/ㅅ', '-/ㅊ'])  # ex) BATSON 뱉슨, 배츤
                    .ELIF(Condition.IsExistsFrontInPhonetic('T'), '/ㅅ')    # ex) TST 트스트
                    .ELIF(Condition.RegexPhoneticGroup(r'TS.+'), ['-/ㅊ', '/ㅅ'])    # ex) TSM 츠므,트스므
                    .ELSE('-/ㅊ')
                )

                .ELSE('/ㅅ')
        ],

        'NG': [
            Control
                .IF(Condition.IsExistsFrontInVowel(), '~ㅇㄱ')
                .ELSE('~ㅇ')
        ],

        'SH': ['/ㅅ#'],

        'CH': [
            Control
                .IF(Condition.IsLast(), '치')
                .ELIF(Condition.IsLastGroup(),
                      Control
                      .IF(Condition.RegexWordGroup(r'.*CHE.*'), '치')
                      .ELSE('/ㅊ'))
                .ELSE('/ㅊ')
        ],

        'DH': [
            Control
                .IF(Condition.IsFirst(), 'ㄷ')
                .ELIF(Condition.RegexWordNextGroup(r'^A'), '/ㅅ')
                .ELIF(Condition.IsExistsBackInPhonetic('S'), '')  # 묵음
                .ELIF(Condition.IsExistsBackInPhonetic('Z'), '')  # 묵음
                .ELIF(Condition.IsExistsBackInPhonetic('ER'), 'ㄷ')
                .ELIF(Condition.IsExistsBackInPhonetic('OW'), 'ㄷ')
                .ELIF(Condition.IsExistsBackInPhonetic('AH'), 'ㅅ')
                .ELIF(Condition.IsExistsBackInPhonetic('IY'), 'ㅅ')
                .ELIF(Condition.IsExistsBackInPhonetic('IH'), 'ㅅ')
                .ELIF(Condition.IsExistsBackInPhonetic('Y'), 'ㅅ')
                .ELSE(['ㄷ', '/ㅅ'])
        ],

        'JH': [
            Control
                .IF(Condition.IsLast(), '지')
                .ELSE('/ㅈ')
        ],

        'TH': [
            Control
                .IF(Condition.IsFirst(), '/ㅅ')
                .ELIF(Condition.IsNotExistsLastVowel(), '/ㅅ')
                .ELSE(
                    Control
                      .IF(Condition.IsExistsBackInPhonetic('S'), '')
                      .ELIF(Condition.IsExistsBackInPhonetic('Z'), '')
                      .ELSE('/ㅅ')
                )
        ],

        'ZH': [
            Control
                .IF(Condition.IsFirst(),
                    Control
                    .IF(Condition.IsExistsMappingWord('X'), '/ㅅ#')
                    .ELSE('/ㅈ#'))
                .ELIF(Condition.IsExistsMappingWord('S'),
                      Control
                      .IF(Condition.RegexWordNextGroup(r'^IA'), '시')
                      .ELSE('/ㅈ#'))
                .ELSE('/ㅈ#')
        ],
    } # yapf: disable

    operation_set = (
        '/', '~', '+', '-', '^', '#', '?'
    ) # yapf: disable

    alphabet_vowel_to_cmu_dict = {
        'A': 'AA',
        'E': 'EH',
        'I': 'IH',
        'O': 'AO',
        'U': 'UH',
        'W': 'W',
        'Y': 'Y',
    } # yapf: disable

    alphabet_consonant_set = (
        'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
        'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Z'
    ) # yapf: disable

    alphabet_vowel_set = (
        'A', 'E', 'I', 'O', 'U', 'W', 'Y'
    ) # yapf: disable

    korean_convert_sharp_dict = {
        'ㅏ': 'ㅑ',
        'ㅓ': 'ㅕ',
        'ㅗ': 'ㅛ',
        'ㅜ': 'ㅠ',
        'ㅐ': 'ㅒ',
        'ㅔ': 'ㅖ',
        'ㅡ': 'ㅟ',
    } # yapf: disable

    korean_coda_sound = {
        'ㄱ': 'ㄱ', 'ㅋ': 'ㄱ',
        'ㄴ': 'ㄴ',
        'ㄷ': 'ㅅ', 'ㅌ': 'ㅅ', 'ㅅ': 'ㅅ',
        'ㅈ': 'ㄷ', 'ㅊ': 'ㄷ', 'ㅎ': 'ㄷ',
        'ㄹ': 'ㄹ',
        'ㅁ': 'ㅁ',
        'ㅂ': 'ㅂ', 'ㅍ': 'ㅂ',
        'ㅇ': 'ㅇ',

        'ㄲ': 'ㄱ',
        'ㅆ': 'ㅅ',
    } # yapf: disable

    @staticmethod
    def convert(word, phonetic, **kwargs):
        word = StrType(word).upper()
        phonetic = StrType(phonetic).upper()

        map_ = CMUToKorean._phonetic_word_mapping(word, phonetic)
        if not map_:
            return None

        combination = []
        map_index = [0, 0]

        for group in map_:
            if CMUToKorean._pattern_exception(map_, map_index[0], combination):
                map_index[0] += 1
                map_index[1] = 0
                continue

            for phonetic in group[0]:
                m = re.match(r'(\D+)(\d)?([?])?', phonetic)
                regrp = m.groups()
                symbol = regrp[0]
                number = regrp[1]
                op = regrp[2]
                ref_dict = None

                if symbol in CMUToKorean.consonant_to_korean_dict:
                    ref_dict = CMUToKorean.consonant_to_korean_dict
                elif symbol in CMUToKorean.semivowel_to_korean_dict:
                    ref_dict = CMUToKorean.semivowel_to_korean_dict
                elif symbol in CMUToKorean.vowel_to_korean_dict:
                    ref_dict = CMUToKorean.vowel_to_korean_dict

                if not ref_dict:
                    if phonetic not in CMUToKorean.operation_set:
                        return None
                    value = phonetic

                elif number and (symbol + number) in ref_dict:
                    value = ref_dict[symbol + number]
                else:
                    value = ref_dict[symbol]

                # op code '?'가 존재시 생략도 추가한다
                if op == '?':
                    clone = []
                    clone.extend(value)
                    clone.append('')
                    value = clone

                # combination
                # combination = value_list * combination
                combination = CMUToKorean._join_process(map_, map_index, combination, value)
                map_index[1] += 1

            map_index[0] += 1
            map_index[1] = 0

        result = CMUToKorean._assembly(src_korean_list=combination, **kwargs)
        return result

    @staticmethod
    def _assembly(src_korean_list, **kwargs):
        def join(lhs, rhs):
            r1 = []

            if lhs and isinstance(lhs, list):
                for l in lhs:
                    r2 = join(l, rhs)
                    if isinstance(r2, list):
                        r1.extend(r2)
                    else:
                        r1.append(r2)

            elif rhs and isinstance(rhs, list):
                for r in rhs:
                    r2 = join(lhs, r)
                    if isinstance(r2, list):
                        r1.extend(r2)
                    else:
                        r1.append(r2)
            else:
                if not lhs:
                    lhs = ''

                if not rhs:
                    rhs = ''

                return [lhs + rhs]

            return r1

        def syllable_join(dest, src_onset, src_nucleus, src_coda):
            if not src_onset:
                src_onset = [None]
            if not src_nucleus:
                src_nucleus = [None]
            if not src_coda:
                src_coda = [None]

            if not isinstance(src_onset, list):
                src_onset = [src_onset]
            if not isinstance(src_nucleus, list):
                src_nucleus = [src_nucleus]
            if not isinstance(src_coda, list):
                src_coda = [src_coda]

            r = []
            for o in src_onset:
                for n in src_nucleus:
                    for c in src_coda:
                        r.append(StrType(Korean.Syllable(phoneme_onset=o, phoneme_nucleus=n, phoneme_coda=c)))

            return join(dest, r)

        # pass 1
        # 한글을 조립한다
        pass1_result = []

        for text in src_korean_list:
            combination = []
            korean = Korean(text)
            korean_len = len(korean)
            carry_onset = None
            carry_nucleus = None
            carry_coda = None
            consonant_continuous = False
            op = None
            i = 0

            while i < korean_len:
                cur = korean[i]
                consonant_combined = False

                if isinstance(cur, Korean.Syllable):
                    # op code 라면
                    if op:
                        # 해당 자음은 무조건 밑받침
                        if op == '~':
                            # 자음만 가능
                            if not cur.is_completed() and not cur.phoneme_nucleus:
                                # 캐리의 초성과 조합배열이 존재 안한다면
                                if not carry_onset and len(combination) == 0:
                                    carry_onset = StrType(cur)

                                # 캐리의 초성, 중성이 존재 안한다면
                                if not carry_onset and not carry_nucleus:
                                    # 각 조합의 마지막에 종성을 넣는다
                                    for j in range(0, len(combination)):
                                        last_elem = Korean.Syllable(letter=combination[j][-1])
                                        last_elem.phoneme_coda = StrType(cur)
                                        last_elem.combine()
                                        combination[j] = combination[j][:-1]
                                        combination[j] += StrType(last_elem)

                                else:
                                    carry_coda = StrType(cur)
                            else:
                                # 완성형 글자라면 예외
                                # middle.exception
                                op = None
                                continue

                        # 종성+모음 조합에서 종성이 초성에 한번 더 나타나게 한다
                        elif op == '^':
                            if not carry_coda:
                                # middle.exception
                                # 캐리에 종성이 존재해야만 한다
                                op = None
                                continue

                            # 현재 초성만 존재하는 경우
                            if not cur.is_completed() and cur.phoneme_onset:
                                # middle.exception
                                # 초성만 존재할순 없다
                                op = None
                                continue

                            # 현재 초성+중성 조합일 경우 초성이 'ㅇ' 이 아니라면
                            if cur.phoneme_onset and cur.phoneme_nucleus:
                                if cur.phoneme_onset != 'ㅇ':
                                    op = None
                                    continue

                            tmp_coda = carry_coda

                            combination = syllable_join(combination,
                                                        carry_onset,
                                                        carry_nucleus,
                                                        carry_coda
                            ) # yapf: disable

                            carry_onset = tmp_coda
                            carry_nucleus = cur.phoneme_nucleus
                            carry_coda = cur.phoneme_coda

                        # 캐리와 합성
                        elif op == '+':
                            # 중성 합성만 가능하다
                            if carry_nucleus and cur.phoneme_nucleus:
                                if carry_coda:
                                    # 캐리에 종성이 존재하는 경우
                                    op = None
                                    continue

                                if cur.phoneme_onset and cur.phoneme_onset != 'ㅇ':
                                    # 현재 글자에 초성이 존재하지만 'ㅇ' 이 아닐경우
                                    op = None
                                    continue

                                if isinstance(carry_nucleus, list):
                                    for i in range(0, len(carry_nucleus)):
                                        # 캐리의 중성과 현재의 중성이 일치하지 않으면
                                        if carry_nucleus[i] != cur.phoneme_nucleus:
                                            nucleus = carry_nucleus[i] + cur.phoneme_nucleus
                                            if nucleus not in Korean.phoneme_nucleus_phonetic_combine_dict:
                                                carry_nucleus[i] = cur.phoneme_nucleus
                                            else:
                                                carry_nucleus[i] = Korean.phoneme_nucleus_phonetic_combine_dict[nucleus]

                                # 캐리의 중성과 현재의 중성이 일치하지 않으면
                                elif carry_nucleus != cur.phoneme_nucleus:
                                    nucleus = carry_nucleus + cur.phoneme_nucleus
                                    if nucleus not in Korean.phoneme_nucleus_phonetic_combine_dict:
                                        # 중성 발음 합성이 존재하지 않을경우
                                        op = None
                                        continue

                                    carry_nucleus = Korean.phoneme_nucleus_phonetic_combine_dict[nucleus]

                                carry_coda = cur.phoneme_coda

                            else:
                                # 중성+초성은 합성불가능
                                op = None
                                continue

                        # ㅅ# -> 쉬,샤, ㅈ# -> 쥐,쟈
                        elif op == '#':
                            # 캐리가 초성+중성 형태라면
                            if carry_onset and carry_nucleus and not carry_coda:
                                # 조합후 다시 처리
                                combination = syllable_join(combination,
                                                            carry_onset,
                                                            carry_nucleus,
                                                            carry_coda
                                ) # yapf: disable

                                carry_onset = None
                                carry_nucleus = None
                                carry_coda = None
                                continue

                            # 캐리의 초성이 존재 하지 않는다면
                            if not carry_onset:
                                carry_onset = 'ㅇ'

                            # 캐리의 종성이 존재한다면
                            if carry_coda:
                                # 종성을 따로 빼낸뒤 조합
                                tmp_coda = carry_coda
                                carry_coda = None

                                combination = syllable_join(combination,
                                                            carry_onset,
                                                            carry_nucleus,
                                                            carry_coda
                                ) # yapf: disable

                                carry_onset = tmp_coda
                                carry_coda = None

                            # 현재 모음이 존재하고 초성이 'ㅇ' 일때
                            # 또는 모음만 존재할때
                            if (cur.phoneme_nucleus and cur.phoneme_onset == 'ㅇ')\
                                    or (cur.phoneme_nucleus and not cur.phoneme_onset):

                                if cur.phoneme_nucleus in CMUToKorean.korean_convert_sharp_dict:
                                    carry_nucleus = CMUToKorean.korean_convert_sharp_dict[cur.phoneme_nucleus]
                                    carry_coda = cur.phoneme_coda
                                else:
                                    # middle.exception
                                    # 존재하지 않으면 무시
                                    op = None
                                    continue

                            # 현재 완성형 글자이면
                            elif cur.is_completed():
                                # ㅅ#가 -> 쉬가
                                carry_nucleus = ['ㅟ', 'ㅠ'] if len(combination) == 0 else 'ㅟ'

                                combination = syllable_join(combination,
                                                            carry_onset,
                                                            carry_nucleus,
                                                            carry_coda
                                ) # yapf: disable

                                carry_onset = cur.phoneme_onset
                                carry_nucleus = cur.phoneme_nucleus
                                carry_coda = cur.phoneme_coda

                            # 현재 자음만 존재한다면
                            else:
                                carry_nucleus = ['ㅟ', 'ㅠ'] if len(combination) == 0 else 'ㅟ'

                                # 자음이 연속 된다면
                                if consonant_continuous:
                                    combination = syllable_join(combination,
                                                                carry_onset,
                                                                carry_nucleus,
                                                                carry_coda
                                    ) # yapf: disable

                                    carry_onset = cur.phoneme_onset
                                    carry_nucleus = cur.phoneme_nucleus
                                    carry_coda = cur.phoneme_coda
                                else:
                                    carry_coda = cur.phoneme_onset

                                consonant_combined = True

                        op = None

                    # 현재글자가 완성형이고 초성이 'ㅇ' 이면
                    elif cur.is_completed() and cur.phoneme_onset == 'ㅇ':

                        # 캐리가 존재하지 않으면
                        if not carry_onset and not carry_nucleus and not carry_coda:
                            carry_onset = cur.phoneme_onset
                            carry_nucleus = cur.phoneme_nucleus
                            carry_coda = cur.phoneme_coda

                        # 캐리에 초성만 존재한다면(ㅊ오 -> 초)
                        elif carry_onset and not carry_nucleus and not carry_coda:
                            carry_nucleus = cur.phoneme_nucleus
                            carry_coda = cur.phoneme_coda

                        # 캐리에 종성이 존재하면 연음
                        elif carry_coda:
                            # 종성을 따로 빼낸뒤 조합
                            tmp_coda = carry_coda
                            carry_coda = None

                            combination = syllable_join(combination,
                                                        carry_onset,
                                                        carry_nucleus,
                                                        carry_coda
                            ) # yapf: disable

                            carry_onset = tmp_coda
                            carry_nucleus = cur.phoneme_nucleus
                            carry_coda = cur.phoneme_coda

                        # 현재 중성과 캐리의 중성이 같다면
                        elif carry_nucleus == cur.phoneme_nucleus:

                            # 종성만 붙여넣는다 (터어, 터얼 -> 터, 털)
                            carry_coda = cur.phoneme_coda

                        else:
                            combination = syllable_join(combination,
                                                        carry_onset,
                                                        carry_nucleus,
                                                        carry_coda
                            ) # yapf: disable

                            carry_onset = cur.phoneme_onset
                            carry_nucleus = cur.phoneme_nucleus
                            carry_coda = cur.phoneme_coda

                    # 현재글자가 모음만 존재한다면
                    elif not cur.phoneme_onset and not cur.phoneme_coda and cur.phoneme_nucleus:
                        # middle.exception
                        # 모음만 존재하는 형태가 오지는 않을것

                        # 캐리에 초성이 존재하지 않으면
                        if not carry_onset:
                            carry_onset = 'ㅇ'

                        # 캐리에 초성/중성이 존재한다면
                        if carry_onset and carry_nucleus:

                            # 캐리에 종성이 존재하면
                            if carry_coda:
                                tmp_onset = carry_coda
                                carry_coda = None
                            else:
                                tmp_onset = 'ㅇ'

                            combination = syllable_join(combination,
                                                        carry_onset,
                                                        carry_nucleus,
                                                        carry_coda
                            ) # yapf: disable

                            carry_onset = tmp_onset
                            carry_nucleus = cur.phoneme_nucleus
                            carry_coda = None

                        # 캐리에 초성이 존재하면
                        elif carry_onset:
                            carry_nucleus = cur.phoneme_nucleus

                    # 현재글자가 자음만 존재한다면
                    elif not cur.phoneme_nucleus:

                        # 이미 캐리에 자음이 존재한다면
                        if carry_onset:

                            # 자음이 연속 된다면
                            if consonant_continuous:

                                # 종성을 따로 빼낸뒤 조합
                                tmp_onset = carry_coda
                                carry_coda = None

                                combination = syllable_join(combination,
                                                            carry_onset,
                                                            carry_nucleus,
                                                            carry_coda
                                ) # yapf: disable

                                carry_onset = tmp_onset
                                carry_nucleus = 'ㅡ'
                                carry_coda = cur.phoneme_onset
                                consonant_combined = True

                            elif carry_nucleus and carry_coda:
                                combination = syllable_join(combination,
                                                            carry_onset,
                                                            carry_nucleus,
                                                            carry_coda
                                ) # yapf: disable

                                carry_onset = cur.phoneme_onset
                                carry_nucleus = cur.phoneme_nucleus
                                carry_coda = cur.phoneme_coda

                            elif carry_nucleus:
                                carry_coda = cur.phoneme_onset

                            else:
                                # '으' 형태로 만든다 (T L -> 틀)
                                carry_nucleus = 'ㅡ'
                                carry_coda = cur.phoneme_onset
                                consonant_combined = True
                        else:
                            carry_onset = cur.phoneme_onset

                    else:
                        # 캐리에 초성/중성이 존재한다면
                        if carry_onset and carry_nucleus:
                            combination = syllable_join(combination,
                                                        carry_onset,
                                                        carry_nucleus,
                                                        carry_coda
                            ) # yapf: disable

                        carry_onset = cur.phoneme_onset
                        carry_nucleus = cur.phoneme_nucleus
                        carry_coda = cur.phoneme_coda

                    if consonant_combined:
                        consonant_continuous = True
                    else:
                        consonant_continuous = False

                else:
                    # 이전의 op code가 # 이었다면
                    if op == '#':
                        # 캐리에 초성만 존재시
                        if carry_onset and not carry_nucleus and not carry_coda:
                            carry_nucleus = ['ㅟ', 'ㅠ'] if len(combination) == 0 else 'ㅟ'

                    op = None

                    # 캐리를 강제 조합한다
                    if cur == '/':
                        if carry_onset:
                            # 중성이 존재 하지않으면
                            if not carry_nucleus:
                                carry_nucleus = 'ㅡ'

                            # 초성이 존재 안한다면
                            if not carry_onset:
                                carry_onset = 'ㅇ'

                            combination = syllable_join(combination,
                                                        carry_onset,
                                                        carry_nucleus,
                                                        carry_coda
                            ) # yapf: disable

                            carry_onset = None
                            carry_nucleus = None
                            carry_coda = None
                            consonant_continuous = False

                    # 이전 캐리를 지운다
                    elif cur == '-':
                        if carry_coda:
                            carry_coda = None
                        elif carry_nucleus:
                            carry_nucleus = None
                        elif carry_onset:
                            carry_onset = None

                    # 무시
                    elif cur == '?':
                        pass

                    # op code를 저장
                    else:
                        op = cur

                i += 1

            # 남은 캐리 처리
            if carry_onset or carry_nucleus or carry_coda:
                # 중성이 존재 하지않으면
                if not carry_nucleus:

                    # 이전의 op code가 # 이었다면
                    if op == '#':
                        carry_nucleus = ['ㅟ', 'ㅠ'] if len(combination) == 0 else 'ㅟ'
                    else:
                        carry_nucleus = 'ㅡ'

                # 초성이 존재 안한다면
                if not carry_onset:
                    carry_onset = 'ㅇ'

                combination = syllable_join(combination,
                                            carry_onset,
                                            carry_nucleus,
                                            carry_coda
                ) # yapf: disable

            pass1_result.extend(combination)

        # pass 2
        # 종성 처리
        pass2_result = []

        for text in pass1_result:
            combination = []
            korean = Korean(text)
            korean_len = len(korean)

            for i in range(0, korean_len):
                cur = korean[i]

                if not isinstance(cur, Korean.Syllable):
                    continue

                # 종성이 존재하지 않으면
                if not cur.phoneme_coda:
                    combination = join(combination, StrType(cur))
                    continue

                # 종성 발음
                if 'raw_coda' in kwargs and kwargs['raw_coda']:
                    sound_coda = cur.phoneme_coda
                else:
                    if cur.phoneme_coda in CMUToKorean.korean_coda_sound:
                        sound_coda = CMUToKorean.korean_coda_sound[cur.phoneme_coda]
                    else:
                        sound_coda = cur.phoneme_coda

                sound_syllable = Korean.Syllable(phoneme_onset=cur.phoneme_onset,
                                                 phoneme_nucleus=cur.phoneme_nucleus,
                                                 phoneme_coda=sound_coda
                ) # yapf: disable

                # ㅎ,ㅅ,ㅆ,ㅈ,ㅊ 은 받침으로 불가능
                if cur.phoneme_coda in ('ㅎ', 'ㅅ', 'ㅆ', 'ㅈ', 'ㅊ'):
                    syllable1 = Korean.Syllable(phoneme_onset=cur.phoneme_onset,
                                                phoneme_nucleus=cur.phoneme_nucleus,
                                                phoneme_coda=None
                    ) # yapf: disable

                    syllable2 = Korean.Syllable(phoneme_onset=cur.phoneme_coda,
                                                phoneme_nucleus='ㅡ',
                                                phoneme_coda=None
                    ) # yapf: disable

                    value = StrType(syllable1) + StrType(syllable2)
                else:
                    prolonged = False

                    while True:
                        # ㅁㄴㅇㄹ은 연음하지 않음
                        if cur.phoneme_coda in ('ㅁ', 'ㄴ', 'ㅇ', 'ㄹ'):
                            break

                        next = korean[i + 1] if i + 1 < korean_len else None
                        if next:
                            # 종성과 다음글자의 초성이 같으면 연음하지 않음
                            if cur.phoneme_coda == next.phoneme_onset:
                                break

                            # 종성이 ㅋ 이고 다음 초성이 ㅅ 이면 연음하지 않음
                            elif cur.phoneme_coda == 'ㅋ' and next.phoneme_onset == 'ㅅ':
                                break

                            # 현재 인덱스가 뒤에서 두번째 일때
                            elif i == (korean_len - 2):
                                # 종성이 ㅋ 일때 그라면
                                if cur.phoneme_coda == 'ㅋ':
                                    if next.phoneme_onset == 'ㄱ' and next.phoneme_coda == 'ㅡ':
                                        break

                                # 종성이 ㅌ 일때 드,츠 라면
                                if cur.phoneme_coda == 'ㅌ':
                                    if next.phoneme_onset == 'ㄷ' and next.phoneme_coda == 'ㅡ':
                                        break

                                    if next.phoneme_onset == 'ㅊ' and next.phoneme_coda == 'ㅡ':
                                        break

                                # 종성이 ㅂ 일때 플 라면
                                if cur.phoneme_coda == 'ㅂ':
                                    if next.phoneme_onset == 'ㅍ' and next.phoneme_coda == 'ㅡ':
                                        break

                                # 종성이 ㄷ 일때 플 라면
                                if cur.phoneme_coda == 'ㄷ':
                                    if next.phoneme_onset == 'ㅌ' and next.phoneme_coda == 'ㅡ':
                                        break

                        prolonged = True
                        break

                    if prolonged:
                        syllable1 = Korean.Syllable(phoneme_onset=cur.phoneme_onset,
                                                    phoneme_nucleus=cur.phoneme_nucleus,
                                                    phoneme_coda=None
                        ) # yapf: disable

                        syllable2 = Korean.Syllable(phoneme_onset=cur.phoneme_coda,
                                                    phoneme_nucleus='ㅡ',
                                                    phoneme_coda=Nonei
                        ) # yapf: disable

                        value = [StrType(sound_syllable), StrType(syllable1) + StrType(syllable2)]
                    else:
                        value = StrType(sound_syllable)

                """
                # middle.comment
                # 160127 다른방법 사용

                # 처음이면 연음하지 않는다
                if i == 0:
                    value = StrType(sound_syllable)

                # 마지막이면
                # elif i == (korean_len - 1):
                else:
                    # ㅁㄴㅇㄹ 제외하고 전부 연음
                    # ㅎ,ㅅ,ㅆ,ㅈ,ㅊ 은 받침으로 불가능
                    # ㅃ,ㄲ,ㄸ,ㅉ 는 애초에 존재하지 않음

                    if cur.phoneme_coda in ('ㅎ', 'ㅅ', 'ㅆ', 'ㅈ', 'ㅊ'):
                        syllable1 = Korean.Syllable(phoneme_onset=cur.phoneme_onset,
                                                    phoneme_nucleus=cur.phoneme_nucleus,
                                                    phoneme_coda=None
                        ) # yapf: disable

                        syllable2 = Korean.Syllable(phoneme_onset=cur.phoneme_coda,
                                                    phoneme_nucleus='ㅡ',
                                                    phoneme_coda=None
                        ) # yapf: disable

                        value = StrType(syllable1) + StrType(syllable2)
                    elif cur.phoneme_coda in ('ㅁ', 'ㄴ', 'ㅇ', 'ㄹ'):
                        value = StrType(sound_syllable)
                    else:
                        syllable1 = Korean.Syllable(phoneme_onset=cur.phoneme_onset,
                                                    phoneme_nucleus=cur.phoneme_nucleus,
                                                    phoneme_coda=None
                        ) # yapf: disable

                        syllable2 = Korean.Syllable(phoneme_onset=cur.phoneme_coda,
                                                    phoneme_nucleus='ㅡ',
                                                    phoneme_coda=None
                        ) # yapf: disable

                        value = [StrType(sound_syllable), StrType(syllable1) + StrType(syllable2)]
                """

                combination = join(combination, value)

            pass2_result.extend(combination)

        result = sorted(set(pass2_result))
        return result

    @staticmethod
    def _pattern_exception(map_, group_index, combination):
        group_len = len(map_)
        group = map_[group_index]

        word = group[1]
        word_vowel_count = 0
        word_consonant_count = 0
        word_type = ''

        for c in word:
            if c in CMUToKorean.alphabet_vowel_set:
                word_vowel_count += 1
                word_type += 'V'
            elif c in CMUToKorean.alphabet_consonant_set:
                word_consonant_count += 1
                word_type += 'C'
            else:
                # 특수문자
                word_type += 'S'

        phonetic_list = group[0]
        phonetic_vowel_count = 0
        phonetic_consonant_count = 0
        phonetic_type = ''

        for c in phonetic_list:
            m = re.match(r'(\D+)(\d)?([?])?', c)
            symbol = m.groups()[0]

            if symbol in CMUToKorean.vowel_to_korean_dict:
                phonetic_vowel_count += 1
                phonetic_type += 'V'
            elif symbol in CMUToKorean.semivowel_to_korean_dict:
                phonetic_vowel_count += 1
                phonetic_type += 'V'
            elif symbol in CMUToKorean.consonant_to_korean_dict:
                phonetic_consonant_count += 1
                phonetic_type += 'C'

            else:
                # 특수문자
                phonetic_type += 'S'

        # 그룹이 마지막이 아니고
        # word type 이 C+V+C+ 패턴이고 (COL)
        # phonetic type 이 C+ 패턴일때 (K L)
        if group_index < group_len - 1 \
                and re.search(r'^C+V+C+$', word_type) and re.search(r'^C+$', phonetic_type):
            # word 모음의 위치에 phonetic 쪽에 새로운 모음을 추가시킨다
            for i in range(0, len(word_type)):
                if word_type[i] == 'V':
                    group[0].insert(i, CMUToKorean.alphabet_vowel_to_cmu_dict[word[i]])

        # word 가 .+E 패턴이고 (DLE)
        # phonetic type 이 C+V+C+ 패턴일때 (D AH L)
        elif re.search(r'^.+E$', word) and re.search(r'^C+VC+$', phonetic_type):
            # op '?' 을 추가한다(생략가능)
            for i in range(0, len(phonetic_type)):
                if phonetic_type[i] == 'V':
                    group[0][i] += '?'

            # op '/' 을 추가한다
            group[0].insert(0, '/')

        # word type 이 CC 패턴이고 (SM)
        # phonetic type 이 CVC 패턴일때 (ZH AH M)
        elif re.search(r'^CC$', word_type) and re.search(r'^CVC$', phonetic_type):
            # op '?' 을 추가한다(생략가능)
            for i in range(0, len(phonetic_type)):
                if phonetic_type[i] == 'V':
                    group[0][i] += '?'

            # op '/' 을 추가한다
            group[0].insert(0, '/')

        # word 특수문자 처리
        if re.search(r'^.+-$', word):
            group[0].append('/')
        elif re.search(r'^-.+$', word):
            group[0].insert(0, '/')

        return False

    @staticmethod
    def _join_process(map_, map_index, lhs, rhs):
        if lhs and isinstance(lhs, list):
            build_list = []
            for lv in lhs:
                result = CMUToKorean._join_process(map_, map_index, lv, rhs)
                if result:
                    if isinstance(result, list):
                        build_list.extend(result)
                    else:
                        build_list.append(result)

            return build_list

        elif rhs and isinstance(rhs, list):
            build_list = []
            for rv in rhs:
                result = CMUToKorean._join_process(map_, map_index, lhs, rv)
                if result:
                    if isinstance(result, list):
                        build_list.extend(result)
                    else:
                        build_list.append(result)

            return build_list

        elif isinstance(rhs, StrType):
            if not lhs:
                lhs = ''

            if not rhs:
                rhs = ''

            return [lhs + rhs]
        elif isinstance(rhs, CMUToKorean.Control.IF):
            for statement in rhs.chain:
                if isinstance(statement, dict):
                    if isinstance(statement['condition'], CMUToKorean.Condition.Interface):
                        if statement['condition'].test(map_, map_index, lhs):
                            return CMUToKorean._join_process(map_, map_index, lhs, statement['value'])
                    else:
                        # middle.error
                        return None
                else:
                    return CMUToKorean._join_process(map_, map_index, lhs, statement)

        return None

    @staticmethod
    def _phonetic_word_mapping(word, phonetic):
        # 자음은 C 모음은 V

        if not word:
            return None
        elif not phonetic:
            return None

        # middle.comment
        # word가 공백이 존재하는지 체크 필요

        word = StrType(word)
        word.upper()
        word_type_list = []

        for c in word:
            if c in CMUToKorean.alphabet_vowel_set:
                word_type_list.append([c, 'V'])
            elif c in CMUToKorean.alphabet_consonant_set:
                word_type_list.append([c, 'C'])
            else:
                # 특수문자
                # 자음으로 취급
                word_type_list.append([c, 'C'])

        # middle.comment
        # CMU 발음기호 존재여부 체크 필요

        phonetic = StrType(phonetic)
        phonetic.upper()
        phonetic_list = phonetic.split()
        phonetic_type_list = []

        for c in phonetic_list:
            m = re.match(r'(\D+)(\d)?([?])?', c)
            symbol = m.groups()[0]

            # 자음은 세기가 (EX. AA1, AH0..) 존재하지 않는다
            if symbol in CMUToKorean.vowel_to_korean_dict:
                phonetic_type_list.append([c, 'V'])
            elif symbol in CMUToKorean.semivowel_to_korean_dict:
                phonetic_type_list.append([c, 'V'])
            elif symbol in CMUToKorean.consonant_to_korean_dict:
                phonetic_type_list.append([c, 'C'])
            else:
                # 특수문자
                # 자음으로 취급
                phonetic_type_list.append([c, 'C'])

        result = []
        phonetic_index = 0
        phonetic_len = len(phonetic_type_list)
        word_index = 0
        word_len = len(word_type_list)

        while phonetic_index < phonetic_len:
            add_vowel_group = False
            add_consonant_group = False
            add_group_continue = False
            vowel_r = False
            phonetic = phonetic_type_list[phonetic_index][0]
            type = phonetic_type_list[phonetic_index][1]

            # phonetic group
            count = 1
            index = phonetic_index + 1

            # middle.comment
            # 예외로 처음부터 일치하지 않다면
            # 묵음 혹은 자음첨가 일 수 있다
            if phonetic_index == 0 and type != word_type_list[index - 1][1]:
                if type == 'V':
                    # ex) CABOK  AE1 B OW0
                    add_consonant_group = True
                    add_group_continue = True
                else:
                    add_vowel_group = True
                    add_group_continue = True

                    # phonetic 에 모음그룹 추가
                    while index < phonetic_len:
                        value = phonetic_type_list[index]
                        if type != 'V':
                            break

                        index += 1
                        count += 1

                        # middle.comment
                        # 예외로 phonetic 에서 ER이 존재하면 자음그룹을 추가한다
                        if re.search(r'ER\d', value[0]):
                            add_group_continue = True
                            break

            # middle.comment
            # 예외로 vowel phonetic 에서 ER이 존재하면 자음그룹을 추가한다
            # ER 은 VC와 동일하게 취급
            elif re.search(r'ER\d', phonetic):
                add_consonant_group = True

            else:
                while index < phonetic_len:
                    value = phonetic_type_list[index]
                    if type != value[1]:
                        break

                    index += 1
                    count += 1

                    # middle.comment
                    # 예외로 vowel phonetic 에서 ER이 존재하면 자음그룹을 추가한다
                    if re.search(r'ER\d', value[0]):
                        add_consonant_group = True
                        break

            group = [phonetic_list[phonetic_index:index], None]
            phonetic_index = index

            # middle.comment
            # 예외로 phonetic 에서 C 타입이고 다음이 ER 일때, 현재가 'R'이 아닐때
            # R을 모음으로 취급한다
            if type == 'C' and count == 1 and group[0][0] != 'R':
                if phonetic_index < phonetic_len and re.search(r'ER\d', phonetic_list[phonetic_index]):
                    vowel_r = True

            # middle.comment
            # 예외로 phonetic 에서 CC+ 형태이고
            # word의 타입이 CV 형태라면 모음그룹을 한번 허용한다
            # (CVVCCC, CVCCC, ...등등)
            if type == 'C' and count >= 2:
                if word_index + 1 < word_len \
                        and word_type_list[word_index][1] == 'C' \
                        and word_type_list[word_index + 1][1] == 'V':
                        add_vowel_group = True
                        add_group_continue = True

            # word group
            token = ''
            index = word_index

            if phonetic_index >= phonetic_len:
                if word_len - word_index >= 1:
                    for value in word_type_list[word_index:word_len]:
                        token += value[0]

                word_index = word_len

            else:
                while index < word_len:
                    value = word_type_list[index]

                    if vowel_r and value[0] == 'R':
                        # R을 모음으로 취급
                        vowel_r = False
                        value[1] = 'V'

                    if value[1] != type:

                        # 모음 그룹을 허용한다면
                        if add_vowel_group:
                            while index < word_len:
                                value = word_type_list[index]
                                if value[1] != 'V':
                                    break

                                token += value[0]
                                index += 1

                            add_vowel_group = False

                            # 계속
                            if add_group_continue:
                                add_group_continue = False
                                continue
                            else:
                                break

                        # 자음 그룹을 추가한다면
                        elif add_consonant_group:
                            while index < word_len:
                                value = word_type_list[index]
                                if value[1] != 'C':
                                    break

                                token += value[0]
                                index += 1

                            add_consonant_group = False

                            # 계속
                            if add_group_continue:
                                add_group_continue = False
                                continue
                            else:
                                break

                        else:
                            break

                    token += value[0]
                    index += 1

                word_index = index

                # word가 종료 됐을때 발음은 아직 남아있다면
                if word_index >= word_len:
                    if phonetic_len - phonetic_index >= 1:
                        type = phonetic_type_list[phonetic_index][1]

                        # 남아 있는 발음의 시작이 자음이라면
                        # 뒤에서부터 자음을 만나기 전까지 그룹을 merge 한다
                        if type == 'C' and len(result) > 0:
                            group[1] = token

                            for value in phonetic_type_list[phonetic_index:phonetic_len]:
                                group[0].append(value[0])

                            for c in group[1]:
                                if c in CMUToKorean.alphabet_consonant_set:
                                    result.append(group)
                                    return result

                            count = len(result)
                            for merge_group in reversed(result):

                                if not merge_group[1]:
                                    merge_group[0] += group[0]
                                    merge_group[1] = '' + group[1]
                                    result = result[0:count]
                                    return result

                                for c in merge_group[1]:
                                    if c in CMUToKorean.alphabet_consonant_set:
                                        merge_group[0] += group[0]
                                        merge_group[1] += group[1]
                                        result = result[0:count]
                                        return result

                                merge_group[0] += group[0]
                                merge_group[1] += group[1]
                                group = merge_group
                                count -= 1

                            return result

                        # 그외는 정상종료를 유도
                        else:
                            for value in phonetic_type_list[phonetic_index:phonetic_len]:
                                group[0].append(value[0])

                            phonetic_index = phonetic_len

            if token == '':
                token = None

            # middle.comment
            # 토큰이 존재하지 않았는데 word가 아직 남았다면
            # 앞 그룹에서 가져온다
            if not token:
                if word_index != 0 and word_index < word_len:
                    group_index = len(result) - 1
                    prev_token = result[group_index][1]

                    if len(prev_token) > 1:
                        token = prev_token[-1:]
                        result[group_index][1] = prev_token[:-1]

            # middle.comment
            # 여전이 토큰이 존재하지 않는다면
            # word의 VC가 모두 존재할때 까지 뒤에서부터 그룹을 머지
            if not token:
                group[1] = ''
                count = len(result)

                for merge_group in reversed(result):
                    merge_group[0] += group[0]
                    merge_group[1] += group[1]
                    group = merge_group

                    exists_vowel = False
                    exists_consonant = False

                    for w in merge_group[1]:
                        if w in CMUToKorean.alphabet_vowel_set:
                            exists_vowel = True
                        elif w in CMUToKorean.alphabet_consonant_set:
                            exists_consonant = True
                        else:
                            # 특수문자
                            # 자음으로 취급
                            exists_consonant = True

                    if exists_vowel and exists_consonant:
                        break

                    count -= 1

                count = 1 if count <= 0 else count
                result = result[0:count]

            else:
                group[1] = token
                result.append(group)

        return result

