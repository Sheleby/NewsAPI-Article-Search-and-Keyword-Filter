# NewsAPI Web Project
## Summary
This project is meant to connect my Python API program that connects to NewsAPI and spaCy for collecting news articles and creating a basic keyword list for each article.

## Dev Log
### 9/4/2026
* Created HTML and CSS code for basic layout and essential features that we will later on connect.
* Created Article Selection Section
* Created Keyword Exclusion Section
* Created Table Section
* For Keyword Exclusion list, I managed to finally fix the strange spacing around the keyword and minimize the x button.

#### The following needs work:
1. Add the Sources Selection
    a. any
    b. gaurdian, etc.
2. Add a Keywords text box.
    a. Make default empty
3. Remove the "Remove - Keyword Exclude List" feature
4. Change "Title Table" to something better.
5. Check that keywords stretch properly with the <p> word length.
6. Check that keyword button is clickable.

### 9/10/2026
* Connected Flask Python to start creating live functions within the html
* Created app.py with search()
* Created get_news in news_api.py which takes in all the inputs and creates the url.
* Created keyword_exclusion() in app to provide the exclusion list display in html
* Created keyword_remove() in app which allows keywords to be removed by clicking X button.
* droplist_add and droplist_remove were modified to perform get_droplist within the app for keyword_exclusion display

### 9/11/2026
* Begun integration of Jupyter Notebook code in news_api which processes the input in the app, and then processes the information to create the data. 
    * Integrated get_news with pandas to create dataframe.
    * Provided framework for keyword_filter and create_keyword_list

#### The following needs work: 
1. Need to put failsafe so that a message pops up when no results are found instead of crashing with an error 304 KeyError. 
2. Need to connect create_keyword_list and keyword_filter so keywords populate in the Keywords column in the dataset.
3. When data is fully populating properly, need to display the data with jinjas in the app.


### 9/16/2026
* Fixed keywords to populate for each article
