# News Aggregator

A simple and efficient news aggregator built using Python.

## Description

This project aims to aggregate news from various sources, providing users with a centralized platform to access the latest news updates.

## Features

- **Aggregation**: Collects news from multiple sources.
- **Filtering**: Allows users to filter news based on categories or keywords.
- **Responsive Design**: Adaptable to various screen sizes for optimal viewing.
- **Base Command Integration**: Seamlessly integrates with Django's management command system for custom command creation.
- **Dynamic News Item Creation**: Capable of creating or updating news items as they become available.
- **Web Scraping Capabilities**: Efficiently fetches and parses content from various websites.
- **Date Normalization**: Converts date strings into a Django-compatible format.
- **Concurrent Fetching**: Uses `ThreadPoolExecutor` for fetching multiple feeds simultaneously, ensuring faster performance.
- **Website Specific Logic**: Tailored logic for various prominent websites to handle each feed's unique structure.

## Screenshots of the News Aggregator in action!
<img width="1440" alt="Screenshot 2023-08-17 at 1 02 25 AM" src="https://github.com/MAA8007/News_aggregator/assets/106858270/7215ba7e-40d3-47f5-8c30-b35ffa5c98c0">
<img width="1440" alt="Screenshot 2023-08-17 at 1 03 09 AM" src="https://github.com/MAA8007/News_aggregator/assets/106858270/f06a7e83-fb65-4c7c-80ec-81b26f0c137f">
<img width="1440" alt="Screenshot 2023-08-17 at 1 03 13 AM" src="https://github.com/MAA8007/News_aggregator/assets/106858270/eff489b4-f775-4c23-a9c7-ac543f007e8d">


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MAA8007/News_aggregator.git
   ```

2. Navigate to the project directory:
   ```bash
   cd News_aggregator
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Open a web browser and navigate to `http://localhost:8000/`.
2. Browse through the aggregated news or use the filters to narrow down your search.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
