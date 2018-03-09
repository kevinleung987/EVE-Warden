import json
import evewarden


with open('config.json') as json_file:
    data = json.load(json_file)
window_name = data['window_name']
w_offset = data['window_offset']
l_offset = data['local_offset']
name_size = data['name_size']
name_offset = data['name_offset']


for i in range(1):
    img = evewarden.capture_window(w_offset)
    img.show()
    print("Window dimensions: "+str(img.size))
    input("w_offset being shown. Press Enter to continue...")
    img = evewarden.capture_window(l_offset)
    img.show()
    input("l_offset being shown. Press Enter to continue...")
    imgMap = img.load()
    for i in range (img.size[0]):
        for j in range(0, img.size[1], name_size+(name_offset*2)):
            imgMap[i,j] = (255, 0, 0)
    img.show()
    input("Name cutoff being shown. Press Enter to exit...")
