from PIL import Image

img = Image.open('img.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    #print(item[0],' ',item[1],' ',item[2])
    if item[0] >= 102 and item[1] >= 102 and item[2] >= 102:
        newData.append((0, 0, 0, 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save("imgNoBackground.png", "PNG")


img = Image.open('imgNoBackground.png').convert('L')

width = 100
height = 100
img = img.resize((width, height), Image.ANTIALIAS) 

ext = ".png"
img.save("greyscale" + ext)

#img = Image.open('greyscale.png')

datas = img.getdata()

newData = []

min = 255
max = 0

for item in datas:
	if item > max:
		max = item
	if item < min:
		min = item

for item in datas:
	new = (item - min) / (max - min)
	newData.append(new * 255)
	
	
img.putdata(newData)	
img.save("normalized.png", "PNG")
