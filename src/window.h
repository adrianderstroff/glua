#ifndef GLUA_WINDOW_H
#define GLUA_WINDOW_H

#include <windows.h>
#include "gl.h"


// -------------------------------------------------------------------------- //
// window related global variables                                            //
// -------------------------------------------------------------------------- //

const char gWindowClassName[] = "GLUA_WINDOW";
HWND gWindowHandle = NULL;
int gWindowDisplayMode = -1;


// -------------------------------------------------------------------------- //
// gl related global variables                                                //
// -------------------------------------------------------------------------- //

HDC gWindowsDeviceContext = NULL;
HGLRC gGlRenderingContext = NULL;


// -------------------------------------------------------------------------- //
// callback related global variables                                          //
// -------------------------------------------------------------------------- //

static lua_State *gL = NULL;
static int gRenderCallback       = -1;
static int gWindowResizeCallback = -1;
static int gMouseBtnCallback     = -1;
static int gMouseMoveCallback    = -1;


// -------------------------------------------------------------------------- //
// register callbacks from lua                                                //
// -------------------------------------------------------------------------- //

// registers a new render callback.
int SetRenderCallback(lua_State *L) {
    gRenderCallback = luaL_ref(L, LUA_REGISTRYINDEX);
    return 0;
}

// registers a new window resize callback.
int SetWindowResizeCallback(lua_State *L) {
    gWindowResizeCallback = luaL_ref(L, LUA_REGISTRYINDEX);
    return 0;
}

// registers a new mouse button callback.
int SetMouseBtnCallback(lua_State *L) {
    gMouseBtnCallback = luaL_ref(L, LUA_REGISTRYINDEX);
    return 0;
}

// registers a new mouse cursor callback.
int SetMouseMoveCallback(lua_State *L) {
    gMouseMoveCallback = luaL_ref(L, LUA_REGISTRYINDEX);
    return 0;
}


// -------------------------------------------------------------------------- //
// pass callbacks to lua                                                      //
// -------------------------------------------------------------------------- //

// trigger a render callback.
void EmitRenderCallback() {
    if (gL == NULL || gRenderCallback == -1) return;

    // push the callback onto the stack
    lua_rawgeti(gL, LUA_REGISTRYINDEX, gRenderCallback);

    // call the callback
    if (0 != lua_pcall(gL, 0, 0, 0)) {
        printf("Failed to call the callback!\n %s\n", lua_tostring(gL, -1) );
        return;
    }
}

// triggers a registered window resize callback with the new width and height
// of the window.
void EmitWindowResizeCallback(int width, int height) {
    if (gL == NULL || gWindowResizeCallback == -1) return;

    // push the callback onto the stack
    lua_rawgeti(gL, LUA_REGISTRYINDEX, gWindowResizeCallback);
    lua_pushnumber(gL, width);
    lua_pushnumber(gL, height);

    // call the callback
    if (0 != lua_pcall(gL, 2, 0, 0)) {
        printf("Failed to call the callback!\n %s\n", lua_tostring(gL, -1) );
        return;
    }
}

// triggers a registered mouse button callback with the pressed mouse button.
void EmitMouseBtnCallback(int mouseBtn) {
    if (gL == NULL || gMouseBtnCallback == -1) return;

    // push the callback onto the stack
    lua_rawgeti(gL, LUA_REGISTRYINDEX, gMouseBtnCallback);
    lua_pushnumber(gL, mouseBtn);

    // call the callback
    if (0 != lua_pcall(gL, 1, 0, 0)) {
        printf("Failed to call the callback!\n %s\n", lua_tostring(gL, -1) );
        return;
    }
}

// triggers a registered mouse cursor callback with the new x- and y-position
// of the mouse cursor.
void EmitMouseMoveCallback(int x, int y) {
    if (gL == NULL || gMouseMoveCallback == -1) return;

    // push the callback onto the stack
    lua_rawgeti(gL, LUA_REGISTRYINDEX, gMouseMoveCallback);
    lua_pushnumber(gL, x);
    lua_pushnumber(gL, y);

    // call the callback
    if (0 != lua_pcall(gL, 2, 0, 0)) {
        printf("Failed to call the callback!\n %s\n", lua_tostring(gL, -1) );
        return;
    }
}


// -------------------------------------------------------------------------- //
// opengl related functions                                                   //
// -------------------------------------------------------------------------- //

void CreateContext(HWND windowHandle) {
    // create pixel format
    PIXELFORMATDESCRIPTOR pfd = {
        sizeof(PIXELFORMATDESCRIPTOR),
        1,
        PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER,    //Flags
        PFD_TYPE_RGBA,        // The kind of framebuffer. RGBA or palette.
        32,                   // Colordepth of the framebuffer.
        0, 0, 0, 0, 0, 0,
        0,
        0,
        0,
        0, 0, 0, 0,
        24,                   // Number of bits for the depthbuffer
        8,                    // Number of bits for the stencilbuffer
        0,                    // Number of Aux buffers in the framebuffer.
        PFD_MAIN_PLANE,
        0,
        0, 0, 0
    };

    // get windows device context handle
    gWindowsDeviceContext = GetDC(windowHandle);

    // let windows determine a suitable pixel format from the above
    // defined pixel format description
    int  pixelFormat = ChoosePixelFormat(gWindowsDeviceContext, &pfd); 
    SetPixelFormat(gWindowsDeviceContext, pixelFormat, &pfd);

    // create OpenGL rendering context and make it current
    gGlRenderingContext = wglCreateContext(gWindowsDeviceContext);
    wglMakeCurrent (gWindowsDeviceContext, gGlRenderingContext);

    // load opengl function pointers
    if(!InitGl()) { 
        printf("Failed to initialize GL!\n");
        PostQuitMessage(0);
        return;
    }
}

