# CV Extractor


## Prerequisite
1. Make sure you have installed python3 on your local machine.
2. Make sure you have OPEN_AI_KEY

## Steps
### Clone the repository
```
git clone https://github.com/hansin91/ai-text.git
```

### Change directory
```
cd cv-extractor
```

### Create virtual environment
Mac Os
```
python3 -m venv .venv
```

Windows
```
py -3 -m venv .venv
```

### Activate the environment
Mac Os
```
source .venv/bin/activate
```

Windows
```
.venv\Scripts\activate
```

### Create .env file
Mac Os
```
touch .env
```

### Insert OPENAI Key
```
OPENAI_API_KEY=YOUR_API_KEY
``` 

### Install required dependencies
```
pip install langchain python-dotenv openai pypdf pdfminer.six streamlit
```

### Run the project
```
streamlit run main.py
```

The project will be on [http://localhost:8501](http://localhost:8501)

## Screenshot
[![Application](/images/image-1.png)](Application)

[![Processing](/images/image-2.png)](Processing)

[![Result](/images/image-3.png)](Result)

[![Result](/images/image-4.png)](Result)

[![Result](/images/image-5.png)](Result)















