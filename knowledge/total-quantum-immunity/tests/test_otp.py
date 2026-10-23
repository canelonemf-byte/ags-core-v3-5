import pytest
import otp


def test_roundtrip_and_short_key():
    m = "mensaje secreto".encode(); k = otp.keygen(len(m))
    assert otp.decrypt(otp.encrypt(m, k), k) == m
    with pytest.raises(ValueError):
        otp.encrypt(m, k[:3])
