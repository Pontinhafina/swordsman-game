extends CharacterBody2D

const SPEED = 145.0
const JUMP_VELOCITY = -315.0
const GRAVITY = 620.0

@onready var sprite = $Sprite2D
@onready var attack_area = $AttackArea
@onready var attack_shape = $AttackArea/CollisionShape2D

var hero_level: int = 1
var is_attacking: bool = false
var is_hurt: bool = false
var is_dead: bool = false
var anim_timer: float = 0.0
var anim_frame: int = 0
var facing_dir: int = 1
var has_key: bool = false
var hp: int = 5

# Preloaded textures
var textures = {
	"idle": preload("res://SPRITES/HEROI/PNG/Swordsman_lvl1/Without_shadow/Swordsman_lvl1_Idle_without_shadow.png"),
	"run": preload("res://SPRITES/HEROI/PNG/Swordsman_lvl1/Without_shadow/Swordsman_lvl1_Run_without_shadow.png"),
	"attack": preload("res://SPRITES/HEROI/PNG/Swordsman_lvl1/Without_shadow/Swordsman_lvl1_attack_without_shadow.png"),
	"hurt": preload("res://SPRITES/HEROI/PNG/Swordsman_lvl1/Without_shadow/Swordsman_lvl1_Hurt_without_shadow.png"),
	"death": preload("res://SPRITES/HEROI/PNG/Swordsman_lvl1/Without_shadow/Swordsman_lvl1_Death_without_shadow.png")
}

func _ready():
	attack_shape.disabled = true
	set_anim("idle")

func _physics_process(dt: float) -> void:
	if is_dead:
		velocity.y += GRAVITY * dt
		move_and_slide()
		return

	# Gravity
	if not is_on_floor():
		velocity.y += GRAVITY * dt
		if velocity.y > 420.0:
			velocity.y = 420.0

	# Jump
	if Input.is_action_just_pressed("jump") and is_on_floor() and not is_attacking:
		velocity.y = JUMP_VELOCITY

	# Attack
	if Input.is_action_just_pressed("attack") and not is_attacking and not is_hurt:
		start_attack()

	# Horizontal Movement
	var direction := Input.get_axis("move_left", "move_right")
	if direction != 0 and not is_attacking:
		facing_dir = 1 if direction > 0 else -1
		sprite.flip_h = (facing_dir < 0)
		attack_area.scale.x = facing_dir
		velocity.x = direction * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED * 8.0 * dt)

	move_and_slide()
	update_animations(dt)

func start_attack():
	is_attacking = true
	anim_frame = 0
	anim_timer = 0.0
	set_anim("attack")

func update_animations(dt: float):
	anim_timer += dt

	if is_attacking:
		anim_frame = int(anim_timer / 0.065)
		# Hitbox active on frames 2, 3, 4
		if anim_frame >= 2 and anim_frame <= 4:
			attack_shape.disabled = false
		else:
			attack_shape.disabled = true

		if anim_frame >= 8:
			is_attacking = false
			attack_shape.disabled = true
			set_anim("idle")
		else:
			sprite.frame_coords = Vector2i(anim_frame, 2)
		return

	if not is_on_floor():
		set_anim("run")
		# Frame 2 or 5 for in-air pose
		sprite.frame_coords = Vector2i(2 if velocity.y < 0 else 5, 2)
		return

	if abs(velocity.x) > 10.0:
		set_anim("run")
		anim_frame = int(anim_timer / 0.09) % 8
		sprite.frame_coords = Vector2i(anim_frame, 2)
	else:
		set_anim("idle")
		anim_frame = int(anim_timer / 0.12) % 12
		sprite.frame_coords = Vector2i(anim_frame, 2)

func set_anim(anim_name: String):
	if sprite.texture != textures[anim_name]:
		sprite.texture = textures[anim_name]
		sprite.vframes = 4
		if anim_name == "idle":
			sprite.hframes = 12
		elif anim_name == "hurt":
			sprite.hframes = 5
		elif anim_name == "death":
			sprite.hframes = 7
		else:
			sprite.hframes = 8

func take_damage(amount: int, knockback_dir: int):
	if is_hurt or is_dead:
		return
	hp -= amount
	is_hurt = true
	velocity.x = knockback_dir * 120.0
	velocity.y = -140.0
	set_anim("hurt")

	if hp <= 0:
		die()
	else:
		await get_tree().create_timer(0.4).timeout
		is_hurt = false

func die():
	is_dead = true
	velocity.x = 0
	set_anim("death")
	anim_frame = 0
	for i in range(7):
		sprite.frame_coords = Vector2i(i, 2)
		await get_tree().create_timer(0.12).timeout

func _on_attack_area_body_entered(body):
	if body.has_method("take_damage") and body != self:
		body.take_damage(hero_level, facing_dir)
