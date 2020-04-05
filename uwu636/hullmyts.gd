extends KinematicBody2D

# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var screen_size  # Size of the game window.
var speed = 4
var pause = false


# Called when the node enters the scene tree for the first time.
func _ready():
	screen_size = get_viewport_rect().size


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if not pause:
		if Input.is_action_pressed("ui_right"):
			move_and_collide(Vector2(speed,0))
		if Input.is_action_pressed("ui_left"):
			move_and_collide(Vector2(-speed,0))
		if Input.is_action_pressed("ui_down"):
			move_and_collide(Vector2(0,speed))
		if Input.is_action_pressed("ui_up"):
			move_and_collide(Vector2(0,-speed))
		if Input.is_action_just_pressed("R"):
			position.x = 0
			position.y = 0


func _on_main_pause():
	if pause == true:
		pause = false
	else:
		pause = true
