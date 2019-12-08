// -------------------------------------------------------------------------- //
// LUA includes                                                               //
// -------------------------------------------------------------------------- //
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"

// -------------------------------------------------------------------------- //
// project includes                                                           //
// -------------------------------------------------------------------------- //
#include "window.h"
#include "glutil.h"


// mapping between the name of the lua callable function and the actual c function
static const struct luaL_Reg lualib[] = {
    {"create_window", GLuaCreateWindow},
    {"show_window", GLuaShowWindow},
    {"render", SetRenderCallback},
    {"swap", GLuaSwapBuffers},
    {"redraw", Redraw},
    {"set_window_resize_callback", SetWindowResizeCallback},
    {"set_mouse_btn_callback", SetMouseBtnCallback},
    {"set_mouse_move_callback", SetMouseMoveCallback},
    {"gl_clear", GlClear},
    {"gl_color3f", GlColor3f},
    {"gl_vertex3f", GlVertex3f},
    {"gl_begin", GlBegin},
    {"gl_end", GlEnd},
    {"gl_viewport", GlViewport},
    {NULL, NULL}
};

// entrance point of the require statement in lua. the name has to be 
// luaopen_<LIBRARY_NAME>
int luaopen_glua (lua_State *L) {
    luaL_newlib(L, lualib);
    return 1;
}

// might change the way functions are registered in order to expose variables
// defined by opengl. a way to do that can be found under the following link:
// https://stackoverflow.com/questions/9527417/wrapping-a-c-library-for-lua-how-do-i-create-nested-tables-of-functions