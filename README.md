Open Earth Foundation
==============================

Disaggregating emissions to city level

### Key outputs
- State-level fuel sales data disaggregated to the [city-level](data/fuel_sales_estimates_by_city.csv) based on population, vehicle owning population, and trip distances.
- What-a-waste data with [city-level population data](data/city_level_data_with_population.csv) from 2016 and 2020 sourced from WorldPop estimates.

Getting Started
-------------

Directory Structure:

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── whatawaste     <- WhataWaste raw and processed data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── notebooks          <- Jupyter notebooks. fuel_sales_weighted_estimates contains the notebook for disaggregating state-level fuel sales down to city level
    │
    ├── Pipfile            <- The requirements file for reproducing the analysis environment, 
    │                         to build the environment do `pipenv install` from the project directory
    │
    ├── src                <- Source code for use in this project.
    

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
