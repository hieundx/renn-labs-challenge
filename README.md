1. Create `.env` file and add `OPENAI_API_KEY=your-api-key`
2. Build docker image: `docker build . -t tag-name`
3. Run docker image: `docker run -p 8501:8501 tag-name`