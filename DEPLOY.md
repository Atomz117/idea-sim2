# How to Deploy "Idea Simulation Engine" to the Web

You can easily deploy this application to **Render.com** (it offers a free tier for Python apps).

## Step 1: Push Code to GitHub
1.  **Create a new Repository** on GitHub (e.g., `idea-sim`).
2.  **Push your code**:
    ```bash
    git init
    git add .
    git commit -m "Initial deploy"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/idea-sim.git
    git push -u origin main
    ```

## Step 2: Create Service on Render
1.  Go to [Render.com](https://render.com) and sign up/login.
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub account and select your `idea-sim` repository.
4.  **Configure the Service**:
    *   **Name**: `idea-sim` (or whatever you like)
    *   **Region**: Singapore or Frankfurt (closest to India)
    *   **Runtime**: Python 3
    *   **Build Command**: `./render-build.sh`
    *   **Start Command**: `gunicorn app:app`
5.  **Free Instance**: Select the "Free" plan.
6.  Click **Create Web Service**.

## Step 3: Access Your App
Render will take a few minutes to build (it installs dependencies and downloads the AI model).
Once finished, you will see a green **Live** badge and a URL like:
`https://idea-sim-xv23.onrender.com`

**That is your permanent server link!**

## Troubleshooting
- If the build fails, check the "Logs" tab in Render.
- Ensure `requirements.txt` contains `gunicorn`.
