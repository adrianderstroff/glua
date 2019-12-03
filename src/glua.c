// -------------------------------------------------------------------------------- //
// LUA includes                                                                     //
// -------------------------------------------------------------------------------- //
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"

// -------------------------------------------------------------------------------- //
// project includes                                                                 //
// -------------------------------------------------------------------------------- //
#include "window.h"



// mapping between the name of the lua callable function and the actual c function
static const struct luaL_Reg lualib[] = {
    {"create_window", create_window},
    {"set_window_resize_callback", setWindowResizeCallback},
    {"set_mouse_btn_callback", setMouseBtnCallback},
    {"set_mouse_move_callback", setMouseMoveCallback},
    {NULL, NULL}
};

// entrance point of the require statement in lua. the name has to be 
// luaopen_<LIBRARY_NAME>
int luaopen_glua (lua_State *L) {
    luaL_newlib(L, lualib);
    return 1;
}