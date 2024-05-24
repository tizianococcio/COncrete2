# Introduction

This is a demo application accompanying my application for a position at Alcemy. 

It implements a simple linear regression model, based on assumptions about the correlation between some factors (not all) involved in concrete production and the corresponding CO2 emission.

It is based on various sources and on information I found on Alcemy's website, in particular:
- https://alcemy.tech/en/produkt/beton
- https://en.wikipedia.org/wiki/Environmental_impact_of_concrete#Carbon_dioxide_emissions_and_climate_change

# Data
I used this information to generate synthetic data points. This is done in the file `01_data.py`. As an attempt to have somewhat realistic data, I calibrated the training set so that with the default input values (those in the `streamlit` form), the CO2 emission is about 410 kg/m3, as described in the Wikipedia article above.

# Model
What I report here is the second iteration of the model. My initial model was based on fewer input parameters, namely temperature, humidity, curing time, and energy consumption. With this simpler data set, a plain Linear Regression model was able to accurately fit the data. Adding more features, in particular dosing events, power curve, rotation speed and duration of the truck drum, the ratio of cement, sand, and gravel increased the complexity of the model, introducing nonlinear correlations. Taking this into account, I added degree-2 polynomials to the original Linear Regression model. The model is defined in the file `02_model.py`.

## Model Evaluation
The residual plot clearly shows some heteroscedasticity (non-constant variance of residuals) and potential non-linearity that is not being fully captured by the model. Running out of time and wanting to focus on the bigger picture I decided to leave the model as is. The model evaluation analysis can be fully seen in the Jupyter Notebook `03_evaluation.ipynb`.

# Streamlit App
The Streamlit frontend application provides a simple interface to the regression model. This is in `04_st_app.py`. And can be seen online at [...].

