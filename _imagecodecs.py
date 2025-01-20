
def _packbits_decode(encoded, out):
    i = 0
    try:
        while True:
            n = ord(encoded[i : i + 1]) + 1
            i += 1
            if n > 129:
                # replicate
                out[i : i + n] = encoded[i : i + 1] * (258 - n)
                i += 1
            elif n < 129:
                # literal
                out[i : i + n] = encoded[i : i + n]
                i += n
    except TypeError:
        pass

decoder_map = {
    32773: _packbits_decode,
}
