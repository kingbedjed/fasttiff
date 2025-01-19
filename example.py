from time import perf_counter
from tifffile import TiffFile, imwrite, imread

# im = imread('sample_cells.tif')
# print(im.shape)
# imwrite('simple_sample_cells.tif', im)

# # Start the timer
# start = perf_counter()
# # read the full tiff file
# with open('sample_cells.tif', 'rb') as f:
#     data = f.read()
# # print the size of the file
# print(f'File size: {len(data)/1024/1024:.2f} MB')
# # Stop the timer
# end = perf_counter()
# # Print the time taken
# print(f'Time taken: {(end-start)*1000:.2f}ms')
#
# # Start the timer
# start = perf_counter()
# # read the full tiff file
# tif = TiffFile('sample_cells.tif')
# # print the size of the file
# print(f'File size: {tif.filehandle.size/1024/1024:.2f} MB')
# # Stop the timer
# end = perf_counter()
# # Print the time taken
# print(f'Time taken: {(end-start)*1000:.2f}ms')
#
# # Start the timer
# start = perf_counter()
# # open the tiff file
# fh = open('sample_cells.tif', 'rb')
# # Stop the timer
# end = perf_counter()
# # Print the time taken
# print(f'Time taken: {(end-start)*1000:.2f}ms')


fh = open('simple_sample_cells.tif', 'rb')
file_size = fh.seek(0, 2)
image_data_size = 640*480
non_image_size = file_size - image_data_size
import struct
# the first 8 bytes of every tiff file is the image file header
# https://www.fileformat.info/format/tiff/egff.htm#:~:text=TIFF%20has%20a,file%20may%20contain.
fh.seek(0)
image_file_header_IFH = fh.read(8)
print(len(image_file_header_IFH))
# print header as hex should be '49492a00' or '4d4d002a'
print(image_file_header_IFH[:4].hex())
print(image_file_header_IFH[4:].hex())

byteorder_sym = {b'II': '<', b'MM': '>', b'EP': '<'}[image_file_header_IFH[:2]]
version = struct.unpack(byteorder_sym + 'H', image_file_header_IFH[2:4])[0]
# 42 is Classic TIFF

if byteorder_sym == '<':
    byteorder = 'little'
else:
    byteorder = 'big'

# The first offset value is found in the last four bytes of
# the header and indicates the position of the first IFD (image file directory
first_IFD_offset = struct.unpack(byteorder_sym + 'I', image_file_header_IFH[-4:])[0]
# first_IFD_offset = int.from_bytes(image_file_header_IFH[-4:], byteorder)
print(first_IFD_offset/1024/1024)

fh.seek(first_IFD_offset)
len_tag_entry_count = 2
num_dir_entries_bytes = fh.read(len_tag_entry_count)
num_dir_entries = struct.unpack(byteorder_sym + 'H', num_dir_entries_bytes)[0]
# num_dir_entries = int.from_bytes(num_dir_entries_bytes, byteorder)
length_of_tags = num_dir_entries * 12
fh.seek(first_IFD_offset + len_tag_entry_count + length_of_tags)
next_IFD_offset = fh.read(4)



first_IFD_offset + 12 + num_dir_entries * 12
non_image_size
file_size

first_tag_offset = first_IFD_offset + 2
fh.seek(first_tag_offset)
tag = fh.read(12)
tag_id_map = {305: 'Software', 274: 'Orientation', 270: 'ImageDescription', 254: 'NewSubfileType', 256: 'ImageWidth', 257: 'ImageLength', 258: 'BitsPerSample', 259: 'Compression', 262: 'PhotometricInterpretation', 273: 'StripOffsets', 277: 'SamplesPerPixel', 278: 'RowsPerStrip', 279: 'StripByteCounts', 282: 'XResolution', 283: 'YResolution', 284: 'PlanarConfiguration', 296: 'ResolutionUnit', 322: 'TileWidth', 323: 'TileLength', 324: 'TileOffsets', 325: 'TileByteCounts', 338: 'ExtraSamples', 339: 'SampleFormat', 530: 'YCbCrSubSampling', 531: 'YCbCrPositioning', 33421: 'CZ_LSMINFO', 33432: 'CZ_LSMINFO2', 33445: 'CZ_LSMINFO3', 33446: 'CZ_LSMINFO4'}
tag_id = struct.unpack(byteorder_sym + 'H', tag[:2])[0]
tag_id_name = tag_id_map[tag_id]
data_type_map = {1: 'BYTE', 2: 'ASCII', 3: 'SHORT', 4: 'LONG', 5: 'RATIONAL', 6: 'SBYTE', 7: 'UNDEFINED', 8: 'SSHORT', 9: 'SLONG', 10: 'SRATIONAL', 11: 'SINGLE', 12: 'DOUBLE'}
data_type = data_type_map[struct.unpack(byteorder_sym + 'H', tag[2:4])[0]]
data_count = struct.unpack(byteorder_sym + 'I', tag[4:8])[0]
data_offset = struct.unpack(byteorder_sym + 'I', tag[8:])[0]
data_type_byte_count_map = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 1, 8: 2, 9: 4, 10: 8, 11: 4, 12: 8}

