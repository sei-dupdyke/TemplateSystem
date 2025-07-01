from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

# Cache for domain -> template name
DOMAIN_TEMPLATES = {}

TEMPLATE_DIR = templates.directory


def create_template(template_name: str, domain: str) -> None:
    """Create a simple template for a domain if it does not exist."""
    path = os.path.join(TEMPLATE_DIR, template_name)
    if os.path.exists(path):
        return
    content = (
        '{% extends "base.html" %}\n'
        '{% block content %}\n'
        f'<p>Welcome to {{ domain }} replica.</p>\n'
        '{% endblock %}\n'
    )
    with open(path, 'w') as f:
        f.write(content)


@app.get("/{full_path:path}", response_class=HTMLResponse)
async def mirror(full_path: str, request: Request):
    """Handle incoming paths and render domain specific templates."""
    if not full_path:
        raise HTTPException(status_code=404)

    parts = full_path.split("/")
    domain = parts[0]
    subpath = "/".join(parts[1:])

    template_name = DOMAIN_TEMPLATES.get(domain)
    if not template_name:
        template_name = f"{domain}.html"
        create_template(template_name, domain)
        DOMAIN_TEMPLATES[domain] = template_name

    return templates.TemplateResponse(
        template_name,
        {"request": request, "domain": domain, "path": subpath},
    )
