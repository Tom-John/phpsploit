import re, random, termcolor

class Interval(tuple):
    """Random interval from float range. (extends tuple)

    Takes two ints ot floats separated by dash or other chars [^0-9.].
    the master stored value is a tuple of the two floats, and calling
    it returns a random float in the given range.

    Example:
    >>> Interval("1,5 < 5")
    (1.5, 5.0)
    >>> Interval("1,5 < 5")()
    4.2
    >>> print(Interval("1,5 < 5.0"))
    1.5 <= x <= 5 (random interval)

    """
    def __new__(cls, interval):
        value = interval
        if type(value) in (int, float, str):
            value = str(value).replace(',','.')
            value = re.split('[^0-9.]', value)

        value = [str(e) for e in value if e]
        if len(value) == 1:
            value = [value[0], value[0]]

        try:
            assert len(value) == 2
            value = tuple(sorted([float(e) for e in value]))
        except:
            raise ValueError('«%s» must be an int/float interval'
                             ' representation' %interval)

        return tuple.__new__(cls, value)


    def __call__(self):
        return random.uniform(self[0], self[1])


    def __str__(self):
        clear = lambda x: str(x).rstrip('0').rstrip('.')
        text = termcolor.format('~{BRIGHT}%s~{NORMAL}')
        if self[0] != self[1]:
            text = ' <= '.join([ clear(self[0]), text%'x', clear(self[1]) ])
            comment = 'random'
        else:
            text = text %clear(self[0])
            comment = 'static'

        return termcolor.format('~{NORMAL,magenta}%s ~{ITALIC,white}'
                                '(%s interval)~{RESET}' %(text, comment))
