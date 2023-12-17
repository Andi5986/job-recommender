# Skill Matcher Application

## Introduction
Skill Matcher is an application designed to match job requirements with candidate profiles using OpenAI's GPT-4 model. It processes job requirement details and candidate profiles, generating explanations for why a candidate is a good match for a job or why a job is suitable for a candidate.

## Features
- Loads job requirements and candidate profiles from Markdown files.
- Utilizes OpenAI's GPT-4 model to analyze and match skills.
- Generates detailed explanations for clients and talents.

## Installation

To set up the Skill Matcher application on your local machine, follow these steps:

### Prerequisites
- Python 3.8 or higher
- Pip package manager
- An active OpenAI API key

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/skill-matcher.git
   cd skill-matcher

### Install dependencies:

```bash
pip install -r requirements.txt
```

Set up your environment variables:
Create a .env file in the root directory and add your OpenAI API key:


```bash
OPENAI_API_KEY=your_api_key_here
```

### Usage
To run the Skill Matcher application:

Place your job requirements and candidate profiles in Markdown format in the respective .md files within the project directory.

### Run the application:

```bash
python recommender_client.py
```

Follow the console prompts to see the generated explanations.

### Contributing
Contributions to the Skill Matcher application are welcome. Please feel free to submit pull requests or open issues to suggest improvements or add new features.

### Contact
For any inquiries or assistance, please contact andi598610@gmail.com


