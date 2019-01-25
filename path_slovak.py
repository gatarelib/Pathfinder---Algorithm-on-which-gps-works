from PIL import Image, ImageDraw
import PIL
from tkinter import *
import time



def get_size():					#ziskanie rozmerov: sirka, vyska, velkost pixela
	width = int(input())
	height = int(input())
	pixel_size = int(input())
	return width*pixel_size, height*pixel_size, pixel_size

width, height, pixel_size = get_size()


#cely tento blok sluzi na vykreslovanie farieb pomocou kurzora
def paint_obsacle(event):		#kreslenie prekazok = tahanie kurzorom
	x1,y1 = (event.x)//pixel_size, (event.y)//pixel_size
	platno.create_rectangle(x1*pixel_size,y1*pixel_size,x1*pixel_size+pixel_size,y1*pixel_size+pixel_size, fill = "black")
	draw.rectangle([x1*pixel_size,y1*pixel_size,x1*pixel_size+pixel_size,y1*pixel_size+pixel_size], fill = "black")

def paint_start(event):			#kreslenie startu = len klik
	x1,y1 = (event.x)//pixel_size, (event.y)//pixel_size
	platno.create_rectangle(x1*pixel_size,y1*pixel_size,x1*pixel_size+pixel_size,y1*pixel_size+pixel_size, fill = "red", outline = "red")
	draw.rectangle([x1*pixel_size,y1*pixel_size,x1*pixel_size+pixel_size,y1*pixel_size+pixel_size], fill = "red", outline = "red")

def paint_end(event):			#kreslenie konca = len klik
	x1,y1 = (event.x)//pixel_size, (event.y)//pixel_size
	platno.create_rectangle(x1*pixel_size,y1*pixel_size,x1*pixel_size+pixel_size,y1*pixel_size+pixel_size, fill = "blue", outline = "blue")
	draw.rectangle([x1*pixel_size,y1*pixel_size,x1*pixel_size+pixel_size,y1*pixel_size+pixel_size], fill = "blue", outline = "blue")

def erase(event):				#vymazavanie = klik
	x1,y1 = (event.x)//pixel_size, (event.y)//pixel_size
	platno.create_rectangle(x1*pixel_size,y1*pixel_size,x1*pixel_size+pixel_size,y1*pixel_size+pixel_size, fill = "white", outline = "grey")
	draw.rectangle([x1*pixel_size,y1*pixel_size,x1*pixel_size+pixel_size,y1*pixel_size+pixel_size], fill = "white", outline = "white")
#


def farba_pixelu(x,y):					#posuvame v obidvoch smeroch o +1, kvoli tomu, ze by sme vzdy
	r,g,b = image.getpixel((x+1,y+1))	# zistovali farbu mriezky, presne tu ciaru a farbu bunky
	return r,g,b



def make():								#vytvori maticu plnu 0 cim si zadefinujeme ze dany bod v matici
	arr = []							#nebol prehladany, ak by bol boly by  tam suradnice + najde start + najde end
	count = 0
	for riadok in range(0,width,pixel_size):
		arr.append([])
		for stlpec in range(0,height,pixel_size):
			arr[riadok//pixel_size].append(0)

			if(farba_pixelu(riadok,stlpec) == (255,0,0)):
				start = [riadok,stlpec]
				count += 1
			if(farba_pixelu(riadok,stlpec) == (0,0,255)):
				end = [riadok,stlpec]
				count += 1

	return arr,start,end



def poinf_info(x,y):					#prehladava vsetkych svojich susedov ak vyvojuju podmienkam:
	info = []							#nachadzaju sa v mriezke + nie su ciernej farby (prekazka)
										#a nie su farby sivej (uz objaveny/prehladany sused)
	if(not(y-pixel_size < 0) and farba_pixelu(x,y-pixel_size) != (0,0,0) and farba_pixelu(x,y-pixel_size) != (128,128,128)):
		info.append([x,y-pixel_size])
	if(not(x+pixel_size+1 > width) and farba_pixelu(x+pixel_size,y) != (0,0,0) and farba_pixelu(x+pixel_size,y) != (128,128,128)):
		info.append([x+pixel_size,y])
	if(not(y+pixel_size+1 > height) and farba_pixelu(x,y+pixel_size) != (0,0,0) and farba_pixelu(x,y+pixel_size) != (128,128,128)):
		info.append([x,y+pixel_size])
	if(not(x-pixel_size < 0) and farba_pixelu(x-pixel_size,y) != (0,0,0) and farba_pixelu(x-pixel_size,y) != (128,128,128)):
		info.append([x-pixel_size,y])
	return info



def execute():							#BFS = srdce celeho algoritmu
	arr,start,end = make()
	que = [start]


	x_start,y_start = start
	S = [x_start//pixel_size,y_start//pixel_size]

	x_end, y_end = end
	E = [x_end,y_end]
	i = 0
	while(arr[x_end//pixel_size][y_end//pixel_size] == 0):
		if(len(que) == 0):
			label_no_path = Label(root, text = "NO PATH!")
			label_no_path.pack()
			return 

		arr_of_visiting = poinf_info(*que[0])
		for element in range(len(arr_of_visiting)):
			
			if(arr_of_visiting[element] not in que):
				que.append(arr_of_visiting[element])
				x,y = arr_of_visiting[element]
				arr[x//pixel_size][y//pixel_size] = [que[0][0]//pixel_size,que[0][1]//pixel_size]

				if(S != [x//pixel_size,y//pixel_size] and E != [x,y]):
					platno.create_rectangle(x,y,x+pixel_size,y+pixel_size, fill = "grey")
					draw.rectangle([x,y,x+pixel_size,y+pixel_size], fill = "grey", outline = "grey")
					
					platno.update()
					time.sleep(0.0001) 
		que.pop(0)

	
	E = arr[x_end//pixel_size][y_end//pixel_size]
	step = 0
	walker = E

	while(walker != S):
		x = walker[0]
		y = walker[1]
		platno.create_rectangle(x*pixel_size,y*pixel_size,x*pixel_size+pixel_size,y*pixel_size+pixel_size, fill = "light goldenrod", outline = "light goldenrod")
		walker = arr[walker[0]][walker[1]]
		
		platno.update()
		time.sleep(0.0001) 
		step += 1

	label_step = Label(root, text = str(step)+" STEPS")
	label_step.pack()
	


root = Tk()
root.title("SHORTEST PATH BETWEEN 2 POINTS")

platno = Canvas(root, width = width, height = height, bg = "white")
platno.pack()

image = PIL.Image.new("RGB", (width,height), "white")
draw = ImageDraw.Draw(image)



def create_grid(width,height,pixel_size):	#vytvorenie mriezky vodorovne a potom zvisle
	for riadok in range(pixel_size,height,pixel_size):
		platno.create_line(0,riadok,width,riadok, fill = "grey")
	for stlpec in range(pixel_size,width,pixel_size):
		platno.create_line(stlpec,0,stlpec,height, fill = "grey")

create_grid(width,height,pixel_size)

											#volanie funkcii na kreslenie
platno.bind("<B2-Motion>", paint_obsacle)	#tahanie kurzorom = prekazky
platno.bind("<Button-2>", erase)			#vymazanie nechceneho pixelu (prefarbenie naspat na bielo)
platno.bind("<Button-1>", paint_start)		#klik start
platno.bind("<Button-3>", paint_end)		#klik koniec


but_exe = Button(root, text = "EXECUTE", command = execute)
but_exe.pack()

root.mainloop()