<h1 align="center">
	Readme As GIF
</h1>

<p align="center">
	Get a dynamically generated GIF with a game overlay on your README!
</p>

<p align="center">
	<img src="https://github.com/enfyna/readme-as-gif/assets/91965312/0a2d4dde-f336-4a33-a8b5-2532222a7a95" />
	<img src="https://github.com/enfyna/readme-as-gif/assets/91965312/b4062f8d-eddd-46c2-9a4c-e4b9483cb568" />
	<img src="https://github.com/enfyna/readme-as-gif/assets/91965312/b2e73055-534d-405a-bc0a-7f7430d6d89d" />
	<img src="https://github.com/enfyna/readme-as-gif/assets/91965312/b396e349-8a67-4a01-858f-34f5199082e7" />
</p>

<p align="center">
	Readme As GIF is a web application that creates personalized GIFs with a game overlay. Users can specify some information about them to generate personalized texts, select their most used technology icons and select the game that appear in the GIF.
</p>

<br>

# Getting Started

To use Readme As GIF, follow these simple steps:

1. **Access the Website:**
   - Go to the Readme As GIF website at:
     - [https://readme-as-gif.vercel.app/](https://readme-as-gif.vercel.app/)

2. **Base Image:**
   - On the website, locate the form.
   - Customize the form according to your preferences.
   - Click the 'Generate' button to create the base image.

3. **Game Selection:**
   - Once the base image is generated, choose the desired game overlay.
   - Click the 'Next' button to access game options.

4. **Game Customization:**
   - Fill in the relevant game options as before.
   - Click 'Generate' to combine your selections.

5. **Outcome Evaluation:**
   - If you're satisfied with the result, click 'Download' to obtain the GIF.
   - If the outcome isn't what you wanted, don't worry! Just click 'Cancel' and modify the base image.

6. **Putting it in Your Readme:**
   - Once the GIF file is downloaded, you can easily integrate it into your README by dragging and dropping.

That's it! With these steps, you can effortlessly create customized GIFs tailored to your preferences. Enjoy the creative process!

> [!NOTE]  
> If you're aiming to generate high-resolution GIFs or GIFs with longer durations, you might encounter limitations on Vercel's platform. In such cases, I recommend building this repository locally to overcome these limits.


<br>

## Building the Project

Follow these steps to set up and build the Readme As GIF project on your local machine:

1. **Clone the Repository:**
   - Clone this repository to your computer using GitHub CLI or download it as a ZIP archive.

2. **Navigate to the Project Directory:**
   - Depending on your operating system:
     - On Linux: Open the terminal application and use the `cd` command to navigate to the destination folder.
       ```
       cd path/to/destination_folder
       ```
     - On Windows:
       - Press `Windows + R`, type `cmd`, and press Enter.
       - Use the `cd` command to navigate to the folder where you extracted the project. For example:
         ```
         cd path\to\destination_folder
         ```

3. **Create a Python Virtual Environment:**
   - Set up a Python virtual environment using the following command:
     ```
     python -m venv venv
     ```

4. **Activate the Python Virtual Environment:**
   - Activate the Python virtual environment:
     - On Linux:
       ```
       source venv/bin/activate
       ```
     - On Windows:
       ```
       venv\Scripts\activate
       ```

5. **Install Project Requirements:**
   - Install the required dependencies using pip and the provided `requirements.txt` file:
     ```
     pip install -r requirements.txt
     ```

6. **Set Flask App Location:**
   - Export the location of `app.py` for Flask:
     ```
     export FLASK_APP=api/app.py
     ```

7. **Run the Application:**
   - Launch the application using the Flask development server:
     ```
     flask run
     ```

8. **Access the Application:**
   - Open your web browser and enter the following URL:
     ```
     http://127.0.0.1:5000/
     ```

<br>

# Contributing

If you find any bugs, have suggestions for improvements, or want to add new features, feel free to open an issue or submit a pull request.

Before making significant changes, please discuss them to ensure they align with the project's goals and direction.

<br>

# License

The Readme As GIF is released under the MIT License. You are free to use, modify, and distribute the code as per the terms of the license.

</p>
