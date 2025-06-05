# Chatbot for checking Alexa skills

## Installation
You will need to install the python openAI library. Selenium should already be instulled, but if it is not, do that too.

```
pip install openai
```

## OpenAI Setup
You will need an openAI account. Set up a project and get an API key.

The model is currently set to gpt-4.0. If you want a cheaper option, choose gpt-4.0-mini. It is rate limited and cannot
handle parallel instances.

## Amazon Setup
You will need a developer account, with username, password, and the url to the developer portal set. You
may have to start a skill to access the dev portal.

## Running the project
Make sure you have invocations in the same directory, and there are no collisions with output.

Run 
```
python3 main.py 
```

If you want to run in parallel, you can specifiy category and then starting letter as input args.
This prevents multiple instances from running on the same skills, leading to race conditions or
inefficeincy.  All 3 patterns are supported.

```
python3 main.py
python3 main.py CategoryName
python3 main.py CategoryName A
```

If too many parallel instances are run, the chatbot may crash. Also, some skills freeze indefinitely (5 or so in our run.)
Kill the Chrome windows and delete these skill invocations, or it may freeze Chrome and possibly overheat your machine.

## Analysis Tools

There are 3 folders with analysis tools, one for resource analysis, one for content analysis, and one for performance analysis.
Each contains python analysis files. All are self contained, although you may need to install boto3.

Also included is sanitized result data.