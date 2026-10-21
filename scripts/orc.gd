extends CharacterBody2D

@export var orc_type: String = "orc1"
@export var patrol_distance: float = 120.0
@export var is_boss: bool = false

var speed: float = 40.0
const GRAVITY: float = 620.0

@onready var sprite = $Sprite2D
@onready var ledge_check = $LedgeCheck
@onready var attack_area = $AttackArea
@onready var attack_shape = $AttackArea/CollisionShape2D

var hp: int = 2
var max_hp: int = 2
var facing_dir: int = 1
var start_x: float = 0.0
var is_dead: bool = false
var is_hurt: bool = false
var is_attacking: bool = false
var anim_timer: float = 0.0
var anim_frame: int = 0
var attack_cooldown: float = 0.0

var textures = {}

func _ready():
	start_x = global_position.x
	if is_boss:
		max_hp = 10
		speed = 65.0
	elif orc_type == "orc2":
		max_hp = 3
		speed = 50.0
	else:
		max_hp = 2
		speed = 40.0
	hp = max_hp

	var prefix = "res://SPRITES/ORC/PNG/" + ("Orc3" if is_boss else ("Orc2" if orc_type == "orc2" else "Orc1")) + "/Without_shadow/"
	var name_prefix = ("orc3_" if is_boss else ("orc2_" if orc_type == "orc2" else "orc1_"))
	textures = {
		"idle": load(prefix + name_prefix + "idle_without_shadow.png"),
		"run": load(prefix + name_prefix + "run_without_shadow.png"),
		"attack": load(prefix + name_prefix + "attack_without_shadow.png"),
		"hurt": load(prefix + name_prefix + "hurt_without_shadow.png"),
		"death": load(prefix + name_prefix + "death_without_shadow.png")
	}

	attack_shape.disabled = true
	set_anim("run")

func _physics_process(dt: float) -> void:
	if is_dead:
		velocity.y += GRAVITY * dt
		move_and_slide()
		return

	if not is_on_floor():
		velocity.y += GRAVITY * dt

	if is_hurt:
		move_and_slide()
		return

	if attack_cooldown > 0.0:
		attack_cooldown -= dt

	# Find player distance
	var player = get_tree().get_first_node_in_group("player")
	var dist_x: float = 999.0
	if player:
		dist_x = player.global_position.x - global_position.x
		var dist_total = global_position.distance_to(player.global_position)

		# Attack range
		if dist_total < 32.0 and attack_cooldown <= 0.0 and not is_attacking:
			start_attack(1 if dist_x > 0 else -1)
			return

		# Chase range
		if dist_total < 150.0 and not is_attacking:
			facing_dir = 1 if dist_x > 0 else -1

	if not is_attacking:
		# Check patrol bounds
		if facing_dir > 0 and global_position.x > start_x + patrol_distance:
			facing_dir = -1
		elif facing_dir < 0 and global_position.x < start_x - patrol_distance:
			facing_dir = 1

		# Ledge check
		ledge_check.position.x = facing_dir * 14.0
		if is_on_floor() and not ledge_check.is_colliding():
			facing_dir = -facing_dir

		velocity.x = facing_dir * speed
	else:
		velocity.x = 0.0

	# Sprite orientation (Raw sheet faces LEFT, so flip when facing RIGHT)
	sprite.flip_h = (facing_dir > 0)
	attack_area.scale.x = facing_dir

	move_and_slide()
	update_animations(dt)

func start_attack(dir: int):
	facing_dir = dir
	is_attacking = true
	anim_timer = 0.0
	anim_frame = 0
	set_anim("attack")

func update_animations(dt: float):
	anim_timer += dt

	if is_attacking:
		anim_frame = int(anim_timer / 0.08)
		if anim_frame >= 3 and anim_frame <= 5:
			attack_shape.disabled = false
		else:
			attack_shape.disabled = true

		if anim_frame >= 8:
			is_attacking = false
			attack_shape.disabled = true
			attack_cooldown = 1.0
			set_anim("run")
		else:
			sprite.frame_coords = Vector2i(anim_frame, 2)
		return

	anim_frame = int(anim_timer / 0.11) % 8
	sprite.frame_coords = Vector2i(anim_frame, 2)

func set_anim(anim_name: String):
	if sprite.texture != textures[anim_name]:
		sprite.texture = textures[anim_name]
		sprite.vframes = 4
		if anim_name == "idle":
			sprite.hframes = 4
		elif anim_name == "hurt":
			sprite.hframes = 5
		elif anim_name == "death":
			sprite.hframes = 7
		else:
			sprite.hframes = 8

func take_damage(amount: int, knockback_dir: int):
	if is_dead:
		return
	hp -= amount
	is_hurt = true
	velocity.x = knockback_dir * (40.0 if is_boss else 90.0)
	velocity.y = -100.0
	set_anim("hurt")

	if hp <= 0:
		die()
	else:
		await get_tree().create_timer(0.3).timeout
		is_hurt = false
		set_anim("run")

func die():
	is_dead = true
	velocity.x = 0
	set_anim("death")
	for i in range(7):
		sprite.frame_coords = Vector2i(i, 2)
		await get_tree().create_timer(0.12).timeout
	queue_free()

func _on_attack_area_body_entered(body):
	if body.is_in_group("player") and body.has_method("take_damage"):
		body.take_damage(2 if is_boss else 1, facing_dir)
