# glua
OpenGL all in one module for Lua

## LUA C module
This is an instruction for developing LUA C modules under Windows. So far this has been tested with MinGW64.

Make sure to compile LUA with the same compiler you compile the module with. One way is to download the LUA sourcecode and then run

```mingw32-make PLAT=mingw```

in the LUA source directory. Then copy the code to the location of interest. Copy the new path and create an environment variable for windows called ***LUA_DIR*** since the CMake FindLUA script is looking for the path. Then make sure to use this environment variable in the path as: ```%LUA_DIR%```.

Now you can try to build the module using CMake. Make sure that CMake can find the LUA directory. Then configure and generate then calling ```mingw32-make PLAT=mingw``` in the build directory to get a <MODULE_NAME>.dll.

The dll has to be moved to a directory where LUA can find it. If you receive an error similar to

```
module 'xyz' not found
        ...
        no file '.\xyz.lua'
        no file '.\lib\init.lua'
        ...
        no file '.\xyz.dll'
stack traceback:
        [C]: in function 'require'
        ...
        no file '.\xyz.lua'
        no file '.\lib\init.lua'
        ...
        no file '.\xyz.dll'
```
where ```xyz``` is the name of the module that had been required, it means that LUA couldn't find the module. A possible location would be to put it in the ***LUA_DIR***.