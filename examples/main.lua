local glua = require 'glua'

glua.create_window("GL test", 400, 400)

glua.render(function()
    glua.gl_begin(glua.TRIANGLES)
    glua.gl_color3f(1,0,0)
    glua.gl_vertex3f(-1,-1,0)
    glua.gl_color3f(0,1,0)
    glua.gl_vertex3f(1,-1,0)
    glua.gl_color3f(0,0,1)
    glua.gl_vertex3f(0,1,0)
    glua.gl_end()
    glua.swap()
end)

glua.set_window_resize_callback(function(w, h)
    glua.gl_viewport(0,0,w,h)
    glua.redraw()
end)

glua.set_mouse_btn_callback(function(mouseBtn)
    --print("Mouse btn " .. tostring(mouseBtn) .. " pressed")
end)

glua.set_mouse_move_callback(function(x,y)
    --print(tostring(x) .. "," .. tostring(y))
end)

glua.show_window()