def parse_tag(byteorder_sym, tag, tag_id_map, data_type_map, data_type_byte_count_map):
    tag_id = struct.unpack(byteorder_sym + 'H', tag[:2])[0]
    tag_id_name = tag_id_map[tag_id]
    data_type = struct.unpack(byteorder_sym + 'H', tag[2:4])[0]
    data_type_str = data_type_map[data_type]
    data_count = struct.unpack(byteorder_sym + 'I', tag[4:8])[0]
    data_offset = struct.unpack(byteorder_sym + 'I', tag[8:])[0]
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

tags = {}
for i in range(num_dir_entries):
    tag_offset = first_IFD_offset + 2 + i * 12
    fh.seek(tag_offset)
    tag = fh.read(12)
    t = parse_tag(byteorder_sym, tag, tag_id_map, data_type_map, data_type_byte_count_map)
    tags[t['tag_id_name']] = t

from pprint import pprint
pprint(tags)

# fh.seek(tags['StripOffsets']['data_offset'])
# strip_offsets = fh.read(tags['StripOffsets']['data_count'] * tags['StripOffsets']['data_type_byte_count'])
# strip_offsets = struct.unpack(byteorder_sym + 'I'*tags['StripOffsets']['data_count'], strip_offsets)
# print(strip_offsets)
strip_offsets = [tags['StripOffsets']['data_offset']]

# fh.seek(tags['StripByteCounts']['data_offset'])
# strip_byte_counts = fh.read(tags['StripByteCounts']['data_count'] * tags['StripByteCounts']['data_type_byte_count'])
# strip_byte_counts = struct.unpack(byteorder_sym + 'I'*tags['StripByteCounts']['data_count'], strip_byte_counts)
# print(strip_byte_counts)
strip_byte_counts = [tags['StripByteCounts']['data_offset']]

# compression is short enough to be stored in the tag
compression = tags['Compression']['data_offset']
# http://fileformats.archiveteam.org/wiki/TIFF#Compression:~:text=Format%20details-,Compression,-Tag%20259%20indicates
compression_map = {1: 'No compression', 5: 'LZW', 6: 'Old-style JPEG', 7: 'JPEG', 8: 'Deflate', 32773: 'PackBits'}
compression = compression_map[compression]
print(compression)

# rows per strip is short enough to be stored in the tag
rows_per_strip = tags['RowsPerStrip']['data_offset']
print(rows_per_strip)

# image length is short enough to be stored in the tag
image_length = tags['ImageLength']['data_offset']
print(image_length)

# image width is short enough to be stored in the tag
image_width = tags['ImageWidth']['data_offset']
print(image_width)


strips_in_image = int((image_length * (rows_per_strip - 1)) / rows_per_strip)
print(strips_in_image)

print(f'''
image_length: {image_length}
image_width: {image_width}
rows_per_strip: {rows_per_strip}
strips_in_image: {strips_in_image}
strip_offsets: {len(strip_offsets)}{strip_offsets}
strip_byte_counts: {len(strip_byte_counts)}{strip_byte_counts}
''')

image_data = []
for i in range(len(strip_offsets)):
    fh.seek(strip_offsets[i])
    image_data += fh.read(strip_byte_counts[i])
    # image_data += fh.read(image_width * rows_per_strip)
print(len(image_data))

image_data_size

import numpy as np
# data_array = np.frombuffer(image_data[:image_data_size], dtype=np.uint8)
data_array = np.asarray(image_data[:image_data_size], dtype=np.uint8)
data_array = data_array.reshape((480, 640))
# import matplotlib.pyplot as plt
# plt.imshow(data_array, cmap='gray')
# plt.show()
from tifffile import imwrite
data_array[:10, :5] = 255
imwrite('/home/jed/sample_cells_from_file.tif', data_array)
