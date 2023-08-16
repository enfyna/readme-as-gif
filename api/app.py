from flask import Flask, request, Response, render_template, send_from_directory
from PIL import Image, ImageDraw, ImageFont

from io import BytesIO
from random import random
from os import path
import os
# import cProfile

app = Flask(__name__)

fnt = ImageFont.truetype("api/font/ModernDOS8x16.ttf", 24)

def draw_base_image(args) -> Image.Image:
	width = int(args.get('width', 600))
	height = int(args.get('height', 190))

	bg_color = int(args.get('bg_color', "0x000000"), base=16)
	font_color = int(args.get('font_color', "0xffffff"), base=16)

	img = Image.new('RGB', (width, height), bg_color)

	arg_keys = args.keys()

	if 'icon_opacity' in arg_keys:
		icon_opacity = float(args.get('icon_opacity'))
	else:
		icon_opacity = 0.5

	right = 0
	for i, key in enumerate(['icon1','icon2','icon3']):
		right += 10
		if key in arg_keys:
			icon_path = f"api/static/image/icons/{args.get(key)}.png"
			if not path.isfile(icon_path):
				return Response("Icon file not found", status=404)

			icon = Image.open(icon_path)

			if icon.mode != 'RGBA':
				icon = icon.convert('RGBA')

			icon = Image.blend(icon, Image.new('RGBA', icon.size, bg_color), 1 - icon_opacity)

			i_w, i_h = icon.size
			ratio = i_h / i_w
			new_width = min(height - 20, width // 2 - 20) // min(2, i + 1)
			new_height = int(ratio * new_width)

			icon = icon.resize((new_width, new_height))

			right += icon.width
			img.paste(icon, (width-right, height-icon.height-10), icon)

	# Create text
	text = ""

	if 'name' in arg_keys:
		name = str(args.get('name'))
		text = "\n".join((text, f"Hi! I am {name}."))

	if 'country' in arg_keys and 'job' in arg_keys:
		country = str(args.get('country'))
		job = str(args.get('job'))
		text = "\n".join((text, f"A passionate {job} from {country.capitalize()}."))

	if 'project' in arg_keys:
		project = str(args.get('project'))
		text = "\n".join((text, f"I’m currently working on a {project}."))

	if 'learning' in arg_keys:
		learning = str(args.get('learning'))
		text = "\n".join((text, f"I’m currently learning {learning}."))

	if 'askme' in arg_keys:
		askme = str(args.get('askme'))
		text = "\n".join((text, f"Ask me about {askme}."))

	if 'funfact' in arg_keys:
		funfact = str(args.get('funfact'))
		text = "\n".join((text, f"Fun fact {funfact}."))

	if len(text) > 0:
		text = text.removeprefix("\n")

		ImageDraw.Draw(img).text((10,10),text,font_color,fnt,spacing=10)

	return img

@app.route('/api/base', methods=['GET'])
def base():

	img = draw_base_image(request.args)

	buffer = BytesIO()
	img.save(
		buffer,
		format="PNG",
	)

	return Response(buffer.getvalue(), mimetype="image/png")

@app.route('/api/arkanoid', methods=['GET'])
def arkanoid():
	# pr = cProfile.Profile()
	# pr.enable()

	width = int(request.args.get('width', 600))
	height = int(request.args.get('height', 190))

	img = draw_base_image(request.args)

	paddle_color = int(request.args.get('paddle_color', "0xffffff"), base=16)
	ball_color = int(request.args.get('ball_color', "0xffffff"), base=16)

	delta = int(request.args.get('delta', 24))

	# Line Properties
	paddle_length = 100
	paddle_width = 10
	paddle_start = (width / 2) - paddle_length

	floor_height = height - (paddle_width * 3 / 2)

	# Ball Properties
	ball_size = min(floor_height-10, max(5, int(request.args.get('ball_size', 15))))
	ball_pos_x = (width + random() * width) / 3
	ball_pos_y = floor_height - ball_size

	ball_start_pos_x = ball_pos_x
	ball_start_pos_y = ball_pos_y

	ball_speed = max(1,int(request.args.get('speed', 7)))

	ball_v_speed = -ball_speed
	ball_h_speed = ball_speed if random() < 0.5 else -ball_speed

	ball_start_direction = 1 if ball_h_speed > 0 else -1

	# Loop
	jump_count = max(1,int(request.args.get('jump', 3)))
	current_jump_count = 0

	end_loop = False

	frames = []

	while True:

		if end_loop:
			break

		frame = img.copy()
		draw = ImageDraw.Draw(frame)

		draw.ellipse((ball_pos_x, ball_pos_y, ball_pos_x+ball_size, ball_pos_y+ball_size),ball_color)

		paddle_start = (2 * ball_pos_x + ball_size - paddle_length) / 2
		paddle_start = min(width-paddle_length, max(0, paddle_start))
		draw.line((paddle_start, height-paddle_width, paddle_start+paddle_length, height-paddle_width),paddle_color,paddle_width)

		frames.append(frame)

		ball_pos_y += ball_v_speed
		if ball_pos_y + ball_v_speed < 0:
			ball_v_speed *= -1
			if not current_jump_count == jump_count - 1:
				ball_h_speed += random() * (ball_speed / 2) - (ball_speed / 2)

		elif ball_pos_y + ball_v_speed > floor_height - ball_size:
			ball_v_speed *= -1
			current_jump_count += 1

			if current_jump_count < jump_count - 1:
				ball_h_speed += random() * (ball_speed / 2) - (ball_speed / 2)

			elif current_jump_count == jump_count - 1:
				# Make sure the ball always gets to the starting point on last jump
				ball_h_speed = (ball_start_pos_x - ball_pos_x) / ((floor_height-ball_size) * 2 / abs(ball_v_speed))

			elif current_jump_count == jump_count:
				end_loop = True

		ball_pos_x += ball_h_speed
		if ball_pos_x + ball_h_speed < 0 or ball_pos_x + ball_h_speed > width - ball_size:
			ball_h_speed *= -1


	buffer = BytesIO()
	frames[0].save(
		buffer,
		format="GIF",
		save_all=True,
		append_images=frames,
		optimize=True,
		duration=delta,
		loop=0, # infinite loop
	)

	# print("new bench.dmp dropped")
	# pr.disable()
	# pr.dump_stats("bench.dmp")

	return Response(buffer.getvalue(), mimetype="image/gif")

@app.route('/api/dino', methods=['GET'])
def dino():

	img = draw_base_image(request.args)

	width = int(request.args.get('width', 600))
	height = int(request.args.get('height', 190))
	delta = int(request.args.get('delta', 24))
	speed = max(2, int(request.args.get('speed', 5)))

	bg_color = max(2, int(request.args.get('bg_color', '0x000000'),base=16))

	# get dino and cactus, resize them
	dino = Image.open('api/static/image/dino/dino_base.png')
	dino_left = Image.open('api/static/image/dino/dino_left.png')
	dino_right = Image.open('api/static/image/dino/dino_right.png')
	cactus = Image.open('api/static/image/dino/cactus.png')
	floor = Image.open('api/static/image/dino/floor.png')
	quarter_floor = floor.copy()
	cloud = Image.open('api/static/image/dino/cloud.png')
	cloud_small = cloud.copy()

	w, h = dino.size
	ratio = w / h
	new_height = max(height // 4, 40)
	new_width = int(ratio * new_height)

	dino = dino.resize((new_width, new_height))
	dino_right = dino_right.resize((new_width, new_height))
	dino_left = dino_left.resize((new_width, new_height))


	w, h = cactus.size
	ratio = w / h
	# using dino height
	new_width = int(ratio * new_height)

	cactus = cactus.resize((new_width, new_height))
	cactus.convert('RGBA')

	w, h = floor.size
	ratio = w / h
	new_height = dino.height // 2
	new_width = int(ratio * new_height)
	floor_num = width // floor.width + 1

	floor = floor.resize((new_width, new_height))
	quarter_floor = quarter_floor.crop((0,0,new_width//4,floor.height))

	floor = floor.convert('RGBA')
	floor = Image.blend(floor, Image.new('RGBA', floor.size, bg_color), 0.3)

	w, h = cloud.size
	ratio = w / h
	new_height = dino.height // 2
	new_width = int(ratio * new_height)

	cloud = cloud.resize((new_width, new_height))
	cloud_small = cloud_small.resize((int(new_width * 0.5), int(new_height * 0.5)))

	# calculate dino speed and position
	dino_pos_x = width // 2

	dino_start_y = int(height - dino.height - cactus.height - 20)
	dino_start_y += speed - (dino_start_y % speed) if 0 != dino_start_y % speed else 0 # align with speed
	dino_pos_y = dino_start_y

	dino_v_speed = speed
	dino_v_speed += dino_v_speed - ((dino_start_y) % dino_v_speed) if 0 != (dino_start_y) % dino_v_speed else 0
	dino_v_speed_current = dino_v_speed

	total_frames_to_climb_cactus = cactus.height + 10 // dino_v_speed

	#calculate cactus positions
	h_w = width // 2
	q_w = width // 4
	o_w = width // 8

	c_dist_1 = min(q_w, max(o_w, int(random() * q_w))) # distance between start point and cactus 1
	c_dist_1 += speed - (c_dist_1 % speed) if 0 != c_dist_1 % speed else 0 # align with speed

	c_dist_2 = min(h_w, max(q_w + o_w, int((random() * q_w) + h_w))) # distance between cactus 1 and cactus 2
	c_dist_2 += speed - (c_dist_2 % speed) if 0 != c_dist_2 % speed else 0 # align with speed

	y = height - cactus.height

	cactusses = []
	# second cactus makes things too complicated 
	# add it later maybe
	cactusses.append([h_w - c_dist_2, y])
	# cactusses.append([h_w - c_dist_2 + c_dist_1, y])

	cactusses.append([h_w, y]) # start point

	# cactusses.append([h_w + c_dist_1, y])
	cactusses.append([h_w + c_dist_2, y])

	# cactusses.append([h_w + c_dist_2 + c_dist_1, y])
	cactusses.append([h_w + c_dist_2 + c_dist_2, y])

	# loop variables
	frames = []
	total_distance_travelled = 0
	end_loop = False

	while True:

		if end_loop:
			break

		frame = img.copy()
		draw = ImageDraw.Draw(frame)

		for i in range(0,10):
			frame.paste(floor, ((i*floor.width) - total_distance_travelled, height - floor.height // 2), floor)
		for i in range(0,20):
			frame.paste(quarter_floor, ((i*quarter_floor.width) - total_distance_travelled//2, height * 4 // 5), quarter_floor)
		for i in range(-4,5):
			frame.paste(cloud_small, (h_w + cloud.width + (i*o_w) - total_distance_travelled//4, height // 8), cloud_small)
		for i in range(-2,3):
			frame.paste(cloud, (h_w + cloud.width + (i*q_w) - total_distance_travelled//2, height // 6), cloud)

		if dino_pos_y + dino.height <= height:
			frame.paste(dino, (dino_pos_x, dino_pos_y), dino)
		else:
			if total_distance_travelled % 60 < 30:
				frame.paste(dino_left, (dino_pos_x, dino_pos_y), dino_left)
			else:
				frame.paste(dino_right, (dino_pos_x, dino_pos_y), dino_right)

		next_cactus_found = False
		for c in cactusses:
			frame.paste(cactus, (int(c[0]), int(c[1])), cactus)
			c[0] -= speed
			if dino_v_speed_current == 0 and dino_pos_y != dino_start_y:
				if next_cactus_found:
					continue
				if c[0] < dino_pos_x:
					continue
				next_cactus_found = True
				if dino_pos_x + dino.width + total_frames_to_climb_cactus > c[0]:
					dino_v_speed_current = -dino_v_speed

		frames.append(frame)

		if total_distance_travelled + speed == c_dist_2:
			end_loop = True

		dino_pos_y += dino_v_speed_current

		if dino_pos_y + dino.height >= height:
			dino_v_speed_current = 0
		elif dino_pos_y + dino_v_speed_current <= dino_start_y:
			dino_v_speed_current = 0

		total_distance_travelled += speed


	buffer = BytesIO()
	frames[0].save(
		buffer,
		format="GIF",
		save_all=True,
		append_images=frames,
		optimize=True,
		duration=delta,
		loop=0, # infinite loop
	)

	return Response(buffer.getvalue(), mimetype="image/gif")

games = [
	'arkanoid',
	'dino',
]

icon_categories = {
    'os': 'Operating Systems',
    'browser': 'Browsers',
    'ide&te': 'IDEs & Text Editors',
	'lang': 'Programming Languages',
	'libraries': 'Libraries & Frameworks',
	'drawing': 'Digital Art & Design',
	'vm': 'Virtual Machines',
	'web': 'Web Sites',
}

@app.route('/')
def index():
    icon_folder = os.path.join(app.static_folder, 'image/icons')
    icon_data = {}

    for category, label in icon_categories.items():
        category_icons = [filename.split('.')[0] for filename in os.listdir(os.path.join(icon_folder, category)) if filename.endswith('.png')]
        icon_data[category] = {
            'label': label,
            'icons': category_icons,
        }

    return render_template('index.html.jinja', icon_data=icon_data, games=games)


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(path.join(app.root_path, 'static/image'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
