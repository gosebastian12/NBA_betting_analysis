NBA Betting Repository
==============================

Overview
------------
Implementation of Hubacek et. al. 2019 in Python to NBA sports betting. This repository contains scripts that were written to download data from various internet sources, the data used in this project (in all its different forms), notebooks that demonstrate the analysis done, and files that represent the reports made from the results of said analyis. 

The work of this project builds on the methodology outlined in that paper, particularly in the neural networks implemented in the forcasting part of it. This is done by using the concept of Residual Neural Networks (referred to as ResNets for short; see the resources below for more information)

See below for the organization of this repository. Additionally, each directory has a similar README file that outlines the contents of that directory.

Helpful resources that were consulted in the construction and exection of this project, in addition to the academic papers included in references, are the following:
1. NBA API information (currently, there is no central place that has all of the information one would need to understand this API. Putting together these resources if the way to go.):
    1. [Information on API endpoints](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/boxscoreadvancedv2.md)
    2. [Enpoint and Parameter Documentation](https://github.com/seemethere/nba_py/wiki/stats.nba.com-Endpoint-Documentation)
    3. [Important information on using requests to connect to NBA API](https://stackoverflow.com/questions/46781563/how-to-obtain-a-json-response-from-the-stats-nba-com-api)
    4. [Organization of NBA API endpoints](https://github.com/seemethere/nba_py/wiki/Completed-Work-Log)
    5. [nba_api python package](https://github.com/swar/nba_api)
    6. [nba_api r/NBA thread](https://www.reddit.com/r/nba/comments/9j2e05/nba_api_an_nba_api_client_for_python/)
    7. [nba_py python package r/NBA thread](https://www.reddit.com/r/nba/comments/3k91g5/finally_some_documentation_for_the_statsnbacom_api/)
2. Information on ResNets:
    1. [Understanding ResNets](http://bjlkeng.github.io/posts/residual-networks/)
    2. [Building ResNets](https://towardsdatascience.com/understanding-and-coding-a-resnet-in-keras-446d7ff84d33)
3. [Inspiration for project's organization](https://medium.com/@rrfd/cookiecutter-data-science-organize-your-projects-atom-and-jupyter-2be7862f487e)
4. [xmlStats API information](https://erikberg.com/api)
5. [Basketball Reference](https://www.basketball-reference.com/)
6. [Information on the requirements.txt file](https://medium.com/@boscacci/why-and-how-to-make-a-requirements-txt-f329c685181e)
7. [Getting Started w/git video](https://www.youtube.com/watch?v=HVsySz-h9r4)
8. Other resources that were instrumental in the coding aspect of this project can be found in the docstrings of the custom functions and classes that can be found in the src directory.

Repository Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
