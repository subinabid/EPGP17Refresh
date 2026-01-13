uv sync --frozen && uv cache prune --ci
python manage.py collectstatic --no-input