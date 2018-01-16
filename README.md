# Hacker News Scraper

![alt text](https://media-exp2.licdn.com/mpr/mpr/shrink_200_200/AAEAAQAAAAAAAAveAAAAJDMzMGU1M2Q0LTA1YWYtNDViZC1hZGIzLTMwYTk2YjgyOTBkYQ.png "TrueLayer Logo")

### Installation 


### Usage

##### Options (Command Line Arguments)

- `--posts [n] `, `-p [n]`  : Number of Posts to be Scraped
- `--multi [n] `, `-m [n]` : Number of Threads to be Used
- `--indent[n] `, `-i [n]` : Indentation Level for JSON Output 

N.B. In all cases `[n]` must be an integer, for number of posts (`--posts`) this number should be between `0` and `MAX_POSTS`. 

`MAX_POSTS` can be amended within the code only. It has been set to `200`, this can be increased to better test multithreading and thus the scalability.

##### Expected Behaviour and Defaults 

- If you pass `--posts [n]` > `MAX_POSTS` it will raise a ValueError. 
- Thread count has been capped to `20` 
- Indentation level has been capped to `10` 
- If you pass no arguments the default values will be used 
- Defaults : `--posts [100]`, `--multi[0]`, `--indent[4]`



