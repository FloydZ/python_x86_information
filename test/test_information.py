from python_x86_information.information import information

def test_information():
    """
    test.in some specific versions of `adc``
    """
    r = information("adc")
    assert len(r) == 2
    
    r = information("adc", ["r64", "r64"])
    assert r == []

    r = information("adc", ["r64", "rax"])
    assert r == ""

    r = information("adc", "rax, r64")
    assert r == ""

    r = information("adc", "rax,r64")
    assert r == ""

    r = information("adc", "rax, rbx")
    assert r == ""
