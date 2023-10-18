import streamlit as st
import os
from dotenv import load_dotenv
from langchain.document_loaders import PDFMinerLoader
from typing import Optional, Sequence
from langchain.pydantic_v1 import BaseModel
from langchain.chains import create_extraction_chain_pydantic
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain

st.title('CV Extractor')
folder_path = "uploads"
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

@st.cache_resource
def docs_loader():
   loader = PDFMinerLoader(st.session_state.path)
   docs = loader.load()
   return docs

def summarize_CV(_docs):
   llm = ChatOpenAI(temperature=0, model_name="gpt-4")
   chain = load_summarize_chain(llm, chain_type="stuff")
   summary = chain.run(_docs)
   return summary

@st.cache_resource
def extract_CV(_docs):
   summary = summarize_CV(_docs)
   info = extract_information(_docs)
   return summary, info

def extract_information(_docs):

   class Achievement(BaseModel):
      name: str
      time: Optional[str]
      task: Optional[Sequence[str]] 

   class Volunteer (BaseModel):
      position: str
      company: str
      time: Optional[str]
      task: Optional[Sequence[str]]   

   class Education(BaseModel):
      school: str
      degree: str
      year: int
      achievement: Optional[Sequence[str]] 

   class WorkExperience(BaseModel):
      company: str
      position: str
      responsibility: Sequence[str]
      duration: str

   class Candidate(BaseModel):
      name: str
      education: Sequence[Education]
      experience: Sequence[WorkExperience]
      skills: Sequence[str]
      achievements: Optional[Sequence[Achievement]]
      volunteers: Optional[Sequence[Volunteer]]

   # Extraction
   llm = ChatOpenAI(temperature=0, model="gpt-4")
   chain = create_extraction_chain_pydantic(pydantic_schema=Candidate, llm=llm)

   # Run
   response = chain.run(_docs)
   return response

def process_uploaded_file(uploaded_file):
   if uploaded_file is not None:
      if not os.path.exists(folder_path):
         os.makedirs(folder_path)
      
      files = os.listdir(folder_path)
      file_count = len(files)
      file_name = 'resume-'+ str(file_count) + '.pdf' 
      with open(f"uploads/{file_name}", "wb") as f:
         f.write(uploaded_file.read())
         st.write('File uploaded successfully')
      return file_name

with st.container():
   uploaded_file = st.file_uploader("Upload a file", type='pdf')
   if uploaded_file is not None:
      if st.button('Process file'):
         path = process_uploaded_file(uploaded_file)
         path = './uploads/' + path
         st.session_state.path = path
         st.cache_resource.clear()
                 
if 'path' in st.session_state:
   docs = docs_loader()
   summary, info = extract_CV(docs)
   candidate = info[0]
   st.markdown(f"#### Name: {candidate.name} ####")
   st.markdown('#### Education:  ####')
   education_html = '<ul>'
   for education in candidate.education:
      education_html += f'<li><b>{education.school}</b><br/>'
      education_html += f'{education.degree} ({education.year})'
      if len(education.achievement) > 0:
         education_html += '<ul>'
         for achievement in education.achievement:
            education_html +=  f'<li>{achievement}</li>'
         education_html += '</ul>'
      education_html += '</li>'
   education_html += '</ul>'
   st.markdown(education_html, unsafe_allow_html=True)
   st.markdown('#### Experience:  ####')
   html_experience = '<ol>'
   for experience in candidate.experience:
      html_experience += f'<li>{experience.company} ({experience.duration})<br/>'
      html_experience += f'<strong>{experience.position}</strong>'
      html_experience += '<ul>'
      for responsibility  in experience.responsibility:
         html_experience += f'<li>{responsibility}</li>'
      html_experience += '</ul>'
      html_experience += '</li>'
   html_experience += '</ol>'
   st.markdown(html_experience, unsafe_allow_html=True)
   
   if len(candidate.skills) > 0:
      st.markdown('#### Skills:  ####')
      skills_html = '<ul>'
      for skill in candidate.skills:
         skills_html += f'<li>{skill}</li>'
      skills_html += '</ul>'
      st.markdown(skills_html, unsafe_allow_html=True)
    
   if len(candidate.achievements) > 0:
      st.markdown('#### Achievements:  ####')
      achievement_html = '<ol>'
      for achievement in candidate.achievements:
         achievement_html += f'<li>{achievement.name} {achievement.time}'
         if len(achievement.task) > 0:
            achievement_html += '<ul>'
            for task in achievement.task:
               achievement_html += f'<li>{task}</li>'
            achievement_html += '</ul>'
         achievement_html += '</li>'
      achievement_html += '</ol>'
      st.markdown(achievement_html, unsafe_allow_html=True)
   
   if len(candidate.volunteers) > 0:
      st.markdown('#### Volunteers:  ####')
      volunteer_html = '<ol>'
      for volunteer in candidate.volunteers:
         volunteer_html += f'<li>{volunteer.company} ({volunteer.time})<br/>'
         volunteer_html += f'<strong>{volunteer.position}</strong>'
         if len(volunteer.task) > 0:
            volunteer_html += '<ul>'
            for task in volunteer.task:
               volunteer_html += f'<li>{task}</li>'
            volunteer_html += '</ul>'
         volunteer_html += '</li>'
      volunteer_html += '</ol>'
      st.markdown(volunteer_html, unsafe_allow_html=True)

   st.markdown('#### Summary:  ####')
   st.write(f"""<p style="text-align: justify;">{summary}</p>""", unsafe_allow_html=True)

 
  
  
        



