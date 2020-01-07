import os
import re

SCRIPT_DIR = __file__ + "/../"
OUT_DIR = __file__ + "/../../src/"

def main():
    path = os.path.realpath(OUT_DIR + "gl.h")
    print(path)
    file = open(path, "w+")

    retrieve_defines()
    retrieve_functions()

    write_header(file)
    write_source(file)
    write_lua_header(file)
    write_lua_source(file)

    file.close()

################################################################################
# write files
################################################################################

def write_header(file):
    c_file_start(file, "glex.h")
    empty_line(file)

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
    empty_line(file)

def write_source(file):
    c_file_start(file, "glex.c")
    empty_line(file)

    write_line(file, '#include <stdio.h>')
    empty_line(file)

    generate_implementations(file)
    empty_line(file)

    write_init_gl_implementation(file)
    empty_line(file)

def write_lua_header(file):
    c_file_start(file, "glutil.h")
    empty_line(file)

    guard_start(file, "GLUTIL_H")
    empty_line(file)

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
    empty_line(file)

def write_lua_source(file):
    c_file_start(file, "glutil.c")
    empty_line(file)

    write_lua_implementation(file)

################################################################################
# lists
################################################################################

GL_TYPES_LIST = [
    (["GLchar*", "GLchar *"], "string", 1),
    (["*"]                  , "udata" , 1),
    (["GLfloat", "GLdouble"], "number", 1),
    (["void"]               , ""      , 0)
]
GL_DEFINES_LIST   = []
GL_FUNCTIONS_LIST = []
GL_FUNCTIONS_DIFF_LIST = []

################################################################################
# helper functions
################################################################################

def retrieve_defines():
    with open(SCRIPT_DIR + "gl_defines.h", 'r') as fp:
        line = fp.readline()
        while line:
            pair = line.split()
            if len(pair) == 3:
                defineTuple = (pair[1], pair[2]) 
                GL_DEFINES_LIST.append(defineTuple)
            line = fp.readline()

def retrieve_functions():
    with open(SCRIPT_DIR + "gl_functions.h", 'r') as fp:
        line = fp.readline()
        while line:
            line = line.strip()

            # grab everything before the parameters
            retValFnName = re.match("[^(]*", line)
            line = line[retValFnName.end()+1:-2]

            # extract return value and function name
            tokens = retValFnName.group().split()
            fnName = tokens[len(tokens)-1]
            retVal = tokens[0]
            for token in tokens[1:len(tokens)-1]:
                retVal += " " + token
            fnTuple = [retVal, fnName]

            # collect all function arguments
            for fnArg in re.finditer("[^(),]+", line):
                fnTuple.append(fnArg.group().strip())

            # add to list and advance to next line
            GL_FUNCTIONS_LIST.append(fnTuple)
            line = fp.readline()

    with open(SCRIPT_DIR + "gl_functions_diff.h", 'r') as fp:
        line = fp.readline()
        while line:
            line = line.strip()

            # grab everything before the parameters
            retValFnName = re.match("[^(]*", line)
            line = line[retValFnName.end()+1:-2]

            # extract return value and function name
            tokens = retValFnName.group().split()
            fnName = tokens[len(tokens)-1]
            retVal = tokens[0]
            for token in tokens[1:len(tokens)-1]:
                retVal += " " + token
            fnTuple = [retVal, fnName]

            # collect all function arguments
            for fnArg in re.finditer("[^(),]+", line):
                fnTuple.append(fnArg.group().strip())

            # add to list and advance to next line
            GL_FUNCTIONS_DIFF_LIST.append(fnTuple)
            line = fp.readline()

def windows_includes(file):
    write_line(file, "#include <windows.h>")
    write_line(file, "#include <stdbool.h>")
    write_line(file, "#define GLDECL WINAPI")

def gl_includes(file):
    write_line(file, "#include <GL/gl.h>")
    write_line(file, "#include <GL/glcorearb.h>")

def glext_defines(file):
    # get length of longest parameter name
    definesLen = determine_longest_word(GL_DEFINES_LIST, lambda pair : pair[0])

    # write all defines to file
    for pair in GL_DEFINES_LIST:
        write_line(file, "#define " + pad(pair[0], definesLen) + " " + pair[1])

def gl_types(file):
    write_line(file, "typedef char      GLchar;")
    write_line(file, "typedef ptrdiff_t GLintptr;")
    write_line(file, "typedef ptrdiff_t GLsizeiptr;")

def generate_functions(file):
    # determine lengths for nice formating
    retLen    = determine_longest_word(GL_FUNCTIONS_LIST, lambda pair : pair[0])
    nameLen   = determine_longest_word(GL_FUNCTIONS_LIST, lambda pair : pair[1])
    paramsLen = determine_longest_word(GL_FUNCTIONS_LIST, lambda pair : concat_parameters(pair))
    for glFunc in GL_FUNCTIONS_LIST:
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

