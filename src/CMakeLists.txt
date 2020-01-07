cmake_minimum_required (VERSION 3.0)
project (glua C)

# third party dependencies
find_package(Lua REQUIRED)
find_package(OpenGL REQUIRED)

# include directories
include_directories (
    ${CMAKE_CURRENT_BINARY_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${LUA_INCLUDE_DIR}
    ${OPENGL_INCLUDE_DIRS}
)

# all sources to compile
set (SOURCES
    gl.h
    main.c
    window.h
)

# get the name of the resulting dll and remove the lib from the name
set (LIB_NAME lib${PROJECT_NAME}.dll)
string (REPLACE lib "" LIB_NAME_SHORT ${LIB_NAME})

# add all sources to the shared library and link third party libraries
add_library (${PROJECT_NAME} SHARED ${SOURCES})
target_link_libraries (${PROJECT_NAME} ${LUA_LIBRARIES} ${OPENGL_LIBRARIES})

# copy dll after successful build to the lua include directory
# so that the module can be found be lua's require statement
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMENT "Copy file ${CMAKE_BINARY_DIR}/${LIB_NAME} to ${LUA_INCLUDE_DIR}/${LIB_NAME_SHORT}"
    COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_BINARY_DIR}/${LIB_NAME} ${LUA_INCLUDE_DIR}/${LIB_NAME_SHORT})