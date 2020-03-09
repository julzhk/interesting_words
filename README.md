TASK
----
* We’ve attached a few documents, each of which has lots of words and sentences. 
* Produce a list of the most frequent interesting words, along with a summary table showing where those words appear 
(sentences and documents). 

* This task can be tackled in any way you feel best solves the problem; 
feel free to show off your prowess! 


HOW TO INSTALL
----
* This script is a standard python 3.8 script. Using virtual env is recommended.
* Install using pip:
 
``` 
pip install -r requirements.txt
```

Install the necessary text corpus:

```
python -m textblob.download_corpora
```

run in the standard way:
```
python word_counter.py

```