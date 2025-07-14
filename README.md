# Reddit User Persona Generator

## Project Description

This project provides a Python-based solution to automatically generate detailed user personas from a Reddit user's public profile. It achieves this by scraping their comments and posts and then leveraging a Large Language Model (LLM) – specifically Google's Gemini 1.5 Flash – to extract key persona characteristics and provide direct citations from the Reddit content.

The goal is to automate the process of understanding a user's interests, personality, goals, and online behavior based on their public Reddit activity, complete with traceable evidence for each inferred trait.

## Features

* **Input Handling:** Takes a Reddit user profile URL as a command-line argument.
    * Example: `https://www.reddit.com/user/kojied/`
* **Data Scraping:** Scrapes recent comments and posts made by the specified Redditor using the PRAW (Python Reddit API Wrapper) library.
* **User Persona Generation:** Utilizes the Google Gemini 1.5 Flash LLM to analyze the scraped text and construct a comprehensive user persona, including:
    * Suggested Name
    * Age (inferred)
    * Occupation (inferred)
    * Interests & Hobbies
    * Personality Traits
    * Goals & Motivations
    * Pain Points & Challenges
    * Online Behavior
* **Citations:** For each characteristic identified in the persona, the script cites the exact Reddit comment or post content (and its URL) from which the information was extracted. If a characteristic is inferred from general activity, it is explicitly noted.
* **Output Management:** Saves the generated user persona into a `.txt` file within the `output/` directory, named after the Reddit username (e.g., `kojied_persona.txt`).

## Technologies Used

* **Python 3.8+**: The core programming language for the project.
* **PRAW (Python Reddit API Wrapper)**: For programmatic access to Reddit's API to scrape user comments and posts.
* **Google Generative AI**: The official Python client library for interacting with Google's Gemini LLM.
* **`python-dotenv`**: For securely managing API keys and other sensitive environment variables.

## Setup Instructions

Follow these steps to set up and run the project on your local machine.

### 1. Clone the Repository

First, clone this GitHub repository to your local machine:

```bash
git clone [https://github.com/your-username/reddit-user-persona.git](https://github.com/your-username/reddit-user-persona.git)
cd reddit-user-persona