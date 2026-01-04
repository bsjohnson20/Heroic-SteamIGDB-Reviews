# Heroic-SteamIGDB-Reviews

A Python tool that scans your Heroic Games Launcher library (Epic Games) and fetches game reviews and ratings from both IGDB (Internet Game Database) and Steam APIs.


### Note this README was generated using Copilot

The code however is not. The amount of times inline AI suggests something completely stupid is silly.
Or just ignores the code above it that is relevant.



## Overview

This tool automates the process of gathering comprehensive game review data for your Epic Games library.  It reads your Heroic Games Launcher configuration, extracts your game collection, and queries both IGDB and Steam to compile ratings, review scores, and review counts into a convenient CSV file.

## Features

- **Automatic Library Scanning**: Reads your Heroic Games Launcher library automatically
- **Dual API Integration**: Fetches data from both IGDB and Steam for comprehensive coverage
- **Smart Caching**: Uses cachier to cache API responses and avoid rate limiting
- **CSV Export**: Outputs game data to a convenient CSV file for analysis
- **Intelligent Sorting**: Sorts games by number of reviews (descending)
- **Progress Tracking**: Visual progress bar with tqdm
- **Rate Limiting**: Built-in rate limiting for IGDB API (4 calls per second)

## Prerequisites

- Python 3.13 or higher
- Heroic Games Launcher installed with Epic Games library
- IGDB API credentials (requires Twitch Developer account)
- Steam API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bsjohnson20/Heroic-SteamIGDB-Reviews.git
cd Heroic-SteamIGDB-Reviews
```

2. Install dependencies using `uv` (recommended) or `pip`:
```bash
# Using uv
uv sync

# Or using pip
pip install cachier pandas python-dotenv tqdm ftfy loguru ratelimit steam-web-api
```

## Configuration

1. Set up your API credentials by creating a `.env` file in the project root:
   ```
   client_id=your_igdb_client_id
   client_secret=your_igdb_client_secret
   STEAM_KEY=your_steam_api_key
   ```

2. **IGDB Credentials**: 
   - Visit [Twitch Developer Portal](https://dev.twitch.tv/)
   - Register your application to get Client ID and Client Secret

3. **Steam API Key**: 
   - Visit [Steam Web API Key](https://steamcommunity.com/dev/apikey)
   - Generate your API key

4. Ensure your Heroic Games Launcher configuration is accessible at the default location

## Usage

Run the main script: 

```bash
python src/main.py
```

The tool will:
1. Read your Epic Games library from Heroic
2. Query IGDB and Steam APIs for each game
3. Compile the data and sort by number of reviews (highest to lowest)
4. Export results to `games.csv`

### Output Format

The generated CSV includes:
- Game name
- IGDB ID
- Steam review score (0-10)
- Review score description (e.g., "Very Positive")
- Total positive reviews
- Total negative reviews
- Total review count

### Data Sources

- **IGDB**:  Provides game ID, name, rating, and rating count
- **Steam**: Provides review score, review descriptions, and detailed review counts

## Cache Management

To clear the cache and force fresh API calls, modify the `CLEAR_CACHE` variable in `main.py`:

```python
CLEAR_CACHE = True  # Set to True to clear cache
```

## Project Structure

```
Heroic-SteamIGDB-Reviews/
├── src/
│   ├── main.py              # Main application logic
│   └── libs/
│       ├── epiclibrary.py   # Heroic library parser
│       ├── igdb.py          # IGDB API wrapper with rate limiting
│       └── steam. py         # Steam API wrapper
├── pyproject.toml           # Project dependencies
├── . env                     # API credentials (not tracked)
└── README.md
```

## Dependencies

- **cachier**: API response caching
- **pandas**: Data manipulation
- **python-dotenv**: Environment variable management
- **tqdm**: Progress bar display
- **ftfy**: Text encoding fixes
- **loguru**: Enhanced logging
- **ratelimit**:  API rate limiting
- **steam-web-api**: Steam API client

## Logging

The tool uses loguru for logging with INFO level by default.  Modify the log level in `main.py`:

```python
log.add(sys.stderr, level="DEBUG")  # For more verbose output
```

## How It Works

1. **Library Scanning**: Reads your Heroic Games Launcher library file
2. **API Querying**: For each game: 
   - Queries IGDB for game ratings and rating counts
   - Queries Steam for review scores and detailed review statistics
3. **Data Merging**: Combines data from both sources into a single record
4. **Sorting**: Orders games by review count (IGDB `rating_count` or Steam `total_reviews`)
5. **Export**: Writes all data to `games.csv`

## Error Handling

- Games not found on IGDB or Steam will still appear in the output with partial data
- API errors are logged but don't stop the scanning process
- Missing game data is tracked and reported at completion

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

[Add your license here]

## Acknowledgments

- [Heroic Games Launcher](https://heroicgameslauncher.com/)
- [IGDB API](https://www.igdb.com/api)
- [Steam Web API](https://steamcommunity.com/dev)

---

**Note**: This tool is for personal use.  Please respect API rate limits and terms of service for both IGDB and Steam. 