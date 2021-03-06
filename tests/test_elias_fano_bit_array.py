from datetime import timedelta
from typing import List

from bitarray import bitarray
from hypothesis import assume, example, given, settings
from hypothesis import strategies as st

from succinct.elias_fano_bit_array import EliasFanoBitArray


@given(st.binary(min_size=8, max_size=10000))
@settings(max_examples=1000, deadline=None)
@example(bb=bytes([42] * 136))
def test_elias_fano_bit_array_bit_array(bb: bytes) -> None:
    assume(len(bb) % 8 == 0)

    bits = bitarray()
    bits.frombytes(bb)
    efba = EliasFanoBitArray(bits)

    for i in range(len(bits)):
        assert efba[i] == bits[i]


@given(st.binary(min_size=8, max_size=10000))
@settings(max_examples=1000)
@example(bb=bytes([42] * 136))
def test_elias_fano_bit_array_rank(bb: bytes) -> None:
    assume(len(bb) % 8 == 0)

    bits = bitarray()
    bits.frombytes(bb)
    efba = EliasFanoBitArray(bits)

    for i in range(len(bits)):
        assert efba.rank(i) == sum(bits[0:(i + 1)])


@given(st.binary(min_size=8, max_size=10000))
@settings(max_examples=1000, deadline=timedelta(milliseconds=500))
@example(bb=bytes([42] * 136))
def test_elias_fano_bit_array_rank_zero(bb: bytes) -> None:
    assume(len(bb) % 8 == 0)

    bits = bitarray()
    bits.frombytes(bb)
    efba = EliasFanoBitArray(bits)

    for i in range(len(bits)):
        assert efba.rank_zero(i) == sum(1 - int(b) for b in bits[0:(i + 1)])


@given(st.binary(min_size=8, max_size=10000))
@settings(max_examples=1000, deadline=timedelta(milliseconds=500))
@example(bb=bytes([42] * 136))
def test_elias_fano_bit_array_select(bb: bytes) -> None:
    assume(len(bb) % 8 == 0)

    bits = bitarray()
    bits.frombytes(bb)
    efba = EliasFanoBitArray(bits)

    select_answers: List[int] = []
    for i in range(len(bits)):
        if bits[i]:
            select_answers.append(i)

    for i, pos in enumerate(select_answers):
        assert efba.select(i) == pos


@given(st.binary(min_size=8, max_size=10000))
@settings(max_examples=1000, deadline=timedelta(milliseconds=2000))
@example(bb=bytes([42] * 136))
def test_elias_fano_bit_array_select_zero(bb: bytes) -> None:
    assume(len(bb) % 8 == 0)

    bits = bitarray()
    bits.frombytes(bb)
    efba = EliasFanoBitArray(bits)

    select_zero_answers: List[int] = []
    for i in range(len(bits)):
        if not bits[i]:
            select_zero_answers.append(i)

    for i, pos in enumerate(select_zero_answers):
        assert efba.select_zero(i) == pos
