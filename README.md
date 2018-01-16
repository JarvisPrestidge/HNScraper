# Hacker News Scraper

![alt text](https://media-exp2.licdn.com/mpr/mpr/shrink_200_200/AAEAAQAAAAAAAAveAAAAJDMzMGU1M2Q0LTA1YWYtNDViZC1hZGIzLTMwYTk2YjgyOTBkYQ.png "Logo Title Text 1")

### Installation 

##### Python 

If you do not have Python installed please make sure you do so. The version required to run this is `2.7`. 

[Installing Python from Scratch](https://wiki.python.org/moin/BeginnersGuide/Download)

After you have done so please verify your version of Python installed via Command Line. Please run the following: 
```
python -V 
```
For example, when I do so `stdout` produces:
```
Python 2.7.10
```
This is a compatible version. The reason for choosing `Python 2` was due to my own experience level. There are notable improvements in `Python 3` but since this is a small development exercise, the implications of this choice are negligible.


##### Modules Required 

The following Python modules will need to be installed (via `pip`):

- `requests`
- `lxml` 
- `validators`
- `multiprocessing` 

Standard libraries are used which are: `math`, `json`, `argparse` and `unittest`. They should be installed with your distribution of Python. 

We are going to use a package management system called `pip`. First we need to install it by running the following:
```
easy_install pip 
```
If you run into issues with privileges then append the `sudo` command:
```
sudo easy_install pip
```
After which we should be able to install the following modules:
```
sudo pip install <module name> 
```
Or you can give it a file which includes all the packages required:
```
sudo pip install -r <requirement file> 
```

### Usage

##### Options (Command Line Arguments)

- `--posts [n] `, `-p [n]`  : Number of Posts to be Scraped
- `--multi [n] `, `-m [n]` : Number of Processes to be Used
- `--indent[n] `, `-i [n]` : Indentation Level for JSON Output 

N.B. In all cases `[n]` must be an integer, for number of posts (`--posts`) this number should be between `0` and `MAX_POSTS`. 

`MAX_POSTS` can be amended within the code only. It has been set to `200`, this can be increased to better test `multiprocessing` and thus the scalability. However, this is a simplistic use of multiple processes rather than sophisticated concurrency.

##### Expected Behaviour and Defaults 

- Number of posts has been capped to `200` 
- Process count has been capped to `20` 
- Indentation level has been capped to `10` 
- If you exceed these values it will raise an ArgumentTypeError
- They can only be amended via a code change 
- If you pass no arguments the default values will be used 
- Defaults : `--posts [100]`, `--multi[0]`, `--indent[4]`

##### Example usage  
```
python hnScraper.py --posts 200 -m 4 -i 2 
```
Unit Tests take no arguments therefore we simple run the script :
```
python testHNScraper.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

### Library Choice 

##### `requests`
- `requests` is a simple and efficient `HTTP` library and supports RESTful `API`. 
- There is no need to use `urllib2` since we only need to make a `GET` request.
- It also takes care of decoding the response into Unicode automatically.

##### `lxml`
- `lxml` is a high performance, production quality XML library.
-  `lxml` has considerable better performance over other libraries such as `BeautifulSoup` which means this solution is scalable. 
-  There is a caveat that the source should be expected have good structure otherwise `BeautifulSoup` may be a better choice. 
-  Since we know the source is well structured, to improve performance `lxml` has been selected. 
-   As previously mentioned it's fast, easy to use and has a variety of features.

##### `validators`
- There are better options for URL validation such as those contained in `django`
- The reason for this choice was due to ease of use. 
- In terms of URL validation it is probably better to design your own. 

##### `multiprocessing` 
- `multiprocessing` module is easier to integrate into code.
- This is a simplistic attempt to increase speed via multiple processes. 
- If we needed to increase speed dramatically this is not the best module.
