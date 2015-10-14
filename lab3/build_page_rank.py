from cffi import FFI

ffi = FFI()
with open("test.h") as h, open("test.c") as c:
    ffi.cdef(h.read())
    ffi.set_source("_page_rank", c.read())

if __name__ == "__main__":
    ffi.compile()
