# Vorlesungsplan Alexa Skill / Lecture-Schedule

## Overview

This project is a proof-of-concept Alexa skill designed to provide information about a lecture timetable. It demonstrates how to integrate Python with Alexa's voice interface to create a simple and functional skill.

## Usecase

The Alexa skill allows users to query their lecture schedule by asking questions like "What lectures do I have today?" or "When is my next lecture?" The skill processes these queries and provides responses based on the data in the timetable.

## Source

The Alexa skill was built using:
- **Python**: For backend logic and data processing.
- **AWS Lambda**: To host the skill's backend.
- **Alexa Skills Kit (ASK)**: To define the interaction model and handle user intents.

The development process involved:
1. Setting up the Alexa skill in the Alexa Developer Console.
2. Writing the backend logic in Python to handle user intents and fetch timetable data.
3. Deploying the backend to AWS Lambda.
4. Testing the skill using the Alexa simulator and physical devices.

## Requirements

To run this project, you will need:
- **Python 3.8 or higher**: For running the backend logic.
- **AWS Account**: To deploy the backend using AWS Lambda.
- **Alexa Developer Account**: To create and manage the Alexa skill.
- **Dependencies**: Install the required Python packages using:

  ```bash
  pip install -r requirements.txt
  ```

## Configuration

Before using the project, you need to configure the timetable link in the scripts. Locate the relevant section in the Python files (e.g., `Timetable.py`) and replace the placeholder or default link with the actual URL to your timetable. Because the Website where `Timetable.py` is scraping its informations from can have many different Layouts, you may need to adjust its Filter, to produce usefull output.

Additionally, the `skill.json` file, which typically contains the Alexa skill configuration, has been removed from this repository to protect endpoint privacy. You will need to create or configure the skill manually in the Alexa Developer Console.

## About Timetable.py

The `Timetable.py` file is a core component of this project. It contains the logic for managing and querying the lecture timetable. Key functionalities include:
- Storing lecture data in a structured format.
- Providing methods to retrieve lectures for a specific day or time.
- Supporting queries like "next lecture" or "lectures for a specific day."

This file serves as the data layer for the Alexa skill, ensuring accurate and efficient responses to user queries.

To just run `Timetable.py` you dont need all of the requirements from `requirements.txt`, you will see what packets need to be installed in your IDE once you open the file.

## Disclaimer

This project is a proof of concept and is not intended for production use. It was created to explore the integration of Python with Alexa and demonstrate the potential of voice-based applications.
