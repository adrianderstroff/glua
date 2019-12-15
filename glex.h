#ifndef GLUA_GLEX_H
#define GLUA_GLEX_H

#include <windows.h>
#include <stdbool.h>
#define GLDECL WINAPI

// https://www.opengl.org/registry/api/GL/glext.h
#define GL_ARRAY_BUFFER                  0x8892
#define GL_ARRAY_BUFFER_BINDING          0x8894
#define GL_COLOR_ATTACHMENT0             0x8CE0
#define GL_COMPILE_STATUS                0x8B81
#define GL_CURRENT_PROGRAM               0x8B8D
#define GL_DYNAMIC_DRAW                  0x88E8
#define GL_ELEMENT_ARRAY_BUFFER          0x8893
#define GL_ELEMENT_ARRAY_BUFFER_BINDING  0x8895
#define GL_FRAGMENT_SHADER               0x8B30
#define GL_FRAMEBUFFER                   0x8D40
#define GL_FRAMEBUFFER_COMPLETE          0x8CD5
#define GL_FUNC_ADD                      0x8006
#define GL_INVALID_FRAMEBUFFER_OPERATION 0x0506
#define GL_MAJOR_VERSION                 0x821B
#define GL_MINOR_VERSION                 0x821C
#define GL_STATIC_DRAW                   0x88E4
#define GL_STREAM_DRAW                   0x88E0
#define GL_TEXTURE0                      0x84C0
#define GL_VERTEX_SHADER                 0x8B31

typedef char      GLchar;
typedef ptrdiff_t GLintptr;
typedef ptrdiff_t GLsizeiptr;


#endif//GLUA_GLEX_H