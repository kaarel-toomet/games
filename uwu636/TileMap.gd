extends TileMap


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var noise = OpenSimplexNoise.new()
var chunkW = 7
var chunkH = 5
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

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if Input.is_action_just_pressed("G"):
		generate(1,2)
	if Input.is_action_just_pressed("X"):
		for cx in range(4):
			for cy in range(3):
				if cx == 0:
					for x in range(chunkW*(cx+wOffsetx),chunkW*(cx+1+wOffsetx)):
						for y in range(chunkH*(cy+wOffsety),chunkH*(cy+wOffsety+1)):
							set_cell(x,y,-1)
				if cx == 3:
					generate(cx+wOffsetx,cy+wOffsety)
		wOffsetx += 1
					
