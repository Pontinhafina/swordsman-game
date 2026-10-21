extends Area2D

var base_y: float = 0.0
var time: float = 0.0

@onready var sprite = $Sprite2D

func _ready():
	base_y = position.y
	time = randf() * PI

func _process(delta: float):
	time += delta * 4.0
	position.y = base_y + sin(time) * 3.0
	# 4 frames in 40x10 sheet
	sprite.frame = int(time * 2.0) % 4

func _on_body_entered(body):
	if body.is_in_group("player"):
		queue_free()
