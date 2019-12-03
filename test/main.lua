local gl = require 'glua'

gl.set_window_resize_callback(function(w, h)
    print("Window resize: " .. tostring(w) .. "," .. tostring(h))
end)

gl.set_mouse_btn_callback(function(mouseBtn)
    print("Mouse btn " .. tostring(mouseBtn) .. " pressed")
end)

gl.set_mouse_move_callback(function(x,y)
    print(tostring(x) .. "," .. tostring(y))
end)

gl.create_window("GL test", 400, 400)