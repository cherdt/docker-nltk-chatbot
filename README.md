ELIZA chatbot Docker image
==========================

Docker container to run the Python NLTK ELIZA chatbot.

How to build
------------

    docker build --tag nltk-chatbot .

How to run
----------

Once built:

    docker run -d -p 9500:9500 nltk-chatbot

How to interact
---------------

Visit http://localhost:9500/chat/


