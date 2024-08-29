Open Earth Foundation
==============================

Disaggregating emissions to city level

Getting Started
-------------

### Getting access to the environment

The quickest way to get started working on this project is to use Two Sigma's hosted BeakerX Lab service by following [this link](https://beakerx-waiter.app.twosigma.com/lab). This should load a BeakerX Lab instance that you can start using immediately.

Alternatively, you can host your own BeakerX instance or use an IDE if you are comfortable doing so.

### Clone this repo to your local directory 

To clone your own copy of the repo, simply run in the terminal on BeakerX or use the Git plugin that is available with BeakerX. 

```bash 
git clone https://gitlab.twosigma.com/dataclinic/hackday-q2-2024-open-earth-foundation.git
```
this will create a folder called q2-2024-open-earth-foundation in your home directory to work form.

For a refresher on git, checkout this [tutorial](https://www.freecodecamp.org/news/what-is-git-and-how-to-use-it-c341b049ae61/)

### Setting up custom nest (optional)
If you're using the hosted BeakerX Lab service, the libraries you need should be avaialable in the (automatically provided) `res_latest` environment. However, you may find that you want more flexibility with the packages/package versions you can use. If you need to create and use your custom environment, create a `nest` enironment in your IRE using the below steps:


- Login to your IRE
- Run `/opt/ts/bin/nest setup` in the shell
- Run `. /home/{your_username}/.bashrc` in the shell. 

#### Creating new environment
Creating a nest environment is pretty similar to conda. 
- Type `nest create {NEST NAME} modeling` in the shell
This creates an environment with name {env_name} based off the base modeling environment. 
- Run `nest activate {NEST NAME}` in the shell

By default nest environments are saved in your `nas/` directory and should show up on BeakerX Lab within a few minutes.

You can check that the nest is located in the correct nas subdirctory by running `nest info` after you've activated the nest on your IRE. 

### Git stuff 


### Clone this repo to your local directory on the Data Clinic 

Data Clinic projects tend to have multiple people working on them at once. If everyone is working from the
same folder, it's pretty easy to step on each others toes, for example if two people are working on the same 
notebook or code file at the same time, they will probably accidentally overwrite each other's work. Instead 
we recommend that everyone has their own copy of the code and keeps in sync using git. 

To clone your own copy of the repo, simply run

```bash 
git clone https://:@gitlab.twosigma.com:443/dataclinic/hackday-q2-2023-open-earth-foundation.git
```
this will create a folder called hackday-q2-2023-open-earth-foundation in your home directory to work form.

For a refresher on git, checkout this [tutorial](https://www.freecodecamp.org/news/what-is-git-and-how-to-use-it-c341b049ae61/)


### Git stuff 

We encourage people to follow the git feature branch workflow which you can read more about here: [https://towardsdatascience.com/why-git-and-how-to-use-git-as-a-data-scientist-4fa2d3bdc197](How to use git as a Data Scientist)

For each feature you are adding to the code 

1. Switch to the master branch and pull the most recent changes 
```
git checkout main 
git pull
```

2. Make a new branch for your addition 
```
git checkout -b cleaning_script
``` 
3. Write your awesome code.
4. Once it's done add it to git 
```
git status
git add {files that have changed}
git commit -m {some descriptive commit message}
```
5. Push the branch to gitlab 
```
git push -u origin cleaning_script
``` 
6. Go to git lab and create a merge request.
7. Either merge the branch yourself if your confident it's good or request that someone else reviews the changes and merges it in.
8. Repeat
9. ...
10. Profit.

Project Organization
------------

Data Clinic projects are a little different form internal Two Sigma projects. We work with external partners 
who will either be the ones who we hope will take our work and use it in their day to day missions to 
empower the communities they serve. We also try to open source as much of our analysis as possible 
to enable others to build on what we have done. 

Because these wider audiences will have to deal with the code / analysis we write potentially long after 
all our volunteers have moved on, we try to adhere to some best practises while working on a project.

To that end we have adopted the Data Science Cookie cutter approach to project structure. The full 
structure is described in detail in the next section but some major guidelines are:

1. Data should be immutable. Datafiles should not be modified in place ever especially the data in RAW. Instead 
scripts should be written that reads in data from a previous step and outputs the results to a new file. 

2. Treat analysis as code in a DAG: Each script should build on those that go before it, reading in data from 
the raw data files and from interim data files and generating new datasets. It shouldn't be required for you 
to run a processing stage again once it has been run. The make file is a good way to ensure this.

3. Notebooks should be for exploration and communication. Try to keep processing code out of notebooks especially 
code that can be used in multiple parts of the analysis. Instead add that code to the robinhood module. In general
someone coming to the project fresh should be able to recreate the analysis using nothing but the code in the robinhood 
directory and data in the data directory. An example notebook for how to access the module can be found in notebooks/Examples.ipynb


Directory Structure:

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
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


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
