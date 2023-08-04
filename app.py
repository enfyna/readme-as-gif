from flask import Flask, request, Response
from PIL import Image, ImageDraw, ImageFont

from io import BytesIO
from random import random
# import cProfile

app = Flask(__name__)

# Loading font takes time so just make this a global for faster access
fnt = ImageFont.truetype("font/ModernDOS8x16.ttf", 24)

@app.route('/arkanoid', methods=['GET'])
def arkanoid():
    # pr = cProfile.Profile()
    # pr.enable()

    width = int(request.args.get('width', 600))
    height = int(request.args.get('height', 190))

    bg_color = int(request.args.get('bg_color', "0x000000"), base=16)
    font_color = int(request.args.get('font_color', "0x00ff00"), base=16)

    paddle_color = int(request.args.get('paddle_color', "0xffffff"), base=16)
    ball_color = int(request.args.get('ball_color', "0xffffff"), base=16)

    delta = int(request.args.get('delta', 24))

    img = Image.new('RGB', (width, height), bg_color)

    frames = []

    # Create text
    text = ""

    arg_keys = request.args.keys()

    if 'name' in arg_keys:
        name = str(request.args.get('name'))
        text = "\n".join((text, f"Hi! I am {name}."))

    if 'country' in arg_keys and 'job' in arg_keys:
        country = str(request.args.get('country'))
        job = str(request.args.get('job'))
        text = "\n".join((text, f"A passionate {job} from {country.capitalize()}."))

    if 'project' in arg_keys:
        project = str(request.args.get('project'))
        text = "\n".join((text, f"I’m currently working on a {project}."))

    if 'learning' in arg_keys:
        learning = str(request.args.get('learning'))
        text = "\n".join((text, f"I’m currently learning {learning}."))

    if 'askme' in arg_keys:
        askme = str(request.args.get('askme'))
        text = "\n".join((text, f"Ask me about {askme}."))

    if 'funfact' in arg_keys:
        funfact = str(request.args.get('funfact'))
        text = "\n".join((text, f"Fun fact {funfact}."))

    if len(text) > 0:
        text = text.removeprefix("\n")
        
        ImageDraw.Draw(img).text((10,10),text,font_color,fnt,spacing=10)

    # Line Properties
    paddle_length = 100
    paddle_width = 10
    paddle_start = (width / 2) - paddle_length

    floor_height = height - (paddle_width * 3 / 2)

    # Ball Properties
    ball_size = int(request.args.get('ball_size', 15))
    ball_pos_x = (width + random() * width) / 3  
    ball_pos_y = floor_height - ball_size

    ball_start_pos_x = ball_pos_x
    ball_start_pos_y = ball_pos_y

    ball_speed = int(request.args.get('speed', 7))

    ball_v_speed = -ball_speed
    ball_h_speed = ball_speed if random() < 0.5 else -ball_speed

    # Loop
    jump_count = int(request.args.get('jump', 3))
    current_jump_count = 0

    end_loop = False

    while True:
        frame = img.copy()
        draw = ImageDraw.Draw(frame)

        draw.ellipse((ball_pos_x, ball_pos_y, ball_pos_x+ball_size, ball_pos_y+ball_size),ball_color)

        paddle_start = (2 * ball_pos_x + ball_size - paddle_length) / 2
        paddle_start = min(width-paddle_length, max(0, paddle_start))
        draw.line((paddle_start, height-paddle_width, paddle_start+paddle_length, height-paddle_width),paddle_color,paddle_width)

        if end_loop:
            break

        ball_pos_y += ball_v_speed
        if ball_pos_y + ball_v_speed < 0:
            ball_v_speed *= -1
        elif ball_pos_y + ball_v_speed > floor_height - ball_size:
            ball_v_speed *= -1
            current_jump_count += 1
            if current_jump_count == jump_count - 1:
                ball_h_speed = -(ball_start_pos_x - ball_pos_x) / (floor_height * 2 / ball_v_speed)
            elif current_jump_count == jump_count:
                end_loop = True

        ball_pos_x += ball_h_speed
        if ball_pos_x + ball_h_speed < 0 or ball_pos_x + ball_h_speed > width - ball_size:
            ball_h_speed *= -1
        
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

    # print("new bench.dmp dropped")
    # pr.disable()
    # pr.dump_stats("bench.dmp")

    return Response(buffer.getvalue(), mimetype="image/gif")

if __name__ == '__main__':
    app.run(debug=True)
