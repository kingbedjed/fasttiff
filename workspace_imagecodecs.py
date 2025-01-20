from reader import read_image_file_header, read_tags
from _imagecodecs import _packbits_decode
from consts import compression_map
import struct
from tifffile import imwrite, imread
from time import perf_counter
import numpy as np

filename = 'sample_cells.tif'

start = perf_counter()
im = imread(filename)
end = perf_counter()
print(f'Tifffile time taken: {(end-start)*1000:.2f}ms')

fh = open(filename, 'rb')

byteorder_sym, first_ifd_offset = read_image_file_header(fh)
tags = read_tags(fh, first_ifd_offset, byteorder_sym)

fh.seek(tags['StripOffsets']['data_offset'])
strip_offsets = fh.read(tags['StripOffsets']['data_count'] * tags['StripOffsets']['data_type_byte_count'])
strip_offsets = struct.unpack(byteorder_sym + 'I'*tags['StripOffsets']['data_count'], strip_offsets)

fh.seek(tags['StripByteCounts']['data_offset'])
strip_byte_counts = fh.read(tags['StripByteCounts']['data_count'] * tags['StripByteCounts']['data_type_byte_count'])
strip_byte_counts = struct.unpack(byteorder_sym + 'I'*tags['StripByteCounts']['data_count'], strip_byte_counts)

image_length = tags['ImageLength']['data_offset']
image_width = tags['ImageWidth']['data_offset']
rows_per_strip = tags['RowsPerStrip']['data_offset']

compression_map[tags['Compression']['data_offset']]

t_start = perf_counter()
image_data = np.empty(np.prod((image_length, image_width)), dtype=np.uint8)
buffer_data = np.empty(np.sum(strip_byte_counts), dtype=np.uint8)
start = 0
end = 0
bytes_per_strip = rows_per_strip * image_width
for i in range(len(strip_offsets)):
    fh.seek(strip_offsets[i])
    end += strip_byte_counts[i]
    # _packbits_decode(fh.read(strip_byte_counts[i]), buffer_data[start:end])
    buffer_data[start:end] = np.fromfile(fh, count=strip_byte_counts[i], offset=0, dtype=np.uint8)
    start = end
_packbits_decode(buffer_data, image_data)
# image_data = np.frombuffer(
#         buffer_data,
#         dtype=np.uint8
#     )
len(image_data) / (image_length * image_width)
# im = np.asarray(image_data, dtype=np.uint8)
image_data.shape = (image_length, image_width)
t_end = perf_counter()
print(f'My time taken: {(t_end-t_start)*1000:.2f}ms')




imwrite('/home/jed/sample_cells_from_file.tif', image_data)
