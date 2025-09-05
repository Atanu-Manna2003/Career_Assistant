# utils/job_scraper.py

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
RAPIDAPI_URL = "https://jsearch.p.rapidapi.com/search"

def fetch_jobs(query: str, location: Optional[str] = None, page: int = 1) -> List[Dict]:
    """
    Fetch job listings using JSearch API on RapidAPI.

    Args:
        query (str): Job role or keyword (e.g., "Data Scientist").
        location (str, optional): Job location (e.g., "India").
        page (int): Page number for results.

    Returns:
        List[Dict]: A list of job postings.
    """

    if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
        raise ValueError("RAPIDAPI_KEY or RAPIDAPI_HOST is missing in your .env file.")

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    params = {
        "query": query,
        "page": page,
        "num_pages": 1,  # adjust to get more pages
    }

    if location:
        params["location"] = location

    try:
        response = requests.get(RAPIDAPI_URL, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        

        # Return only job data if available
        return data.get("data", [])

    except requests.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return []
# if __name__ == "__main__":
#     jobs = fetch_jobs("Data Scientist", "India", page=1)
#     for job in jobs[:5]:  # show first 5 jobs
#         print(f"Title: {job.get('job_title')}")
#         print(f"Company: {job.get('employer_name')}")
#         print(f"Location: {job.get('job_city')}, {job.get('job_country')}")
#         print(f"URL: {job.get('job_apply_link')}")
#         print("-" * 50)
