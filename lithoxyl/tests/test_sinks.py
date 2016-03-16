# -*- coding: utf-8 -*-

from lithoxyl.sensible import (SensibleSink,
                               SensibleFormatter as SF,
                               SensibleEventFormatter as SEF)
from lithoxyl.emitters import StreamEmitter, AggregateEmitter
from lithoxyl.filters import ThresholdFilter
from lithoxyl.logger import Logger


fmtr = SEF('{status_char}{begin_timestamp}')
strm_emtr = StreamEmitter('stderr')
aggr_emtr = AggregateEmitter()
strm_sink = SensibleSink(formatter=fmtr, emitter=strm_emtr)
fake_sink = SensibleSink(formatter=fmtr, emitter=aggr_emtr)


def test_sensible_basic():
    log = Logger('test_ss', [strm_sink, fake_sink])

    print

    log.debug('greet').success('hey')
    assert aggr_emtr.entries[-1][1][0] == 's'

    with log.debug('greet') as t:
        t.success('hello')
        t.warn("everything ok?")

    assert aggr_emtr.entries[-1][1][0] == 'S'

    with log.debug('greet') as t:
        t.failure('bye')
    assert aggr_emtr.entries[-1][1][0] == 'F'

    try:
        with log.debug('greet') as t:
            raise ZeroDivisionError('narwhalbaconderp')
    except Exception:
        pass

    assert aggr_emtr.entries[-1][1][0] == 'E'


def test_bad_encoding():
    try:
        StreamEmitter('stderr', encoding='nope')
    except LookupError:
        assert True
    else:
        assert False


def test_bad_encoding_error_fallback():
    try:
        StreamEmitter('stderr', errors='badvalue')
    except LookupError:
        assert True
    else:
        assert False


def _test_exception():
    _tmpl = ('{iso_end} - {exc_type}: {exc_message}'
             ' - {func_name}:{line_number} - {exc_tb_list}')
    sink = SensibleSink(SF(_tmpl),
                        StreamEmitter('stderr'),
                        filters=[ThresholdFilter(exception=0)])
    logger = Logger('excelsilog', [sink])
    with logger.info('A for Effort', reraise=False) as tr:
        print tr
        raise ValueError('E for Exception')
    return
