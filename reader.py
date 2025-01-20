import struct
from consts import (
    tag_id_map,
    data_type_map,
    data_type_byte_count_map,
)
from _imagecodecs import decoder_map
import numpy as np

def parse_tag_bytes(tag_bytes, byteorder_sym):
    tag_id = struct.unpack(byteorder_sym + 'H', tag_bytes[:2])[0]
    tag_id_name = tag_id_map[tag_id]
    data_type = struct.unpack(byteorder_sym + 'H', tag_bytes[2:4])[0]
    data_type_str = data_type_map[data_type]
    data_count = struct.unpack(byteorder_sym + 'I', tag_bytes[4:8])[0]
    data_offset = struct.unpack(byteorder_sym + 'I', tag_bytes[8:])[0]
    data_type_byte_count = data_type_byte_count_map[data_type]
    tag_map = {
        'tag_id': tag_id,
        'tag_id_name': tag_id_name,
        'data_type': data_type,
        'data_type_str': data_type_str,
        'data_count': data_count,
        'data_offset': data_offset,
        'data_type_byte_count': data_type_byte_count
    }
    return tag_map

def read_tags(fh, IFD_offset, byteorder_sym):
    tag_entry_count_num_bytes = 2
    tag_num_bytes = 12
    fh.seek(IFD_offset)
    num_dir_entries_bytes = fh.read(tag_entry_count_num_bytes)
    num_dir_entries = struct.unpack(byteorder_sym + 'H', num_dir_entries_bytes)[0]
    tags = {}
    for i in range(num_dir_entries):
        tag_offset = IFD_offset + tag_entry_count_num_bytes + i * tag_num_bytes
        fh.seek(tag_offset)
        tag_bytes = fh.read(tag_num_bytes)
        t = parse_tag_bytes(tag_bytes, byteorder_sym)
        tags[t['tag_id_name']] = t
    return tags

def read_image_file_header(fh):
    fh.seek(0)
    tiff_magic_num = fh.read(2)
    if tiff_magic_num != b'\x4d\x4d' and tiff_magic_num != b'\x49\x49':
        raise ValueError(f'Invalid TIFF magic number: {tiff_magic_num}')
    byteorder_sym = {b'II': '<', b'MM': '>', b'EP': '<'}[tiff_magic_num]
    fh.seek(2)
    version = struct.unpack(byteorder_sym + 'H', fh.read(2))[0]
    fh.seek(4)
    first_IFD_offset_bytes = fh.read(4)
    first_IFD_offset = struct.unpack(byteorder_sym + 'I', first_IFD_offset_bytes)[0]
    return byteorder_sym, first_IFD_offset

def read_image_data(fh, strip_offsets, strip_byte_counts,
                    image_length, image_width, decoder_func=None, dtype=np.uint8):
    image_data = np.empty(np.prod((image_length, image_width)), dtype=dtype)
    buffer_data = np.empty(np.sum(strip_byte_counts), dtype=np.uint8)
    start = 0
    end = 0
    for i in range(len(strip_offsets)):
        fh.seek(strip_offsets[i])
        end += strip_byte_counts[i]
        buffer_data[start:end] = np.fromfile(fh, count=strip_byte_counts[i], offset=0, dtype=np.uint8)
        start = end
    if decoder_func is not None:
        decoder_func(buffer_data, image_data)
    else:
        image_data = buffer_data
    image_data.shape = (image_length, image_width)
    return image_data

def imread(filename):
    with open(filename, 'rb') as fh:
        byteorder_sym, first_ifd_offset = read_image_file_header(fh)
        tags = read_tags(fh, first_ifd_offset, byteorder_sym)
        data = read_image_data(
            fh,
            strip_offsets=[tags['StripOffsets']['data_offset']],
            strip_byte_counts=[tags['StripByteCounts']['data_offset']],
            image_length=tags['ImageLength']['data_offset'],
            image_width=tags['ImageWidth']['data_offset'],
            decoder_func=decoder_map.get(tags['Compression']['data_offset'], None),
        )
    return data