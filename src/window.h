#include <windows.h>

// -------------------------------------------------------------------------------- //
// window related global variables                                                  //
// -------------------------------------------------------------------------------- //

const char g_szClassName[] = "LUAGL_WINDOW";


// -------------------------------------------------------------------------------- //
// callback related global variables                                                //
// -------------------------------------------------------------------------------- //

static lua_State *gL = NULL;
static int windowResizeCallback = -1;
static int mouseBtnCallback = -1;
static int mouseMoveCallback = -1;


// -------------------------------------------------------------------------------- //
// register callbacks from lua                                                      //
// -------------------------------------------------------------------------------- //

static int setWindowResizeCallback(lua_State *L) {
    windowResizeCallback = luaL_ref(L, LUA_REGISTRYINDEX);
    return 0;
}

static int setMouseBtnCallback(lua_State *L) {
    mouseBtnCallback = luaL_ref(L, LUA_REGISTRYINDEX);
    return 0;
}

static int setMouseMoveCallback(lua_State *L) {
    mouseMoveCallback = luaL_ref(L, LUA_REGISTRYINDEX);
    return 0;
}


// -------------------------------------------------------------------------------- //
// pass callbacks to lua                                                            //
// -------------------------------------------------------------------------------- //

static void emitWindowResizeCallback(int width, int height) {
    if (gL == NULL) return;

    // push the callback onto the stack
    lua_rawgeti(gL, LUA_REGISTRYINDEX, windowResizeCallback);
    lua_pushnumber(gL, width);
    lua_pushnumber(gL, height);

    // call the callback
    if (0 != lua_pcall(gL, 2, 0, 0)) {
        printf("Failed to call the callback!\n %s\n", lua_tostring(gL, -1) );
        return;
    }
}

static void emitMouseBtnCallback(int mouseBtn) {
    if (gL == NULL) return;

    // push the callback onto the stack
    lua_rawgeti(gL, LUA_REGISTRYINDEX, mouseBtnCallback);
    lua_pushnumber(gL, mouseBtn);

    // call the callback
    if (0 != lua_pcall(gL, 1, 0, 0)) {
        printf("Failed to call the callback!\n %s\n", lua_tostring(gL, -1) );
        return;
    }
}

static void emitMouseMoveCallback(int x, int y) {
    if (gL == NULL) return;

    // push the callback onto the stack
    lua_rawgeti(gL, LUA_REGISTRYINDEX, mouseMoveCallback);
    lua_pushnumber(gL, x);
    lua_pushnumber(gL, y);

    // call the callback
    if (0 != lua_pcall(gL, 2, 0, 0)) {
        printf("Failed to call the callback!\n %s\n", lua_tostring(gL, -1) );
        return;
    }
}


// -------------------------------------------------------------------------------- //
// windows related functions                                                        //
// -------------------------------------------------------------------------------- //

// the window event system processing
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch(msg) {
        case WM_CLOSE:
            DestroyWindow(hwnd);
            break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        case WM_SIZE:
        {
            int width  = LOWORD(lParam); 
            int height = HIWORD(lParam);
            emitWindowResizeCallback(width, height);
        }
            break;
        case WM_LBUTTONDOWN:
            emitMouseBtnCallback(0);
            break;
        case WM_RBUTTONDOWN:
            emitMouseBtnCallback(1);
            break;
        case WM_MOUSEMOVE:
        {
            int xPos = LOWORD(lParam); 
            int yPos = HIWORD(lParam);
            emitMouseMoveCallback(xPos, yPos);
        }
            break;
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

// helper method for getting the instance handle of the
// dll that created the window
HMODULE GetCurrentModule() {
    MEMORY_BASIC_INFORMATION mbi;
    static int dummy;
    VirtualQuery(&dummy, &mbi, sizeof(mbi));
 
    return (HMODULE)mbi.AllocationBase;
}

int create_window(lua_State *L) {
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
    int nCmdShow = si.wShowWindow;

    WNDCLASSEX wc;
    HWND hwnd;
    MSG Msg;

    //Step 1: Registering the Window Class
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
    wc.lpszClassName = g_szClassName;
    wc.hIconSm       = LoadIcon(NULL, IDI_APPLICATION);

    if (!RegisterClassEx(&wc)) {
        MessageBox(NULL, "Window Registration Failed!", "Error!",
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    // Step 2: Creating the Window
    hwnd = CreateWindowEx(
        WS_EX_CLIENTEDGE,
        g_szClassName,
        title,
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, width, height,
        NULL, NULL, hInstance, NULL);

    if (hwnd == NULL) {
        MessageBox(NULL, "Window Creation Failed!", "Error!",
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    // Step 3: The Message Loop
    while (GetMessage(&Msg, NULL, 0, 0) > 0) {
        TranslateMessage(&Msg);
        DispatchMessage(&Msg);
    }

    // the function returns no results to lua
    return 0;
}