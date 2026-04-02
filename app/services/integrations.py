import httpx
import urllib.parse
from app.core.config import settings

async def get_location_integrations(location_name: str, lat: float, lon: float) -> dict:
    integrations = {}
    
    integrations["google_maps_url"] = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

    city_only = location_name.split(',')[0].strip()
    encoded_city = urllib.parse.quote(city_only)

    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&explaintext=true&titles={encoded_city}&format=json"
            
            headers = {
                "User-Agent": "PMA-WeatherApp/1.0 (mailto:name.surname@example.com)"
            }
            
            response = await client.get(wiki_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                pages = data.get("query", {}).get("pages", {})
                
                if pages:
                    first_page = list(pages.values())[0]
                    extract = first_page.get("extract", "").strip()
                    
                    if extract:
                        first_paragraph = extract.split('\n')[0]
                        integrations["wikipedia_summary"] = first_paragraph
                    else:
                        integrations["wikipedia_summary"] = f"Wikipedia could not find an exact summary for {city_only}."
                else:
                    integrations["wikipedia_summary"] = f"Wikipedia could not find an exact summary for {city_only}."
            else:
                integrations["wikipedia_summary"] = f"Wikipedia error: {response.status_code}"
    except Exception as e:
        integrations["wikipedia_summary"] = f"Summary unavailable: {str(e)}"

    full_encoded_location = urllib.parse.quote(location_name)
    integrations["youtube_videos"] = []
    
    if settings.YOUTUBE_API_KEY:
        try:
            async with httpx.AsyncClient() as client:
                yt_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=3&q={full_encoded_location}+tourism+tour&type=video&key={settings.YOUTUBE_API_KEY}"
                yt_response = await client.get(yt_url)
                if yt_response.status_code == 200:
                    yt_data = yt_response.json()
                    integrations["youtube_videos"] = [
                        f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                        for item in yt_data.get("items", [])
                    ]
        except Exception:
            pass
    else:
        integrations["youtube_videos"] = [f"https://www.youtube.com/results?search_query=tour+{full_encoded_location}"]

    return integrations