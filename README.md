[![Python Tests](https://github.com/software-students-spring2025/5-final-404s/actions/workflows/backend.yml/badge.svg?branch=main)](https://github.com/software-students-spring2025/5-final-404s/actions/workflows/backend.yml)

# Team 404s



## Description

A web application that helps users track their daily food intake and receive recommended meals based on what they have eaten. 
Users can enter what they have eaten and we can calculate food nutrition facts and see what nutrient they lack and recommend meals based on that. 
For example if they have had no carbs yet maybe we recommend food options with carbs such as pasta, rice, bread etc.

## Contributors:
[Maya Felix](https://github.com/mxf4596)


[Arkadiuz Mercado](https://github.com/ArionM27)


[Angel Serrano](https://github.com/a-ngels)


[First Last](https://github.com/)

## links to the container images for each custom subsystem, hosted on DockerHub.
https://nutritrack-appmd.ondigitalocean.app/


## instructions for how to set up any environment variables and import any starter data into the database, as necessary, for the system to operate correctly when run.

You will need an API key from https://fdc.nal.usda.gov/api-guide 

Click on "Sign up to obtain a key" 

Navigate here for instructions on how to set up the key: https://api.data.gov/docs/developer-manual/



## Environment Variables

You must create a `.env` file in the `/backend` folder before running the app.  
Use `.env.example` as a guide:



```bash
cp backend/.env.example backend/.env 
```