################################################################################

def generate_implementations(file):
    # determine lengths for nice formating
    nameLen   = determine_longest_word(GL_FUNCTIONS_LIST, lambda pair : pair[1])
    for glFunc in GL_FUNCTIONS_LIST:
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

    for pair in GL_FUNCTIONS_LIST:
        write_line(file, load_gl_function(pair))

    empty_line(file)
    write_line(file, "    return true;")
    write_line(file, "}")

def load_gl_function(pair):
    name = pair[1].strip()
    nl = "\\n"
    return f'''
    gl{name} = ({name}proc *)wglGetProcAddress("gl{name}");
    if (!gl{name}) {{
        printf("Function gl{name} couldn't be loaded from opengl32.dll{nl}");
        return false;
    }}'''

################################################################################

def write_lua_definition(file):
    allFnList = GL_FUNCTIONS_DIFF_LIST + GL_FUNCTIONS_LIST
    for pair in allFnList:
        write_line(file, generate_lua_definition(pair))

def generate_lua_definition(pair):
    name  = "Gl"+pair[1].strip()
    return f"int {name}(lua_State *L);"

def write_lua_c_mapping(file):
    allFnList = GL_FUNCTIONS_DIFF_LIST + GL_FUNCTIONS_LIST

    luaFnNameList = generate_lua_function_names()
    fnLuaLen = determine_longest_word(luaFnNameList, lambda x : x)
    fnCLen   = determine_longest_word(allFnList, lambda p : p[1])
    write_line(file, "#define EXPOSED_GL_FUNCTIONS \\")
    for i in range(len(allFnList)):
        luaFnName = pad(f'"{luaFnNameList[i]}"', fnLuaLen+2)
        cFnName   = pad("Gl"+allFnList[i][1], fnCLen+2)
        write_line(file, f'    {{{luaFnName}, {cFnName}}}, \\')
    write_line(file, '    /* end */')

def generate_lua_function_names():
    allFnList = GL_FUNCTIONS_DIFF_LIST + GL_FUNCTIONS_LIST
    luaFnNameList = []
    for pair in allFnList:
        # grab c function name
        name = pair[1]
        # turn it into lua naming convention
        luaName = name[0].lower()
        for c in name[1:]:
            isLower = c.islower() or c.isdigit()
            luaName += c.lower() if isLower else "_" + c.lower()
        luaFnNameList.append("gl_" + luaName)
    return luaFnNameList

def write_lua_c_constants(file):
    write_line(file, '#define EXPOSED_GL_CONSTANTS \\')
    for pair in GL_DEFINES_LIST:
        write_line(file, generate_lua_c_constant(pair))
    write_line(file, '    /* end */')

def generate_lua_c_constant(pair):
    name = pair[0]
    return f'''    lua_pushnumber(L, {name});\\
    lua_setfield(L, -2, "{name[3:]}");\\'''

################################################################################

def write_lua_implementation(file):
    for pair in GL_FUNCTIONS_LIST:
        write_line(file, generate_lua_implementation(pair))
    for pair in GL_FUNCTIONS_DIFF_LIST:
        write_line(file, generate_lua_implementation(pair))

def generate_lua_implementation(pair):
    name  = "Gl"+pair[1]
    nl = "\n"
    
    # determine number of parameters
    numOfParams = max(len(pair) - 2, 0)
    if numOfParams == 1 and determine_return_type(pair[2])[2] == 0:
        numOfParams = 0

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

def determine_return_type(param):
    returnType = extract_return_type(param)
    for glTypeRank in GL_TYPES_LIST:
        for glType in glTypeRank[0]:
            if glType in returnType:
                return (returnType, glTypeRank[1], glTypeRank[2])
    return (returnType, "integer", 1)

def extract_return_type(param):
    tokens = param.split()
    returnType = tokens[0]
    for i in range(1,len(tokens)-1):
        returnType += " " + tokens[i]
    return returnType

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

def c_file_start(file, fileName):
    headDiff = 120 - 4
    lineDiff = 120 - len(fileName) - 5
    write_line(file, "/*" + (headDiff * "*") + "*/")
    write_line(file, "/*" + (headDiff * " ") + "*/")
    write_line(file, "/* " + fileName + (lineDiff * " ") + "*/")
    write_line(file, "/*" + (headDiff * " ") + "*/")
    write_line(file, "/*" + (headDiff * "*") + "*/")

def guard_start(file, name):
    write_line(file, f"#ifndef {name}")
    write_line(file, f"#define {name}")

def guard_end(file, name):
    write_line(file, f"#endif//{name}")

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