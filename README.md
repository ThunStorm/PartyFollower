# PartyFollower
A lightweight problem auto-answering script for "Beijing Follows the Party" event.

## Description

The project aims to built a software to automatically answer questions in "Beijing Always Follows the Party" event.  

It consists of two scripts `questions-scraper.py ` (used to scrape the question bank) and `quiz-challenger.py` (used to answer the quiz)

Scripts are written in Python3.6 and test with Raspbian

## How to use

1. Clone or download to your PC and install the dependencies via pip

   ```shell
   $ pip install -r requirments.txt
   ```

2. We recommend to run the script background with the tool, for example, "[tmux](https://github.com/tmux/tmux/wiki)" 

   ```shell
   # Ubuntu or Debian
   $ sudo apt install tmux
   
   # CentOS or Fedora
   $ sudo yum install tmux
   
   # Mac
   $ brew install tmux
   ```

3. Create a new session in **tmux** and run scripts in the session

   ```shell
   # Read tmux wiki for more
   $ tmux 
   
   # if the data folder is not downloaded, run "python3 questions-scraper.py" first.
   $ python3 quiz-challenger.py [With your customised configurations, usage see -h]
   ```

   usage: quiz-challenger.py [-h] [--phone_number PHONE_NUMBER]
                             [--interval_sec INTERVAL_SEC] [--rounds ROUNDS]
                             [--daily_challenge] [--time TIME]

   optional arguments:
     -h, --help            show this help message and exit
     --phone_number PHONE_NUMBER
                           Input your phone number.
     --interval_sec INTERVAL_SEC
                           Input the interval between two attempts.
     --rounds ROUNDS       Input how many rounds in sum you would like to pass.
     --daily_challenge     Use to do daily challenge.
     --time TIME           Set up the time you expect to do quiz every day.

   

4.  Detach the session and attach it when you need in the future

    ```shell
      # Detach the session
      $ tmux detach
   
      # Check the session name and attach it again
      $ tmux ls
      $ tmux attach -t [name of the session]
   ```

## Coda

It is nice to start this project. I learned a lot about the history of the CCP during coding it. These scripts are for those who love coding and would like to learn more about history.

