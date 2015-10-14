from cffi import FFI

ffi = FFI()
with open("page_rank.h") as h, open("page_rank.c") as c:
    h = h.read()
    c = c.read()
    ffi.cdef(h)
    ffi.cdef("int strcmp(char*, char*);")
    ffi.set_source("_page_rank", h + '\n' + c)

if __name__ == "__main__":
    ffi.compile()
