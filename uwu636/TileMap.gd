extends TileMap


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var noise = OpenSimplexNoise.new()
var chunkW = 20 #then changing these, change the numbers in hullmyts's script, that are used in the changechunk signal
var chunkH = 20
var wOffsetx = 0 # activewindow offset, top-left chunk in tiles
var wOffsety = 0


func generate(cx,cy):
	for x in range(chunkW*cx,chunkW*(cx+1)):
		for y in range(chunkH*cy,chunkH*(cy+1)):
			set_cell(x,y,int(noise.get_noise_2d(x,y)+2))







# Called when the node enters the scene tree for the first time.
func _ready():
	noise.seed = 69
	noise.octaves = 4
	noise.period = 20.0
	noise.persistence = 0.8
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
