<h1 align="center">
	Arkanoid GIF Generator
</h1>

<p align="center">
	Get a dynamically generated Arkanoid game on your README!
</p>

<p align="center">
	<img src="https://arkanoid-github-readme.vercel.app/arkanoid?speed=10&delta=48" />
</p>

<p align="center">

The Arkanoid GIF Generator is a web application that creates personalized Arkanoid gameplay GIFs with customizable text. Users can specify some information about them through URL query parameters to generate personalized texts that appear alongside the Arkanoid game in the GIF.

<br>

# Getting Started

To use the Arkanoid GIF Generator, simply access the website at:

	https://arkanoid-github-readme.vercel.app/arkanoid

Once you are on the website, you will see a very basic black and white arkanoid game playing.

To use this in your readme you have 2 options.

Option 1:

	![](https://arkanoid-github-readme.vercel.app/arkanoid)

Simply copy and paste this in your readme. The GIF will be left aligned.

Option 2:

	<p align="center">
		<img src="https://arkanoid-github-readme.vercel.app/arkanoid" />
	</p>

When you paste this pay attention to the colorization and spacing of your code to ensure the tags are colored. If the HTML tags are not colored correctly you may need to adjust your spacing. But if you setup this correctly you can select how the GIF will be aligned.

# Customization

You can create personalized Arkanoid GIFs by providing the query parameters in the URL.

### Text Customizations

The provided text will be overlaid on the Arkanoid gameplay.

Example :

	https://arkanoid-github-readme.vercel.app/arkanoid?name=enfyna&job=frontend%20developer&country=Turkey

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

	https://arkanoid-github-readme.vercel.app/arkanoid?bg_color=224488&ball_color=ffaa88

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


# Contributing

If you find any bugs, have suggestions for improvements, or want to add new features, feel free to open an issue or submit a pull request.

Before making significant changes, please discuss them to ensure they align with the project's goals and direction.


<br>


# License

The Arkanoid GIF Generator is released under the MIT License. You are free to use, modify, and distribute the code as per the terms of the license.

</p>