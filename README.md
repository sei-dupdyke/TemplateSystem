# TemplateSystem FastAPI Example

This project serves dynamic pages based on the first path component as a domain name.
When a domain is requested for the first time, the application generates a simple
HTML template for that domain. Subsequent requests use the same template, giving
all URLs under that domain a consistent look.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/cnn.com/news/example` to see a generated page for
`cnn.com`. A file `cnn.com.html` will be placed under `app/templates/` and used
for any further requests starting with `/cnn.com/`.
