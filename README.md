# Yousef Hamdan portfolio

A buildless, responsive static portfolio designed for easy hosting on Vercel, Cloudflare Pages, or any static server.

## Run locally

```powershell
cd dist
python -m http.server 4173
```

Open `http://localhost:4173`.

## DislocPred: local model service

`api/models/best11.pt` is bundled with this project. The portfolio uses this local YOLOv11 pose model through the included FastAPI service; it does not send images to a third-party model API.

```powershell
cd api
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Then set `ddh.baseUrl` in `dist/site-config.js` to `http://127.0.0.1:8000` and refresh the portfolio. The demo accepts a local image upload and returns a model overlay. It is a research prototype only and must not be used for clinical diagnosis or treatment decisions.

For a container deployment:

```powershell
cd api
docker build -t dislocpred-service .
docker run -p 8000:8000 dislocpred-service
```

## Personalize

- GitHub, Hugging Face, and LinkedIn are configured. Add a résumé URL in `dist/site-config.js` if desired.
- Add approved screenshots and public demo/GitHub links to each project case study.
- Set `api.baseUrl` after a FastAPI (or similar) backend exists. The present playground is deliberately offline.

## Deploy later

Deploy the contents of `dist/` to a static host. No server-side dependency is required. A future API can be hosted separately and configured through the integration layer.
