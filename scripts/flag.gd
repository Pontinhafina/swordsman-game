extends Area2D

@onready var sprite = $Sprite2D
var timer: float = 0.0

func _process(delta):
	timer += delta
	# 4 frames in 192x48
	sprite.frame = int(timer / 0.15) % 4

func _on_body_entered(body):
	if body.is_in_group("player"):
		print("VITÓRIA DA FASE!")
