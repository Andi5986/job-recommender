import os
from dotenv import load_dotenv
import openai
from langchain.document_loaders import UnstructuredMarkdownLoader
import tiktoken

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = openai.Client(api_key=os.getenv('OPENAI_API_KEY'))  # Corrected line

def reportTokens(prompt, model):
    encoding = tiktoken.encoding_for_model(model)
    print("\033[37m" + str(len(encoding.encode(prompt))) + " tokens\033[0m in prompt: " + "\033[92m" + prompt[:50] + "\033[0m")

class SkillMatcher:
    def __init__(self, client, model="gpt-4-1106-preview", max_tokens=3000):
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

    def generate_response(self, prompt):
        reportTokens(prompt, self.model)
        try:
            response = self.client.Completion.create(
                engine=self.model,
                prompt=prompt,
                max_tokens=self.max_tokens
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error: {e}")
            return "No response generated"
        
def main():
    skill_matcher = SkillMatcher(client)

    job_requirements = skill_matcher.load_markdown_content('./requirements.md')
    recommended_profiles = skill_matcher.load_markdown_content('./recommender.md')

    profiles = recommended_profiles.split('-' * 50 + "\n\n")

    for profile in profiles:
        prompt_job_requirements = job_requirements[:500]
        prompt_profile = profile[:3000]

        prompt_for_client = skill_matcher.generate_prompt(prompt_job_requirements, prompt_profile, 'client')
        explanation_for_client = skill_matcher.generate_response(prompt_for_client)
        print(f"Explanation for client:\n{explanation_for_client}\n")
        
        prompt_for_talent = skill_matcher.generate_prompt(prompt_job_requirements, prompt_profile, 'talent')
        explanation_for_talent = skill_matcher.generate_response(prompt_for_talent)
        print(f"Explanation for talent:\n{explanation_for_talent}\n")

if __name__ == "__main__":
    main()
