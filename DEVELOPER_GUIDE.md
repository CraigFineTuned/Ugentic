# UGENTIC Developer Guide

## 1. Introduction

This guide explains the fundamental concepts of working on the UGENTIC project, detailing the relationship between your **local machine**, the **Python virtual environment**, and the **GitHub repository**. Understanding this workflow is the key to effective, error-free development.

---

## 2. The Three Core Components

Think of the project as having three distinct parts:

### a. Your Local Filesystem (`C:\Users\craig\Desktop\MainProjects\Ugentic`)

*   **What it is:** This is your personal, private workspace. All the project files (`.py`, `.md`, etc.) live here.
*   **What happens here:** You edit code, create new files, and run the application on your machine.
*   **Key Point:** Changes you make here are **only on your computer**. They are not automatically saved or uploaded to GitHub.

### b. The Python Virtual Environment (`.venv`)

*   **What it is:** An isolated, self-contained sandbox for all the Python packages (dependencies) that our project needs. The `.venv` folder inside the project directory holds all of these packages.
*   **What happens here:** When you run `pip install -r requirements.txt`, all the packages listed in that file are downloaded and installed **into this `.venv` folder only**. They do not affect your computer's main Python installation.
*   **Key Point:** This prevents version conflicts between projects. The `.venv` folder itself is **never sent to GitHub** (it's listed in `.gitignore`). Only the *list* of required packages (`requirements.txt`) is shared.

### c. The GitHub Repository (`https://github.com/CraigFineTuned/Ugentic`)

*   **What it is:** The official, central, shared "source of truth" for our project's **code**. 
*   **What happens here:** This is where we store the definitive version of our source files (`.py`, `.md`, `config.json`, etc.) and, most importantly, the `requirements.txt` file.
*   **Key Point:** The GitHub repository does **not** contain the virtual environment or the actual installed packages. It only holds the blueprint for our code and a list of its dependencies.

---

## 3. The Core Workflow: Best Practices

This is the standard, professional workflow for keeping your local machine and GitHub perfectly in sync.

### A. Making Code Changes

1.  **Edit Locally:** Make any changes to the code on your local machine.
2.  **Test Locally:** Run the application (`run_ugentic.bat`) to make sure your changes work as expected.
3.  **Stage Changes:** Use the command `git add .` to prepare all your changes for saving.
4.  **Commit Changes:** Use `git commit -m "Your descriptive message here"` to save a snapshot of your changes to your **local** repository.
5.  **Push to GitHub:** Use `git push origin main` to upload your saved commit to the **remote** GitHub repository, making it the new official version.

### B. Managing Python Dependencies

This is critical for ensuring the project runs correctly everywhere.

**When you need to ADD a new package:**

1.  **Activate Environment:** Open a terminal in the project folder and run `.venv\Scripts\activate`.
2.  **Install Package:** Run `pip install name_of_new_package`.
3.  **Update `requirements.txt`:** This is the most important step. After installing, run the following command **exactly**: 
    ```bash
    pip freeze > requirements.txt
    ```
    This command automatically updates the `requirements.txt` file with the new package and its version.
4.  **Commit the Change:** You must now `git add .`, `git commit`, and `git push` the **updated `requirements.txt` file**. This tells the project that a new dependency is required.

**When you start on a new computer (or need to sync):**

1.  **Clone from GitHub:** Get the latest code using `git clone` or `git pull`.
2.  **Install Dependencies:** Run `run_ugentic.bat` or manually run `pip install -r requirements.txt`. This will read the `requirements.txt` file and install the correct versions of all packages into your `.venv`.

---

## 4. Troubleshooting Common Issues

*   **Problem: `ModuleNotFoundError: No module named 'some_package'`**
    *   **Cause:** You have either not installed the dependencies, or your terminal is not using the virtual environment.
    *   **Solution:** Run `run_ugentic.bat` again, or manually run `.venv\Scripts\activate` in your terminal before running the python script.

*   **Problem: "I made changes, but I don't see them on GitHub."**
    *   **Cause:** You have not committed and pushed your changes.
    *   **Solution:** You must run `git add .`, then `git commit -m "message"`, and finally `git push origin main`.

*   **Problem: "GitHub has new changes that I don't have locally."**
    *   **Cause:** The remote repository has been updated by a collaborator (or by me).
    *   **Solution:** Run `git pull origin main` to download the latest changes to your local machine.
