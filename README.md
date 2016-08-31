Stock Market Analysis and Prediction
====================================
Stock Market Analysis and Prediction is the project on technical analysis,
visualization and prediction using data provided by NEPSE(Nepal Stock Exchange).
The core objective of this project is to comparitively analyse the effectiveness
of different prediction algorithms on stock market data and provide general
insight on this data to user through visualization. The project encompasses
the concept of Data Mining, Machine Learning and Statistics.

-------------------------------------------------------------------------------

Requirements:
-------------
- python (3.5)
- beautifulsoup4 (4.4.1)
- matplotlib (1.5.1)
- numpy (1.10.4)
- pandas (0.18.1)
- scikit-learn (0.17.1)
- pybrain(0.3.3)
- docopt (0.6.2)
- schema (0.6.2)
- cufflinks (0.8.2)
- plotly (1.12.7)

Install:
--------
### clone the repo
	$ git clone https://github.com/samshara/Stock-Market-Analysis-and-Prediction.git <directory_name>

### To install the required packages  to virtual environment and setup package:
	# pip3 install -r requirements.txt
    # cd <cloned directory>
    # pip install . (install the package locally)
    # pip install -e . (install the package with symlink, so that changes in the sources will be immediately available. *Development Version*

### To run the command line interface:
        $ smap_nepse <command> [options] eg. smap_nepse -h
