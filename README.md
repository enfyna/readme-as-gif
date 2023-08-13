<h1 align="center">
	Arkanoid GIF Generator
</h1>

<p align="center">
	Get a dynamically generated Arkanoid game on your README!
</p>

<p align="center">
	<img src="https://github.com/enfyna/arkanoid-github-readme/assets/91965312/18b304e9-fd04-47d0-8199-e079d393575e" />
</p>

<p align="center">

The Arkanoid GIF Generator is a web application that creates personalized Arkanoid gameplay GIFs with customizable text. Users can specify some information about them through URL query parameters to generate personalized texts that appear alongside the Arkanoid game in the GIF.

<br>

# Getting Started

> ***Note*** : This method is very easy but every time you open your readme this API will generate a GIF from scratch so the response time is a bit slow and if you want do a lot of customizations the API response time will increase more. And vercel has limits so for example if you want a bigger window you could hit the limit. Because of this I recommend [building](#building) this repo on your computer and after you generated your GIF save it to your computer add it to your readme as a normal GIF.

To use the Arkanoid GIF Generator, simply access the website at:

	https://arkanoid-github-readme.vercel.app/api/arkanoid

Once you are on the website, you will see a very basic black and white arkanoid game playing.
After you have made your [customizations](#customization) copy the full URL and embed it as an image in your README.md like this:

	<p align="center">
		<img src="https://arkanoid-github-readme.vercel.app/arkanoid" />
	</p>

> Note : When you paste this pay attention to the colorization and spacing of your code to ensure the tags are colored. If the HTML tags are not colored correctly you need to adjust your spacing.

<br>

# Customization

<p align="center">
	<img src="https://github.com/enfyna/arkanoid-github-readme/assets/91965312/0f39f4b5-b4d2-4450-bf9e-43df0e6c9d70" />
</p>

<p align="center">
	<img src="https://github.com/enfyna/arkanoid-github-readme/assets/91965312/2125a0e2-6746-4fcb-b66c-29d2db68b4a6" />
</p>
You can create personalized Arkanoid GIFs by providing the query parameters in the URL.


### Text Customizations

The provided text will be overlaid on the Arkanoid gameplay.

Example :

	https://arkanoid-github-readme.vercel.app/api/arkanoid?name=enfyna&job=frontend%20developer&country=Turkey

- `name` : Your name.
- `project` : The name of the project you are currently working on.
- `learning` : The subject or skill you are currently learning.
- `askme` : The subject or skill you are confident in.
- `funfact` : A short fun fact that you know.
- `country` : Your homeland. (To use this you have to set `job`)
- `job` : Your current job. (To use this you have to set `country`)


### Window Customizations

- `width` : Window width in px. (default : 600)
- `height` : Window height in px. (default : 190)

Note : The response time will slow down if you give too high values to the width and height.

Note : If you give a too low value for the height the ball may not make a correct loop.

- `delta` : Duration between frames in ms. (default : 24)

Note : If you try to use a too low value the result may become laggy.

### Color Customizations

Colors are in hexadecimal.

Example :

	https://arkanoid-github-readme.vercel.app/api/arkanoid?bg_color=224488&ball_color=ffaa88

- `bg_color` : Window background color. (default : 000000)
- `font_color` : Window font color. (default : FFFFFF)
- `paddle_color` : Paddle color. (default : FFFFFF)
- `ball_color` : Ball color. (default : FFFFFF)

### Game Customizations

Some parameters to customize the game. Changing these could change the response time a lot.  

- `ball_size` : Ball size in px. Increasing this will reduce the response time. (default : 15)
- `speed` : Ball speed in px/frame. Increasing this will reduce the response time. (default : 7)
- `jump` : Ball jump count. Decreasing this will reduce the response time. (default : 3)


<br>

# Building

1. Clone this repo to your computer. You can use github CLI or just download it as a zip.

2. If you used CLI 'cd' to the destination folder. If you downloaded it as a zip extract it in a folder and open the folder that you extracted to and with right click select "open terminal here". 

3. Create python virtual environment:

		python -m venv venv

4. Activate python venv by sourcing it:

		. venv/bin/activate

> Note : On windows it should be : venv\bin\activate.bat

5. Install requirements:

		pip install -r requirements.txt

6. Export app.py location for flask:

		export FLASK_APP=api/app.py

7. Run it : 

		flask run

8. Open your browser and enter this URL:

		http://127.0.0.1:5000/arkanoid


# Contributing

If you find any bugs, have suggestions for improvements, or want to add new features, feel free to open an issue or submit a pull request.

Before making significant changes, please discuss them to ensure they align with the project's goals and direction.


<br>


# License

The Arkanoid GIF Generator is released under the MIT License. You are free to use, modify, and distribute the code as per the terms of the license.

</p>
