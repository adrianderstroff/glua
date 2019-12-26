import os

OUT_DIR = __file__ + "/../"

def main():
    write_header()
    write_source()
    write_lua_header()
    write_lua_source()

################################################################################
# write files
################################################################################

def write_header():
    path = os.path.realpath(OUT_DIR + "glex.h")
    print(path)
    file = open(path, "w+")

    guard_start(file, "GLUA_GLEX_H")
    empty_line(file)

    windows_includes(file)
    empty_line(file)

    glext_defines(file)
    empty_line(file)

    gl_includes(file)
    empty_line(file)

    gl_types(file)
    empty_line(file)

    generate_functions(file)
    empty_line(file)

    write_line(file, "bool InitGl();")
    empty_line(file)

    guard_end(file, "GLUA_GLEX_H")
    file.close()

def write_source():
    path = os.path.realpath(OUT_DIR + "glex.c")
    print(path)
    file = open(path, "w+")

    write_line(file, '#include "glex.h"')
    empty_line(file)
    write_line(file, '#include <stdio.h>')
    empty_line(file)

    generate_implementations(file)
    empty_line(file)

    write_init_gl_implementation(file)
    empty_line(file)

    file.close()

def write_lua_header():
    path = os.path.realpath(OUT_DIR + "glutil.h")
    print(path)
    file = open(path, "w+")

    guard_start(file, "GLUTIL_H")
    empty_line(file)

    write_line(file, '#include "glex.h"')
    write_line(file, '#include "lua.h"')
    write_line(file, '#include "lualib.h"')
    write_line(file, '#include "lauxlib.h"')
    empty_line(file)

    # write file definitions
    write_lua_definition(file)
    empty_line(file)

    # write lua c mapping
    write_lua_c_mapping(file)
    empty_line(file)

    # write lua c constants
    write_lua_c_constants(file)
    empty_line(file)

    guard_end(file, "GLUTIL_H")
    
    file.close()

def write_lua_source():
    path = os.path.realpath(OUT_DIR + "glutil.c")
    print(path)
    file = open(path, "w+")

    write_line(file, '#include "glutil.h"')
    empty_line(file)

    write_lua_implementation(file)

    file.close()

################################################################################
# lists
################################################################################

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
    ("void", "VertexAttribPointer", "GLuint index", "GLint size", "GLenum type", "GLboolean normalized", "GLsizei stride", "const GLvoid * pointer")
]

################################################################################
# helper functions
################################################################################

def windows_includes(file):
    write_line(file, "#include <windows.h>")
    write_line(file, "#include <stdbool.h>")
    write_line(file, "#define GLDECL WINAPI")

def gl_includes(file):
    write_line(file, "#include <GL/gl.h>")
    write_line(file, "#include <GL/glcorearb.h>")

def glext_defines(file):
    write_line(file, "// https://www.opengl.org/registry/api/GL/glext.h")                
    for pair in GLEXT_DEFINES_LIST:
        write_line(file, "#define " + pad(pair[0],32) + " " + pair[1])

def gl_types(file):
    write_line(file, "typedef char      GLchar;")
    write_line(file, "typedef ptrdiff_t GLintptr;")
    write_line(file, "typedef ptrdiff_t GLsizeiptr;")

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

def generate_implementations(file):
    # determine lengths for nice formating
    nameLen   = determine_longest_word(GL_LIST, lambda pair : pair[1])
    for glFunc in GL_WIN32_LIST:
        write_line(file, format_gl_implementation(glFunc, nameLen))
    for glFunc in GL_LIST:
        write_line(file, format_gl_implementation(glFunc, nameLen))

def format_gl_implementation(pair, nameLen):
    name = pair[1]
    funcType = pad(name+"proc", nameLen+4)
    return f"{funcType} *gl{name};"

def write_init_gl_implementation(file):
    write_line(file,
    '''bool InitGl() {
    // get the function pointer of wglGetProcAddress
    HINSTANCE dll = LoadLibraryA("opengl32.dll");
    typedef PROC WINAPI wglGetProcAddressproc(LPCSTR lpszProc);
    if (!dll) {
        printf("opengl32.dll not found.\\n");
        return false;
    }
    wglGetProcAddressproc* wglGetProcAddress =
    (wglGetProcAddressproc*)GetProcAddress(dll, "wglGetProcAddress");''')

    for pair in GL_WIN32_LIST:
        write_line(file, load_gl_function(pair))
    for pair in GL_LIST:
        write_line(file, load_gl_function(pair))

    empty_line(file)
    write_line(file, "    return true;")
    write_line(file, "}")

