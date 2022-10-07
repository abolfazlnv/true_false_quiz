
## Run Locally

Clone the project

```bash
  git clone https://github.com/abolfazlnv/true_false_quiz.git
```

Go to the project directory

```bash
  cd true_false_quiz
```

Create virtual env
```bash
  python -m venv .env
```

Active virtual env (windows)
```bash
  .env\Scripts\active
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Go to the backend directory

```bash
  cd backend
```

Migrations
```bash
  python ./manage.py makemigrations
  python ./manage.py migrate
```

Start the server

```bash
  python ./manage.py runserver
```

