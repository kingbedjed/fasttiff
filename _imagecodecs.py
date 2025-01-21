
def _packbits_decode(encoded, out):
    i_encoded = 0
    i_out = 0
    try:
        while i_encoded < len(encoded):
            val = int(encoded[i_encoded]) + 1
            i_encoded += 1
            if val > 129:
                # replicate
                out[i_out : i_out + (258 - val)] = encoded[i_encoded : i_encoded + 1]
                i_encoded += 1
                i_out += 258 - val
            elif val < 129:
                # literal
                out[i_out :i_out + val] = encoded[i_encoded : i_encoded + val]
                i_encoded += val
                i_out += val
    except TypeError:
        pass

decoder_map = {
    32773: _packbits_decode,
}
