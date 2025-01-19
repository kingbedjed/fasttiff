from reader import imread as reader_imread
from tifffile import imread as tifffile_imread
from time import perf_counter
import numpy as np

filename = 'simple_sample_cells.tif'

# time tifffile
start = perf_counter()
tifffile_im = tifffile_imread(filename)
print(tifffile_im.shape)
end = perf_counter()
print(f'Tifffile time taken: {(end-start)*1000:.2f}ms')

# time reader
start = perf_counter()
reader_im = reader_imread(filename)
print(reader_im.shape)
end = perf_counter()
print(f'Reader time taken: {(end-start)*1000:.2f}ms')

np.testing.assert_array_equal(tifffile_im, reader_im)
print('All tests passed.')