void DestroyContext() {
    if(gGlRenderingContext == NULL) return;

    wglDeleteContext(gGlRenderingContext);
    gGlRenderingContext = NULL;
}

int GLuaSwapBuffers(lua_State *L) {
    SwapBuffers(gWindowsDeviceContext);
    return 0;
}

void Draw(HWND windowHandle) {
    printf("draw\n");
    PAINTSTRUCT paintStruct;
    BeginPaint(windowHandle, &paintStruct);
    
    if (gGlRenderingContext)
        EmitRenderCallback();

    EndPaint(windowHandle, &paintStruct);
}

int Redraw(lua_State *L) {
    printf("redraw\n");
    UpdateWindow(gWindowHandle);

    return 0;
}


// -------------------------------------------------------------------------- //
// windows related functions                                                  //
// -------------------------------------------------------------------------- //

// helper method that grabs the new width and height of the resized window and
// passes them to the window resize callback.
void Resize(LPARAM lParam) {
    int width  = LOWORD(lParam); 
    int height = HIWORD(lParam);
    EmitWindowResizeCallback(width, height);
}

// helper method that grabs the x- and y-pos of the mouse cursor and passes it
// to the mouse move callback.
void MouseMoveEvent(LPARAM lParam) {
    int xPos = LOWORD(lParam); 
    int yPos = HIWORD(lParam);
    EmitMouseMoveCallback(xPos, yPos);
}

// the window event system processing
LRESULT CALLBACK WndProc(HWND windowHandle, UINT message, WPARAM wParam, 
                         LPARAM lParam) {
    switch(message) {
        case WM_CREATE:
            CreateContext(windowHandle);
            break;
        case WM_CLOSE:
            DestroyContext();
            DestroyWindow(windowHandle);
            break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        case WM_SIZE:
            Resize(lParam);
            break;
        case WM_PAINT:
            Draw(windowHandle);
            break;
        case WM_LBUTTONDOWN:
            EmitMouseBtnCallback(0);
            break;
        case WM_RBUTTONDOWN:
            EmitMouseBtnCallback(1);
            break;
        case WM_MOUSEMOVE:
            MouseMoveEvent(lParam);
            break;
        default:
            return DefWindowProc(windowHandle, message, wParam, lParam);
    }
    return 0;
}

// helper method for getting the instance handle of the dll that created the 
// window.
HMODULE GetCurrentModule() {
    MEMORY_BASIC_INFORMATION mbi;
    static int dummy;
    VirtualQuery(&dummy, &mbi, sizeof(mbi));
 
    return (HMODULE)mbi.AllocationBase;
}

// create a window
int GLuaCreateWindow(lua_State *L) {
    // save lua state for later retrival
    gL = L;

    // grab input parameters from lua
    const char* title = luaL_checkstring(L, 1);
    int width   = luaL_checkinteger(L, 2);
    int height  = luaL_checkinteger(L, 3);

    // get instance handle from the module creating this class
    // the hinstance together with the class name have to 
    // uniquely identify this window.
    HINSTANCE hInstance = GetCurrentModule();
    
    // get info whether window should be started in normal,
    // minimized or maximized mode.
    STARTUPINFO si;
    GetStartupInfo(&si);  
    gWindowDisplayMode = si.wShowWindow;

    // register the window class
    WNDCLASSEX wc;
    wc.cbSize        = sizeof(WNDCLASSEX);
    wc.style         = 0;
    wc.lpfnWndProc   = WndProc;
    wc.cbClsExtra    = 0;
    wc.cbWndExtra    = 0;
    wc.hInstance     = hInstance;
    wc.hIcon         = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wc.lpszMenuName  = NULL;
    wc.lpszClassName = gWindowClassName;
    wc.hIconSm       = LoadIcon(NULL, IDI_APPLICATION);
    wc.style         = CS_OWNDC;

    if (!RegisterClassEx(&wc)) {
        printf("Window Registration Failed!");
        lua_pushboolean(gL, false);
        return 1;
    }

    // create the window
    gWindowHandle = CreateWindowEx(
        WS_EX_CLIENTEDGE,
        gWindowClassName,
        title,
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, width, height,
        NULL, NULL, hInstance, NULL);

    if (gWindowHandle == NULL) {
        printf("Window Creation Failed!");
        lua_pushboolean(gL, false);
        return 1;
    }

    // window creation successful
    lua_pushboolean(gL, true);
    return 1;
}

// displays the window and runs the message loop
int GLuaShowWindow() {
    // show and update the window
    ShowWindow(gWindowHandle, gWindowDisplayMode);
    UpdateWindow(gWindowHandle);

    // run the message loop
    MSG message;
    while (GetMessage(&message, NULL, 0, 0) > 0) {
        TranslateMessage(&message);
        DispatchMessage(&message);
    }

    return 0;
}

#endif//GLUA_WINDOW_H