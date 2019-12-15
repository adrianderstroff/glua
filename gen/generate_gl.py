def main():
    file = open("glex.h", "w+")
    guard_start(file)
    empty_line(file)

    windows_includes(file)
    empty_line(file)

    glext_defines(file)
    empty_line(file)

    gl_types(file)
    empty_line(file)

    empty_line(file)
    guard_end(file)
    file.close()

def windows_includes(file):
    write_line(file, "#include <windows.h>")
    write_line(file, "#include <stdbool.h>")
    write_line(file, "#define GLDECL WINAPI")

GLEXT_DEFINES_LIST = [
    ("GL_ARRAY_BUFFER", "0x8892"),
    ("GL_ARRAY_BUFFER_BINDING", "0x8894"),
    ("GL_COLOR_ATTACHMENT0", "0x8CE0"),
    ("GL_COMPILE_STATUS", "0x8B81"),
    ("GL_CURRENT_PROGRAM", "0x8B8D"),
    ("GL_DYNAMIC_DRAW", "0x88E8"),
    ("GL_ELEMENT_ARRAY_BUFFER", "0x8893"),
    ("GL_ELEMENT_ARRAY_BUFFER_BINDING", "0x8895"),
    ("GL_FRAGMENT_SHADER", "0x8B30"),
    ("GL_FRAMEBUFFER", "0x8D40"),
    ("GL_FRAMEBUFFER_COMPLETE", "0x8CD5"),
    ("GL_FUNC_ADD", "0x8006"),
    ("GL_INVALID_FRAMEBUFFER_OPERATION", "0x0506"),
    ("GL_MAJOR_VERSION", "0x821B"),
    ("GL_MINOR_VERSION", "0x821C"),
    ("GL_STATIC_DRAW", "0x88E4"),
    ("GL_STREAM_DRAW", "0x88E0"),
    ("GL_TEXTURE0", "0x84C0"),
    ("GL_VERTEX_SHADER", "0x8B31")
]

def glext_defines(file):
    write_line(file, "// https://www.opengl.org/registry/api/GL/glext.h")                
    for pair in GLEXT_DEFINES_LIST:
        write_line(file, "#define " + pad(pair[0],32) + " " + pair[1])

def gl_types(file):
    write_line(file, "typedef char      GLchar;")
    write_line(file, "typedef ptrdiff_t GLintptr;")
    write_line(file, "typedef ptrdiff_t GLsizeiptr;")

def guard_start(file):
    write_line(file, "#ifndef GLUA_GLEX_H")
    write_line(file, "#define GLUA_GLEX_H")

def guard_end(file):
    file.write("#endif//GLUA_GLEX_H")

def write_line(file, text):
    file.write(text + "\n")

def empty_line(file):
    file.write("\n")

def pad(word, size):
    delta = size - len(word)
    if delta > 0:
        return word + (" " * delta)
    else:
        return word

if __name__ == "__main__":
    main()