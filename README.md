# EasyScraper

EasyScraper is a Python tool for scraping business information from [https://easy.co.il](https://easy.co.il). It uses Selenium for web scraping and Pandas for data manipulation. The tool allows you to specify categories and cities to scrape business details and saves the results in a CSV file.

In the upcoming video, you'll observe the script's functionality to capture a Captcha at any given moment during execution. This allows the user to solve the Captcha, and the script seamlessly resumes from the same point without any issues.
[CLICK HERE TO SEE THE VIDEO](https://www.veed.io/view/3c4eb7ae-22d5-4743-bfd8-7b34b299072f?panel=share)

## Prerequisites

Before running EasyScraper, make sure you have the following installed:

- Python 3
- ChromeDriver
- Selenium
- Pandas

Install the required Python packages using:

```bash
pip install selenium pandas
```

Also, download the appropriate version of ChromeDriver from [https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/) and ensure it's in your system's PATH.

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/easyscraper.git
cd easyscraper
```

2. Set up virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```

3. Install project dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Edit `search_quaries/categories` and `search_quaries/cities.txt` with the desired categories and cities.

2. Run the scraper:

```bash
python scraper.py
```

The tool will scrape business information based on the specified categories and cities, saving the results in `database.csv`.

## Configuration

Adjust the settings in the `scraper.py` file to customize the scraping behavior. You can modify the scraping delay, adjust the Chrome options, or enhance error handling.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Daniel-Ziv/easyscraper/blob/main/LICENSE) file for details.

## Acknowledgments

- Thanks to the contributors of Selenium and Pandas for their excellent tools.

