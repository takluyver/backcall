from backcall import callback_prototype

@callback_prototype
def msg_callback(a, b, c, d=None, e=None, f=None):
    pass

def test_all_args():
    @msg_callback
    def thingy1(q, w, s, d, e, f):
        return q, w, s, d, e, f
    
    assert not getattr(thingy1, '__wrapped__', None)
    assert thingy1('A', 'B', 'C', d='D', e='E', f='F') == tuple('ABCDEF')

def test_some_args():
    @msg_callback
    def thingy2(t, *, d=None):
        return t, d
    
    assert getattr(thingy2, '__wrapped__', None)
    assert thingy2('A', 'B', 'C', d='D', e='E', f='F') == ('A', 'D')

def test_no_args():
    @msg_callback
    def thingy3():
        return 'Success'
    
    assert getattr(thingy3, '__wrapped__', None)
    assert thingy3('A', 'B', 'C', d='D', e='E', f='F') == 'Success'
