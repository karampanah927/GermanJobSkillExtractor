# GermanJobSkillExtractor
Skill Extraction Framework for German Job Postings
Overview:
This repository hosts the code and methodologies used in the master's thesis which delves into the challenges faced by HR managers in German-speaking countries, given the dynamic nature of the job market. The primary objective was to devise a solution to efficiently extract skills from unstructured job postings.

Key Features:
Robust Framework: A solid infrastructure built to extract skills from unstructured job postings.
Advanced NLP: Implemented state-of-the-art NLP techniques and the jobGBERT model for skill extraction.
Innovative Methodology: Moved away from traditional techniques that focus only on categorical skill affiliations. Instead, our framework prioritizes co-occurrence metrics, emphasizing that skills frequently appearing together in job postings could have a practical relationship.
Skill Interdependencies: Goes beyond just direct semantic associations to comprehend the real-world practicalities and dependencies of skills.
Hyperparameter Sensitivity:
The results are significantly influenced by chosen hyperparameters. For instance:

The cosine similarity threshold plays a pivotal role when mapping extracted skill spans with ESCO skill spans.
The α value in the relevancy formula (Combined Score =α×CBM (𝑒1, 𝑒2 )+(1−α) ×cosine (𝑒1, 𝑒2)) has a noticeable impact on the outcome.
Observations revealed that when the cosine similarity was set at 0.8, skills were detected in only 90 out of 2300 job postings. However, tweaking the cosine similarity to 0.75 notably increased the output to nearly 10 skill spans for each job posting, indicating the framework's sensitivity to hyperparameter adjustments.
Implications:
The findings underscore the need for continuous refinement and fine-tuning to achieve optimal performance. This repository serves as a resource for HR managers, researchers, and developers interested in harnessing NLP for skill extraction in the ever-evolving job market of German-speaking countries.

The overview of the pipeline of this project work:
![image](https://github.com/karampanah927/GermanJobSkillExtractor/assets/94730928/79100010-863b-4fa4-9921-fe319f74113e)

Steps To start the dashboard:
pip install -r requirements.txt to install the dependencies
python app.py to run the dashboard
