import os
import sys
import ast
from dotenv import load_dotenv
from openai import OpenAI
from langchain.document_loaders import UnstructuredMarkdownLoader
import tiktoken
from time import sleep

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

openai_model = "gpt-4-1106-preview"
openai_model_max_tokens = 3000

def reportTokens(prompt, model):
    encoding = tiktoken.encoding_for_model(model)
    print("\033[37m" + str(len(encoding.encode(prompt))) + " tokens\033[0m in prompt: " + "\033[92m" + prompt[:50] + "\033[0m")

class SkillMatcher:
    def __init__(self, client, model=openai_model, max_tokens=openai_model_max_tokens):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens

    def load_markdown_content(self, file_path):
        loader = UnstructuredMarkdownLoader(file_path)
        documents = loader.load()
        texts = [doc.page_content for doc in documents]
        return ' '.join(texts)

    def generate_prompt(self, job_requirements, profile_metadata, role):
        return (
            f"Job Requirements:\n{job_requirements}\n\n"
            f"Candidate Profile:\n{profile_metadata}\n\n"
            f"Explain why this candidate is a {('good match for the job' if role == 'client' else 'good job to apply for')}:"
        )

    def generate_response(self, system_prompt, user_prompt):
        reportTokens(system_prompt, self.model)
        reportTokens(user_prompt, self.model)
        
        # Structure messages as a list of message dictionaries
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": 0,
        }

        try:
            response = self.client.chat.completions.create(**params)
            return response.choices[0].message.content.strip()
        except Exception as e:
            print("Failed to generate response. Error: ", e)
            return "No response generated"

def main():
    skill_matcher = SkillMatcher(client)

    job_requirements = skill_matcher.load_markdown_content('./requirements.md')
    recommended_profiles = skill_matcher.load_markdown_content('./recommender.md')

    profiles = recommended_profiles.split('-' * 50 + "\n\n")

    for profile in profiles:
        prompt_job_requirements = job_requirements[:500]
        prompt_profile = profile[:3000]

        system_prompt_for_client = "Please generate a detailed explanation for the following:"
        user_prompt_for_client = skill_matcher.generate_prompt(prompt_job_requirements, prompt_profile, 'client')
        explanation_for_client = skill_matcher.generate_response(system_prompt_for_client, user_prompt_for_client)
        print(f"Explanation for client:\n{explanation_for_client}\n")
        
        system_prompt_for_talent = "Please generate a detailed explanation for the following:"
        user_prompt_for_talent = skill_matcher.generate_prompt(prompt_job_requirements, prompt_profile, 'talent')
        explanation_for_talent = skill_matcher.generate_response(system_prompt_for_talent, user_prompt_for_talent)
        print(f"Explanation for talent:\n{explanation_for_talent}\n")

if __name__ == "__main__":
    main()
