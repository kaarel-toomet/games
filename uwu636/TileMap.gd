extends TileMap


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var noise = OpenSimplexNoise.new()
var mainnoise = OpenSimplexNoise.new()
var offsetnoise = OpenSimplexNoise.new()
var chunkW = 15 #then changing these, change the numbers in hullmyts's script, that are used in the changechunk signal
var chunkH = 10
var wOffsetx = -1 # activewindow offset, top-left chunk in tiles
var wOffsety = -1
var breakto = {0:1, 1:6, 2:0, 3:0, 4:2, 5:4, 6:6, 7:2, 8:0}
#0:sand, 1:sea, 2:grass, 3:box, 4:stone, 5:snow, 6:deep sea
#7:tree, 8:cactus

func generate(cx,cy):
	if $generated.ger_cell(cx,cy) != -1:
		return
	$generated.set_cell(cx,cy,0)
	for x in range(chunkW*cx,chunkW*(cx+1)):
		for y in range(chunkH*cy,chunkH*(cy+1)):
			var gencell = -1
			noise.seed = 32
			mainnoise.octaves = 5
			mainnoise.period = 40
			mainnoise.persistence = abs(noise.get_noise_2d(x+1000,y))+0.4
			mainnoise.lacunarity = 2#(noise.get_noise_2d(x,y-1000)/2)+2
			var noiseval = mainnoise.get_noise_2d(x+43,y)+offsetnoise.get_noise_2d(x,y)
			#print(mainnoise.period, " ",mainnoise.persistence," ",mainnoise.lacunarity, " ", noiseval)
			if noiseval < -0.3:
				gencell = 6
			elif noiseval < 0:
				gencell = 1
			elif noiseval < 0.1:
				gencell = 0
			elif noiseval < 0.3:
				gencell = 2
			elif noiseval < 0.45:
				gencell = 4
			else:
				gencell = 5
			if get_cell(x,y) == -1:
				set_cell(x,y,gencell)
func lammuta(x,y):
	x = floor(x)
	y = floor(y)
	if get_cell(x,y) == -1:
		return
	set_cell(x,y,breakto[get_cell(x,y)])
func ehita(x,y):
	set_cell(floor(x),floor(y),3)






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
	scroll(0,0)

func scroll(sx,sy):
	for cx in range(3):
		for cy in range(3):
			for x in range(chunkW*(cx+wOffsetx),chunkW*(cx+wOffsetx+1)):
				for y in range(chunkH*(cy+wOffsety),chunkH*(cy+wOffsety+1)):
					pass#set_cell(x,y,-1)
					#fix_invalid_tiles()
	for cx in range(3):
		for cy in range(3):
			generate(cx + wOffsetx + sx, cy + wOffsety + sy)
	wOffsetx += sx
	wOffsety += sy

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if Input.is_action_just_pressed("LCLICK"):
		var parent = get_parent()
		var xy = parent.get_global_mouse_position()/32
		lammuta(xy[0],xy[1])
	if Input.is_action_just_pressed("RCLICK"):
		var parent = get_parent()
		var xy = parent.get_global_mouse_position()/32
		ehita(xy[0],xy[1])


func _on_hullmyts_changechunk(changex, changey):
	scroll(changex, changey)
