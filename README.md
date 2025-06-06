# NLP Emotion Tracker

An end-to-end NLP-based emotion tracking system that scrapes text data from social platforms, analyzes it using machine learning, and presents results through a modern dashboard interface.

## 🎬 Project Showcase Video 📽️

## Features

## ⚙️ Tech Stack

<table align="center" style="width:100%; border-collapse: collapse; text-align: center;">
  <tr>
    <td align="center">FontEnd</td>
    <td align="center">BackEnd</td>
    <td align="center">Natural Language Processing</td>
    <td align="center">Data Analysis</td>
  </tr>
  <tr>
    <td align="center"><img src="https://skillicons.dev/icons?i=react,vite,tailwind" align="center"><br/>+<br/><img src="https://skillicons.dev/icons?i=ts" align="center"></td>
    <td align="center"><img src="https://skillicons.dev/icons?i=django" align="center"><br/>+<br/><img src="https://skillicons.dev/icons?i=postgres" align="center"></td>
    <td align="center">
      <img width="60" src="https://joblib.readthedocs.io/en/stable/_static/joblib_logo.svg" alt="joblib" title="joblib"/>
      <img width="60"src="https://cdn.prod.website-files.com/657639ebfb91510f45654149/67cb2328a0f5afcb01adc404_66bbf2250478cce84c3c3760_66bbf21b7f0ee244a1589b75_c3635b59-a3d2-444a-b636-a9d0061dcdde.png" alt="hugging_face"/>
      <br />
      <img src="https://skillicons.dev/icons?i=sklearn" align="center">
    </td>
    <td align="center">
       <img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/python.png" alt="Python" title="Python"/>
      <img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/numpy.png" alt="NumPy" title="NumPy"/>
      <img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/pandas.png" alt="Pandas" title="Pandas"/>
    </td>
  </tr>
</table>

## Project Structure

```
NLP_Emotion_Tracker/
├── backend/
│   ├── manage.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── management/
│   │       └── commands/
│   │           ├── import_data.py
│   │           └── train_and_import_test_data.py
│   ├── emotion_analyzer/
│   │   ├── analyzer.py
│   │   └── ...
│   └── nlp_emotion_tracker_backend/
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── data/
│   ├── AI Sentiment Report.html
│   ├── scrape.py
│   ├── clean data/
│   │   ├── Data_Clean.ipynb
│   │   ├── data_lab.ipynb
│   │   ├── labeled_comments.csv
│   │   └── reddit_comments_fixed.csv
│   ├── reddit/
│   │   ├── Reddit_Srapper.py
│   │   └── reddit_posts_cleaner.ipynb
│   ├── twitter X/
│   └── YouTube/
├── frontend/
│   ├── .env
│   ├── .gitignore
│   ├── bun.lockb
│   ├── components.json
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── README.md
│   ├── tailwind.config.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── public/
│   │   └── favicon.ico
│   └── src/
│       ├── assets/
│       ├── components/
│       │   ├── dashboard/
│       │   │   ├── EmotionDistributionChart.tsx
│       │   │   ├── PostCard.tsx
│       │   │   └── ...
│       │   ├── ui/
│       │   │   ├── badge.tsx
│       │   │   ├── card.tsx
│       │   │   ├── chart.tsx
│       │   │   └── progress.tsx
│       │   └── ...
│       ├── pages/
│       │   ├── Dashboard.tsx
│       │   ├── Analytics.tsx
│       │   └── ...
│       ├── routes/
│       ├── App.tsx
│       ├── main.tsx
│       ├── index.css
│       └── types/
│           └── api.d.ts
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## Setup Instructions

1. **Clone the Repository**:


``````sh
git clone https://github.com/yourusername/NLP_Emotion_Tracker.gitgit clone https://github.com/yourusername/NLP_Emotion_Tracker.git
cd NLP_Emotion_Trackercd NLP_Emotion_Tracker
``````

---- This structure supports end-to-end NLP emotion tracking, from data scraping and labeling to model training and web visualization.- The **frontend** folder contains the React frontend, with all UI components, pages, and configuration files.- The **data** folder contains datasets, scripts, and notebooks for data collection and cleaning.- The **backend** folder contains the Django backend, including API, emotion analysis, and project settings.## Notes---```docker-compose up --build```shTo run both frontend and backend using Docker Compose:### 5. Docker (Optional)---- Example: Open and run `Data_Clean.ipynb` or `data_lab.ipynb` in Jupyter Notebook.- Use the scripts and notebooks in the `data/` folder to clean, label, and prepare datasets.### 4. Data Preparation (Optional)---- The frontend will be available at `http://localhost:5173` (or as shown in your terminal).```npm run devnpm installcd ../frontend```sh### 3. Frontend Setup (React + Vite)---```python manage.py runserver```sh#### e. Start the backend server```python manage.py train_and_import_test_datapython manage.py import_data```sh#### d. (Optional) Import or train data```python manage.py migrate```sh#### c. Run migrations```pip install -r requirements.txt```sh#### b. Install dependencies```# source venv/bin/activate   # On Mac/Linuxvenv\Scripts\activate   # On Windowspython -m venv venvcd backend```sh#### a. Create and activate a virtual environment### 2. Backend Setup (Django)------



2. **Backend Setup (Django)**: 

a. Create and activate a virtual environment

```sh
cd backend
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate   # On Mac/Linux
```

b. Install dependencies

```sh
pip install -r requirements.txt
```

c. Run migrations

```sh
python manage.py migrate
```

d. (Optional) Import or train data

```sh
python manage.py import_data
python manage.py train_and_import_test_data
```

e. Start the backend server

```sh
python manage.py runserver
```

---

3. **Frontend Setup (React + Vite)** 

```sh
cd ../frontend
npm install
npm run dev
```

- The frontend will be available at `http://localhost:5173` (or as shown in your terminal).

---

4. **Data Preparation (Optional)**

- Use the scripts and notebooks in the `data/` folder to clean, label, and prepare datasets.
- Example: Open and run `Data_Clean.ipynb` or `data_lab.ipynb` in Jupyter Notebook.

---

5. **Docker (Optional)**

To run both frontend and backend using Docker Compose:

```sh
docker-compose up --build
```

---

## Notes

- The **backend** folder contains the Django backend, including API, emotion analysis, and project settings.
- The **data** folder contains datasets, scripts, and notebooks for data collection and cleaning.
- The **frontend** folder contains the React frontend, with all UI components, pages, and configuration files.
- This structure supports end-to-end NLP emotion tracking, from data scraping and labeling to model training and web visualization.

---# NLP Emotion Tracker

**Notes:**
- The `backend/` folder contains the Django backend, including API, emotion analysis, and project settings.
- The `data/` folder contains datasets, scripts, and notebooks for data collection and cleaning.
- The `frontend/` folder contains the React frontend, with all UI components, pages, and configuration files.
- This structure supports end-to-end NLP emotion tracking, from data scraping and labeling to model training and web visualization.





