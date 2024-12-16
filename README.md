<h1> GRAPH EXTRACTION USING OPEN AI GPT APIs</h1>

<h2> Introduction </h2>

The following project takes an image of any analytical graph (for now limited to line, bar and pie chart) and do the following:

1) Classify the image as Bar, Line, Pie chart or None of the Above(NOTA)
2) Provide a summary on the chart using the obtained class
3) Try to extract the datapoints of the chart in a JSON which can be converted to a table

The project tries to achieve this using OpenAI GPT-4o APIs and its Vision capabilites

<h2> Setup </h2>

For python environment:

1) Create a python environment:

```bash
python -m venv $(environment_name)
```

2) Activate the environment:

```bash
source $(environment_name)/bin/activate
```

3) Download the requirements:

```bash
pip install -r requirements.txt
```

For conda setup:

1) Install Anaconda and Miniconda

2) Create a new environment:

```bash
conda create --name $(environment_name) -y
```

3) Activate the environment:

```bash
conda activate $(environment_name)
```

4) Install dependencies:

```bash
pip install -r requirements.txt
```

Environment Variables Setup:

1) Create a ```.env``` file and add it to ```.gitignore```
2) Initialise your OpenAI API key in it as follows:

```OPENAI_API_KEY="$(YOUR_OPENAI_API_KEY)$"```

<h2> Running the Code</h2>

```bash
python image_class.py --image_path $(image_path)
```