import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
import docx

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    return extract_text(file)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def clean_text(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop])

def extract_skills(text):
    skills_list = [
        "python","java","c++","sql","machine learning",
        "data analysis","deep learning","flask","django",
        "html","css","javascript","react","node"
    ]
    found = []
    for skill in skills_list:
        if skill in text.lower():
            found.append(skill)
    return list(set(found))

def calculate_similarity(resume, jd):
    cv = CountVectorizer()
    matrix = cv.fit_transform([resume, jd])
    return cosine_similarity(matrix)[0][1] * 100

def missing_skills(resume_skills, jd_skills):
    return list(set(jd_skills) - set(resume_skills))