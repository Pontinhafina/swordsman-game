extends Area2D

@export var grants_upgrade: bool = false
var opened: bool = false
@onready var sprite = $Sprite2D
@onready var prompt = $PromptLabel

func _ready():
	prompt.visible = false

func _process(_delta):
	if not opened and has_overlapping_bodies():
		for b in get_overlapping_bodies():
			if b.is_in_group("player") and Input.is_action_just_pressed("interact"):
				open_chest(b)

func _on_body_entered(body):
	if body.is_in_group("player") and not opened:
		prompt.visible = true

func _on_body_exited(body):
	if body.is_in_group("player"):
		prompt.visible = false

func open_chest(player):
	if opened:
		return
	opened = true
	prompt.visible = false
	# Animate open (frames 0 to 3 in 128x32)
	for f in range(4):
		sprite.frame = f
		await get_tree().create_timer(0.08).timeout

	if grants_upgrade and player.has_method("hero_level"):
		player.hero_level = min(3, player.hero_level + 1)
