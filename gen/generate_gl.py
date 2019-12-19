import os

def main():
    path = os.path.realpath(__file__+"/../../glex.h")
    print(path)
    file = open(path, "w+")
    guard_start(file)
    empty_line(file)

    windows_includes(file)
    empty_line(file)

    glext_defines(file)
    empty_line(file)

    gl_types(file)
    empty_line(file)

    generate_functions(file)
    empty_line(file)

    write_line(file, "bool InitGl();")
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

GL_WIN32_LIST = [
    ("void", "BlendEquation", "GLenum mode"),
    ("void", "ActiveTexture", "GLenum texture")
]
GL_LIST = [
    ("void", "AttachShader", "GLuint program", "GLuint shader"),
    ("void", "BindBuffer", "GLenum target", "GLuint buffer"),
    ("void", "BindFramebuffer", "GLenum target", "GLuint framebuffer"),
    ("void", "BufferData", "GLenum target", "GLsizeiptr size", "const GLvoid *data", "GLenum usage"),
    ("void", "BufferSubData", "GLenum target", "GLintptr offset", "GLsizeiptr size", "const GLvoid * data"),
    ("GLenum", "CheckFramebufferStatus", "GLenum target"),
    ("void", "ClearBufferfv", "GLenum buffer", "GLint drawbuffer", "const GLfloat * value"),
    ("void", "CompileShader", "GLuint shader"),
    ("GLuint", "CreateProgram", "void"),
    ("GLuint", "CreateShader", "GLenum type"),
    ("void", "DeleteBuffers", "GLsizei n", "const GLuint *buffers"),
    ("void", "DeleteFramebuffers", "GLsizei n", "const GLuint *framebuffers"),
    ("void", "EnableVertexAttribArray", "GLuint index"),
    ("void", "DrawBuffers", "GLsizei n", "const GLenum *bufs"),
    ("void", "FramebufferTexture2D", "GLenum target", "GLenum attachment", "GLenum textarget", "GLuint texture", "GLint level"),
    ("void", "GenBuffers", "GLsizei n", "GLuint *buffers"),
    ("void", "GenFramebuffers", "GLsizei n", "GLuint * framebuffers"),
    ("GLint", "GetAttribLocation", "GLuint program", "const GLchar *name"),
    ("void", "GetShaderInfoLog", "GLuint shader", "GLsizei bufSize", "GLsizei *length", "GLchar *infoLog"),
    ("void", "GetShaderiv", "GLuint shader", "GLenum pname", "GLint *params"),
    ("GLint", "GetUniformLocation", "GLuint program", "const GLchar *name"),
    ("void", "LinkProgram", "GLuint program"),
    ("void", "ShaderSource", "GLuint shader", "GLsizei count", "const GLchar* const *string", "const GLint *length"),
    ("void", "Uniform1i", "GLint location", "GLint v0"),
    ("void", "Uniform1f", "GLint location", "GLfloat v0"),
    ("void", "Uniform2f", "GLint location", "GLfloat v0", "GLfloat v1"),
    ("void", "Uniform4f", "GLint location", "GLfloat v0", "GLfloat v1", "GLfloat v2", "GLfloat v3"),
    ("void", "UniformMatrix4fv", "GLint location", "GLsizei count", "GLboolean transpose", "const GLfloat *value"),
    ("void", "UseProgram", "GLuint program"),
    ("void", "VertexAttribPointer", "GLuint index", "GLint size", "GLenum type", "GLboolean normalized", "GLsizei stride", "const GLvoid * pointer"),
]

def generate_functions(file):
    # determine lengths for nice formating
    retLen    = determine_longest_word(GL_LIST, lambda pair : pair[0])
    nameLen   = determine_longest_word(GL_LIST, lambda pair : pair[1])
    paramsLen = determine_longest_word(GL_LIST, lambda pair : concat_parameters(pair))
    for glFunc in GL_WIN32_LIST:
        write_line(file, format_gl_function(glFunc, retLen, nameLen, paramsLen))
    for glFunc in GL_LIST:
        write_line(file, format_gl_function(glFunc, retLen, nameLen, paramsLen))

def format_gl_function(pair, retLen, nameLen, paramsLen):
    # assemble type definition
    ret        = pad(pair[0], retLen)
    func       = pad(pair[1]+"proc("+concat_parameters(pair)+");", nameLen+paramsLen+4)
    typedef    = "typedef " + ret + " GLDECL " + func
    # assemble function declaration
    returnType = pad(pair[1]+"proc*", nameLen+5)
    name       = "gl"+pair[1]
    definition = "extern " + returnType + " " + name + ";" 
    return typedef + definition

def concat_parameters(pair):
    params = ""
    if len(pair) > 2:
        params += pair[2]
    for param in pair[3:]:
        params += ", " + param
    return params

def determine_longest_word(glList, accessor):
    maxLength = 0
    for element in glList:
        word = accessor(element)
        maxLength = max(maxLength, len(word))
    return maxLength

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