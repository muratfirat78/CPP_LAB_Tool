# CPP LAB Tool

An interactive quiz tool for Python lab sessions, built on Jupyter Notebook with `ipywidgets`. Students select a component and a run, answer questions, and their progress is saved locally (or via Google Drive).

---

## Requirements

```bash
conda create -n cpp_lab python=3.9
conda activate cpp_lab
pip install jupyter ipywidgets numpy nbformat
```

---

## Getting started

1. Clone the repo:
```bash
   git clone https://github.com/muratfirat78/CPP_LAB_Tool
   cd CPP_LAB_Tool
```
2. Start Jupyter:
```bash
   python -m notebook
```
3. Open `main.ipynb`
4. Make sure `online_version = False`
5. Run the cell — the quiz interface appears

---

## How it works