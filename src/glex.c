#include "glex.h"

#include <stdio.h>

#define GLE(ret, name, ...) name##proc * gl##name;
GLUA_GL_LIST
GLUA_GL_LIST_WIN32
#undef GLE

bool init_gl() {
    // get the function pointer of wglGetProcAddress
    HINSTANCE dll = LoadLibraryA("opengl32.dll");
    typedef PROC WINAPI wglGetProcAddressproc(LPCSTR lpszProc);
    if (!dll) {
        printf("opengl32.dll not found.\n");
        return false;
    }
    wglGetProcAddressproc* wglGetProcAddress =
     (wglGetProcAddressproc*)GetProcAddress(dll, "wglGetProcAddress");

    // try to load all functions from the two defined macros
    #define GLE(ret, name, ...)                                                \
    gl##name = (name##proc *)wglGetProcAddress("gl" #name);                    \
    if (!gl##name) {                                                           \
        printf("Function gl" #name " couldn't be loaded from opengl32.dll\n"); \
        return false;                                                          \
    }
    GLUA_GL_LIST
    GLUA_GL_LIST_WIN32
    #undef GLE

    return true;
}