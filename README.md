## DESCRIPTION

This repo contains a series of scripts to download and analyze homework.

## STRUCTURE

In /in files used as input for the scripts. In /out files that are the output of the scripts In /download the downloaded
assignments In /secrets private files like gh tokens In /scripts the availalbe scripts

## SETUP

0) Have ```python 3.0```

1) Install the requirements listed in ```requirements.txt``` with
   ```pip install -r requirements.txt```
2) Write a file ```/in/assignments/{ORG}```.csv with the fields: Assignment (prefix of the assignment repo),Deadline (
   ex: 2022-01-26 10:24)
3) Write a file ```/in/students/{ORG}.csv``` with the following fields (Name,Surname,Email,GitHub ID)
4) Write the github token to be used in ```/secrets/github_token.txt```
5) Set the github ORG to analyse in /config.py

## SCRIPTS

in /scripts:

- download_assignments.py: used to download the repos of all the assignments specified in ```/in/assignments/{ORG}```
- lab_analysis: produces an analysis of the downloaded repos for the selected {ORG}