from dotenv import load_dotenv
import os
import openai
import PyPDF2
import docx
import json

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Load OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key Loaded: {openai.api_key}")

def extract_cv_data(file_path):
    try:
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            print("Unsupported file type.")
            return {"error": "Unsupported file type"}

        print("Extracted CV Text:", text[:500])  # Print first 500 characters for verification

        return extract_with_llm(text)

    except Exception as e:
        print(f"Error processing file: {e}")
        return {"error": "Failed to process the file"}

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def extract_with_llm(cv_text):
    try:
        prompt = f"""
        Extract the following details from the CV below:
        - Full Name
        - Email
        - Phone Number
        - Gender
        - Skills
        - Years of Experience (choose closest: 0-1, 1-3, 3-5, 5+)
        - Education (1-2 lines)

        CV:
        {cv_text}

        Provide the output in this JSON format:
        {{
            "name": "",
            "email": "",
            "phone": "",
            "gender": "",
            "skills": "",
            "experience": "",
            "education": ""
        }}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can use "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        print("Raw LLM Response:", response)

        llm_output = response.choices[0].message.content.strip()
        print("LLM Returned Text:", llm_output)

        extracted_data = json.loads(llm_output)
        return extracted_data

    except Exception as e:
        print(f"LLM extraction failed: {e}")
        return {"error": "LLM extraction failed"}
