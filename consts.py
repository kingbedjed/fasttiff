tag_id_map = {
    305: 'Software',
    274: 'Orientation',
    270: 'ImageDescription',
    254: 'NewSubfileType',
    256: 'ImageWidth',
    257: 'ImageLength',
    258: 'BitsPerSample',
    259: 'Compression',
    262: 'PhotometricInterpretation',
    273: 'StripOffsets',
    277: 'SamplesPerPixel',
    278: 'RowsPerStrip',
    279: 'StripByteCounts',
    282: 'XResolution',
    283: 'YResolution',
    284: 'PlanarConfiguration',
    296: 'ResolutionUnit',
    322: 'TileWidth',
    323: 'TileLength',
    324: 'TileOffsets',
    325: 'TileByteCounts',
    338: 'ExtraSamples',
    339: 'SampleFormat',
    530: 'YCbCrSubSampling',
    531: 'YCbCrPositioning',
    33421: 'CZ_LSMINFO',
    33432: 'CZ_LSMINFO2',
    33445: 'CZ_LSMINFO3',
    33446: 'CZ_LSMINFO4',
}

data_type_map = {
    1: 'BYTE',
    2: 'ASCII',
    3: 'SHORT',
    4: 'LONG',
    5: 'RATIONAL',
    6: 'SBYTE',
    7: 'UNDEFINED',
    8: 'SSHORT',
    9: 'SLONG',
    10: 'SRATIONAL',
    11: 'SINGLE',
    12: 'DOUBLE',
}

data_type_byte_count_map = {
    1: 1,  # BYTE
    2: 1,  # ASCII
    3: 2,  # SHORT
    4: 4,  # LONG
    5: 8,  # RATIONAL
    6: 1,  # SBYTE
    7: 1,  # UNDEFINED
    8: 2,  # SSHORT
    9: 4,  # SLONG
    10: 8,  # SRATIONAL
    11: 4,  # SINGLE
    12: 8,  # DOUBLE
}

compression_map = {
    1: 'No compression',
    5: 'LZW',
    6: 'Old-style JPEG',
    7: 'JPEG',
    8: 'Deflate',
    32773: 'PackBits',
}



