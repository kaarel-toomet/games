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
			set_cell(x,y,int(noise.get_noise_2d(x+chunkW*wOffsetx,y+chunkH*wOffsety)+2))







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
	# sx/sy are in chunks
	# wOffset x/y are in tiles
	wOffsetx += sx*chunkW 
	wOffsety += sy*chunkH 
	for cx in range(3):
			for cy in range(3):
				for x in range(chunkW):
					for y in range(chunkH):
						set_cell(cx*chunkW+x,cy*chunkH+y,
								get_cell(cx*(chunkW+sx)+x,cy*(chunkH+sy)+y))

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if Input.is_action_just_pressed("G"):
		generate(1,2)
	if Input.is_action_just_pressed("X"):
		for cx in range(3):
			for cy in range(3):
				scroll(1,0)
					
