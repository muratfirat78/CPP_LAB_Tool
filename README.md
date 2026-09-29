# CPP LAB Tool

An interactive lab tool for data science sessions, built on Jupyter Notebook with `ipywidgets`. Students select a component and a run, answer questions (open, multiple choice, or programming), and their progress is saved to Google Drive.

---

## For students: Getting started in Google Colab

1. Open the notebook in Colab:  
   👉 [Open in Google Colab](https://colab.research.google.com/github/muratfirat78/CPP_LAB_Tool/blob/main/main.ipynb)

2. Sign in with your Google account when prompted.

3. Run the cell — the lab interface appears.

Your answers are automatically saved to Google Drive.

---

## For instructors: Master version

The master version shows an overview of all student progress.

1. Open the master notebook in Colab:  
   👉 [Open master version](https://colab.research.google.com/github/muratfirat78/CPP_LAB_Tool/blob/main/master%20version/master%20version.ipynb)

2. Sign in with the instructor Google account.

3. Run the cell — the overview of student answers appears.

Student answers are stored in the shared Google Drive folder `StudentAnswers_DUP_Sept2026` (folder ID: `1AdbSOXY2EMdLoKjNaX5D3DG3uMmpAn8P`). This folder must be shared as **Editor for anyone with the link**.

---

## Local setup (optional)

```bash
conda create -n cpp_lab python=3.9
conda activate cpp_lab
pip install jupyter ipywidgets numpy nbformat
git clone https://github.com/muratfirat78/CPP_LAB_Tool
cd CPP_LAB_Tool
git submodule update --init --recursive
python -m notebook
```

Open `main.ipynb` and set `online_version = False`.

---

## Structure

```
CPP_LAB_Tool/
├── main.ipynb               # Student notebook
├── questions/               # Question JSON files
├── Statistics_Dashboard/    # Interactive statistics dashboard (submodule)
├── master version/          # Instructor overview notebook
└── ...
```

## Adding questions

Questions are JSON files in the `questions/` folder. Filename format:  
`<Component>_<Run>_<index>.json`

Supported types: `open`, `multiple_choice`, `programming`.