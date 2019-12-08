#include "glutil.h"

int GlClear(lua_State *L) {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    return 0;
}

int GlColor3f(lua_State *L) {
    double r = luaL_checknumber(L, 1);
    double g = luaL_checknumber(L, 2);
    double b = luaL_checknumber(L, 3);

    glColor3f(r, g, b);
    return 0;
}

int GlVertex3f(lua_State *L) {
    double x = luaL_checknumber(L, 1);
    double y = luaL_checknumber(L, 2);
    double z = luaL_checknumber(L, 3);

    glVertex3f(x, y, z);
    return 0;
}

int GlBegin(lua_State *L) {
    glBegin(GL_TRIANGLES);
}

int GlEnd(lua_State *L) {
    glEnd();
}

int GlViewport(lua_State *L) {
    double x      = luaL_checknumber(L, 1);
    double y      = luaL_checknumber(L, 2);
    double width  = luaL_checknumber(L, 3);
    double height = luaL_checknumber(L, 4);

    glViewport(x, y, width, height);
    return 0;
}