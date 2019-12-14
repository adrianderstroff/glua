def main():
    file = open("glex.h", "w+")
    guard_start(file)
    empty_line(file)

    windows_includes(file)
    empty_line(file)

    empty_line(file)
    guard_end(file)
    file.close()

def windows_includes(file):
    write_line(file, "#include <windows.h>")
    write_line(file, "#include <stdbool.h>")
    write_line(file, "#define GLDECL WINAPI")

def guard_start(file):
    write_line(file, "#ifndef GLUA_GLEX_H")
    write_line(file, "#define GLUA_GLEX_H")

def guard_end(file):
    write_line(file, "#endif//GLUA_GLEX_H")

def write_line(file, text):
    file.write(text + "\n")

def empty_line(file):
    file.write("\n")

if __name__ == "__main__":
    main()