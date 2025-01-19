from reader import imread as reader_imread
from tifffile import imread as tifffile_imread
from time import perf_counter
from reader import read_image_file_header, read_tags, read_image_data

filename = 'simple_sample_cells.tif'

with open(filename, 'rb') as fh:
    start = perf_counter()
    byteorder_sym, first_ifd_offset = read_image_file_header(fh)
    print(f'read_image_file_header time taken: {(perf_counter()-start)*1000:.2f}ms')
    start = perf_counter()
    tags = read_tags(fh, first_ifd_offset, byteorder_sym)
    print(f'read_tags time taken: {(perf_counter() - start) * 1000:.2f}ms')
    start = perf_counter()
    data = read_image_data(
        fh,
        strip_offsets=[tags['StripOffsets']['data_offset']],
        strip_byte_counts=[tags['StripByteCounts']['data_offset']],
        image_length=tags['ImageLength']['data_offset'],
        image_width=tags['ImageWidth']['data_offset']
    )
    print(f'read_image_data time taken: {(perf_counter() - start) * 1000:.2f}ms')

# Start the timer
start = perf_counter()
im = tifffile_imread(filename)
print(im.shape)
# Stop the timer
end = perf_counter()
# Print the time taken
print(f'Tifffile time taken: {(end-start)*1000:.2f}ms')


# Start the timer
start = perf_counter()
im = reader_imread(filename)
print(im.shape)
# Stop the timer
end = perf_counter()
# Print the time taken
print(f'Reader time taken: {(end-start)*1000:.2f}ms')