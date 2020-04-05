extends TileMap


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var noise = OpenSimplexNoise.new()
var mainnoise = OpenSimplexNoise.new()
var offsetnoise = OpenSimplexNoise.new()
var chunkW = 15 #then changing these, change the numbers in hullmyts's script, that are used in the changechunk signal
var chunkH = 10
var wOffsetx = 0 # activewindow offset, top-left chunk in tiles
var wOffsety = 0


func generate(cx,cy):
	for x in range(chunkW*cx,chunkW*(cx+1)):
		for y in range(chunkH*cy,chunkH*(cy+1)):
			noise.seed = 32
			mainnoise.octaves = 5
			mainnoise.period = 40
			mainnoise.persistence = abs(noise.get_noise_2d(x+1000,y)/2)+0.4
			mainnoise.lacunarity = (noise.get_noise_2d(x,y-1000)/2)+2
			var noiseval = mainnoise.get_noise_2d(x+43,y)+offsetnoise.get_noise_2d(x,y)
			#print(mainnoise.period, " ",mainnoise.persistence," ",mainnoise.lacunarity, " ", noiseval)
			if noiseval < -0.3:
				set_cell(x,y,6)
			elif noiseval < 0:
				set_cell(x,y,1)
			elif noiseval < 0.1:
				set_cell(x,y,0)
			elif noiseval < 0.3:
				set_cell(x,y,2)
			elif noiseval < 0.45:
				set_cell(x,y,4)
			else:
				set_cell(x,y,5)







# Called when the node enters the scene tree for the first time.
func _ready():
	randomize()
	noise.seed = 434
	noise.octaves = 5
	noise.period = 100
	noise.persistence = 0.5
	noise.lacunarity = 2
	offsetnoise.seed = 434
	offsetnoise.octaves = 5
	offsetnoise.period = 500
	offsetnoise.persistence = 0.5
	offsetnoise.lacunarity = 2
	randomize()
	for x in range(3):
		for y in range (3):
			generate(x,y)

func scroll(sx,sy):
	for cx in range(3):
		for cy in range(3):
			for x in range(chunkW*(cx+wOffsetx),chunkW*(cx+wOffsetx+1)):
				for y in range(chunkH*(cy+wOffsety),chunkH*(cy+wOffsety+1)):
					set_cell(x,y,-1)
					fix_invalid_tiles()
	for cx in range(3):
		for cy in range(3):
			generate(cx + wOffsetx + sx, cy + wOffsety + sy)
	wOffsetx += sx
	wOffsety += sy

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if Input.is_action_just_pressed("G"):
		generate(1,2)
	if Input.is_action_just_pressed("X"):
		scroll(1,0)


func _on_hullmyts_changechunk(changex, changey):
	scroll(changex, changey)
