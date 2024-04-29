from flask import (
    Flask,
    request,
    Response,
    render_template,
    send_from_directory,
)
from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)
from os import (
    path,
    listdir,
)
from io import (
    BytesIO,
)
from random import (
    random,
    randint,
)

app = Flask(__name__)

fnt = ImageFont.truetype("api/font/ModernDOS8x16.ttf", 24)

def draw_base_image(args : dict):
    width = int(args.get('width', 600))
    height = int(args.get('height', 190))

    bg_color = int(args.get('bg_color', "0x000000"), base=16)
    font_color = int(args.get('font_color', "0xffffff"), base=16)

    img = Image.new('RGB', (width, height), bg_color)

    arg_keys = args.keys()

    icon_opacity = float(args.get('icon_opacity', 0.5))

    right_dist = 0
    for i, key in enumerate(['icon1','icon2','icon3']):
        if not key in arg_keys:
            continue

        icon_path = f"api/static/image/icons/{args.get(key)}.png"
        if not path.isfile(icon_path):
            return Response("Icon file not found", status=404)

        icon = Image.open(icon_path)

        if icon.mode != 'RGBA':
            icon = icon.convert('RGBA')

        icon = Image.blend(
            icon, 
            Image.new('RGBA', icon.size, bg_color),
            1 - icon_opacity
        )

        i_w, i_h = icon.size
        ratio = i_h / i_w
        new_width = min(height - 20, width // 2 - 20) // min(2, i + 1)
        new_height = min(height - 20, int(ratio * new_width))

        icon = icon.resize((new_width, new_height))

        top = 0
        if icon.height > height - 20:
            top = height - icon.height - 10
        elif i == 0:
            top = height//2 - icon.height//2
        else:
            top = height - height //4 - icon.height // 2

        right_dist += icon.width + 10
        img.paste(
            icon, 
            (width - right_dist, top),
            icon
        )

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

    if 'custom' in arg_keys:
        custom = str(args.get('custom')).strip()
        text = "\n".join((text, custom))

    if len(text) > 0:
        text = text.removeprefix("\n")

        ImageDraw.Draw(img).text(
            (10,10),
            text,
            font_color,
            fnt,
            spacing=10
        )

    return img

@app.route('/api/base', methods=['GET'])
def base():

    img = draw_base_image(request.args)
    if isinstance(img, Response):
        return img

    buffer = BytesIO()
    img.save(
        buffer,
        format="PNG",
        optimize=True,
    )

    return Response(buffer.getvalue(), mimetype="image/png")

@app.route('/api/arkanoid', methods=['GET'])
def arkanoid():

    width = int(request.args.get('width', 600))
    height = int(request.args.get('height', 190))

    img = draw_base_image(request.args)
    if isinstance(img, Response):
        return img

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

    ball_speed = max(1,int(request.args.get('speed', 7)))

    ball_v_speed = -ball_speed
    ball_h_speed = ball_speed if randint(0, 1) else -ball_speed

    # Loop
    jump_count = max(1,int(request.args.get('jump', 3)))
    current_jump_count = 0

    frames = []

    while current_jump_count < jump_count:

        frame = img.copy()
        draw = ImageDraw.Draw(frame)

        draw.ellipse((ball_pos_x, ball_pos_y, ball_pos_x+ball_size, ball_pos_y+ball_size),ball_color)

        paddle_start = (2 * ball_pos_x + ball_size - paddle_length) / 2
        paddle_start = max(min(width - paddle_length, paddle_start), 0)
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
    return Response(buffer.getvalue(), mimetype="image/gif")

@app.route('/api/dino', methods=['GET'])
def dino():

    img = draw_base_image(request.args)
    if isinstance(img, Response):
        return img

    width = int(request.args.get('width', 600))
    height = int(request.args.get('height', 190))
    delta = int(request.args.get('delta', 24))
    speed = max(2, int(request.args.get('speed', 5)))

    bg_color = max(2, int(request.args.get('bg_color', '0x000000'),base=16))

    sp_color = (
        *(int(request.args.get('obj_color', '000000')[i:i+2], 16) for i in (4, 2, 0)),
        255 #alpha
    )

    dino = Image.open('api/static/image/dino/dino_base.png')
    dino_left = Image.open('api/static/image/dino/dino_left.png')
    dino_right = Image.open('api/static/image/dino/dino_right.png')
    cactus = Image.open('api/static/image/dino/cactus.png')
    floor = Image.open('api/static/image/dino/floor.png').convert('RGBA')
    cloud = Image.open('api/static/image/dino/cloud.png').convert('RGBA')

    for image in (dino, dino_left, dino_right, cactus, cloud, floor):
        img_data = image.getdata()
        px = []
        for i in img_data:
            if i[3] > 0:
                px.append(sp_color)
            else:
                px.append((0,0,0,0))
        image.putdata(px)

    half_floor = floor.copy()
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

    w, h = floor.size
    ratio = w / h
    new_height = dino.height // 2
    new_width = int(ratio * new_height)

    floor = floor.resize((new_width, new_height))
    half_floor = half_floor.crop((0,0,new_width//2,floor.height))

    half_floor = Image.blend(half_floor, Image.new('RGBA', half_floor.size, bg_color), 0.3)

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
    # and dino needs to jump a lot so I dont think it looks good
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

    duration = (c_dist_2) // speed
    
    for _ in range(duration):
        frame = img.copy()

        for i in range(-5,10):
            frame.paste(
                floor,
                (floor.width + (i*o_w) - total_distance_travelled//2, height - floor.height // 2),
                floor
            )
        for i in range(-5,19):
            frame.paste(
                half_floor,
                (half_floor.width + (i*o_w) - total_distance_travelled//4, height * 4 // 5),
                half_floor
            )
        for i in range(-2,9):
            frame.paste(
                cloud_small,
                (cloud_small.width + (i*o_w) - total_distance_travelled//4, height // 8),
                cloud_small
            )
        for i in range(-2,6):
            frame.paste(
                cloud,
                (cloud.width + (i*q_w) - total_distance_travelled//2, height // 6),
                cloud
            )

        if dino_pos_y + dino.height < height:
            frame.paste(dino, (dino_pos_x, dino_pos_y), dino)
        elif total_distance_travelled % 70 < 35:
            frame.paste(dino_left, (dino_pos_x, dino_pos_y), dino_left)
        else:
            frame.paste(dino_right, (dino_pos_x, dino_pos_y), dino_right)

        next_cactus_found = False
        for c in cactusses:
            frame.paste(cactus, (int(c[0]), int(c[1])), cactus)
            c[0] -= speed
            if next_cactus_found:
                continue
            if c[0] < dino_pos_x:
                continue
            if dino_v_speed_current == 0 and dino_pos_y != dino_start_y:
                next_cactus_found = True
                if dino_pos_x + dino.width + total_frames_to_climb_cactus > c[0]:
                    dino_v_speed_current = -dino_v_speed

        dino_pos_y += dino_v_speed_current

        if dino_pos_y + dino.height >= height:
            dino_v_speed_current = 0
            dino_pos_y = height - dino.height
        elif dino_pos_y + dino_v_speed_current <= dino_start_y:
            dino_v_speed_current = 0
            dino_pos_y = dino_start_y

        total_distance_travelled += speed
        frames.append(frame)


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
    'db':'Databases',
    'drawing': 'Digital Art & Design',
    'vm': 'Virtual Machines',
    'web': 'Web Sites',
    'ge': 'Game Engines'
}

@app.route('/')
def index():
    if app.static_folder is None:
        return Response("Path not found", status=404)
    icon_folder = path.join(app.static_folder, 'image/icons')
    icon_data = {}

    for category, label in icon_categories.items():
        category_icons = [filename.split('.')[0] for filename in listdir(path.join(icon_folder, category)) if filename.endswith('.png')]
        icon_data[category] = {
            'label': label,
            'icons': category_icons,
        }

    return render_template('index.html.jinja', icon_data=icon_data, games=games)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static/image'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
