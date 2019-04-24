# Create Your Own Story (CYOS)

This is CYOS group, we have created a crossover fan-fiction generator using a Web-Crawler, a textrank algorithm, and NLP techniques using the Stanford NLTK Library.

## Defintion of Crossover fan-fiction
Crossover fan-fiction is something a fan for both book1 and book2 want to write a story where 
character in book1 and book2 co-occur in a new same story.

## System Architecture
Our system has the following components:
1. Web Crawler that has crawled around 500 * 500 novels
2. Website that ask user to input their choice and give them customized feedback
3. Story_generator that based on user input and stories in the database, generate stories.

## Installation Guide
The following installation guide for MacOS or linux-based system (Ubuntu)
```bash
# install python3.6 if not exist

# install node
sudo apt install nodejs npm

# Clone the repository
git clone https://github.com/xiaotingFu/582_StoryGenerator


# Start python virtual environment
virtualenv -p python3 myenv

# start virtual env
source venv/bin/activate

# Install the dependencies for this project
pip install -r "requirements.txt"
python gen_backend/init.py

# Deploy story_generator


# Deploy the system backend
cd backend

# install dependencies for node
npm install

# start backend server
npm start

# start frontend server
cd frontend
npm install
npm start

```