def load_gl_function(pair):
    name = pair[1]
    nl = "\\n"
    return f'''
    gl{name} = ({name}proc *)wglGetProcAddress("gl{name}");
    if (!gl{name}) {{
        printf("Function gl{name} couldn't be loaded from opengl32.dll{nl}");
        return false;
    }}'''

def write_lua_definition(file):
    for pair in GL_WIN32_LIST:
        write_line(file, generate_lua_definition(pair))
    for pair in GL_LIST:
        write_line(file, generate_lua_definition(pair))

def generate_lua_definition(pair):
    name  = "Gl"+pair[1]
    return f"int {name}(lua_State *L);"

def write_lua_c_mapping(file):
    write_line(file, '#define LUA_C_MAPPING \\')
    for pair in GL_WIN32_LIST:
        write_line(file, generate_lua_c_mapping(pair))
    for pair in GL_LIST:
        write_line(file, generate_lua_c_mapping(pair))
    write_line(file, '    /* end */')

def generate_lua_c_mapping(pair):
    name = pair[1]
    # format lua function
    luaName = name[0].lower()
    for c in name[1:]:
        luaName += c.lower() if c.islower() else "_" + c.lower()
    return f'    {{"{luaName}", gl{name}}}, \\'

def write_lua_c_constants(file):
    write_line(file, '#define LUA_C_CONSTANTS \\')
    for pair in GLEXT_DEFINES_LIST:
        write_line(file, generate_lua_c_constant(pair))
    write_line(file, '    /* end */')

def generate_lua_c_constant(pair):
    name = pair[0]
    return f'''    lua_pushnumber(L, {name});\\
    lua_setfield(L, -2, "{name[3:]}");\\'''

def write_lua_implementation(file):
    for pair in GL_WIN32_LIST:
        write_line(file, generate_lua_implementation(pair))
    for pair in GL_LIST:
        write_line(file, generate_lua_implementation(pair))

def generate_lua_implementation(pair):
    name  = "Gl"+pair[1]
    numOfParams = max(len(pair) - 2, 0)
    if numOfParams == 1 and determine_return_type(pair[2])[2] == 0:
        numOfParams = 0
    nl = "\n"
    # grab all parameter names
    paramNames = []
    for i in range(numOfParams):
        tokens = pair[i+2].split()
        paramName = tokens[len(tokens)-1]
        paramNames.append(paramName)
    # find length of longest parameter name
    paramNameLen = determine_longest_word(paramNames, lambda x : x)
    # grab all parameter types
    paramTypes = []
    for i in range(numOfParams):
        paramTypes.append(determine_return_type(pair[i+2]))
    # find length of longest parameter type name
    paramTypeLen = determine_longest_word(paramTypes, lambda x : x[0])
    # retrieve all parameters from lua
    getParams = ""
    for i in range(numOfParams):
        paramName = pad(paramNames[i], paramNameLen)
        paramType = pad(paramTypes[i][0], paramTypeLen)
        luaCheckType = paramTypes[i][1]
        udataParam = ', "' + paramTypes[i][0] + '"' if "udata" in luaCheckType else ""
        getParams += f"    {paramType} {paramName} = ({paramType})luaL_check{luaCheckType}(L, {i+1}{udataParam});{nl}"
    # assemble all parameters for functions call
    callParams = ""
    for i in range(numOfParams):
        paramName = paramNames[i]
        if (i == 0): callParams += paramName
        else: callParams += f", {paramName}"
    return f'''int {name}(lua_State *L) {{
{getParams}
    gl{pair[1]}({callParams});
    return 0;
}}
'''

################################################################################
# shared functions
################################################################################

GL_TYPES = [
    ["GLenum","integer",1],
    ["GLchar *","string",1],
    ["GLchar","integer",1],
    ["GLboolean","integer",1],
    ["GLintptr","integer",1],
    ["GLint *","udata",1],
    ["GLint","integer",1],
    ["GLuint *","udata",1],
    ["GLuint","integer",1],
    ["GLfloat *","udata",1],
    ["GLfloat","number",1],
    ["GLsizeiptr","integer",1],
    ["GLsizei *","udata",1],
    ["GLsizei","integer",1],
    ["GLvoid *","udata",1],
    ["GLvoid","",1],
    ["void", "", 0]
]

def determine_return_type(param):
    for glType in GL_TYPES:
        if glType[0] in param:
            return glType
    return ""

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

def guard_start(file, name):
    write_line(file, f"#ifndef {name}")
    write_line(file, f"#define {name}")

def guard_end(file, name):
    file.write(f"#endif//{name}")

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

################################################################################
# main entrypoint
################################################################################

if __name__ == "__main__":
    main()