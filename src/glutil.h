#ifndef GLUA_GLUTIL_H
#define GLUA_GLUTIL_H

#include "glex.h"
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"

int GlClear(lua_State *L);
int GlColor3f(lua_State *L);
int GlVertex3f(lua_State *L);
int GlBegin(lua_State *L);
int GlEnd(lua_State *L);
int GlViewport(lua_State *L);

#endif//GLUA_GLUTIL_H