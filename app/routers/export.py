from fastapi import APIRouter, HTTPException, Response
from enum import Enum
import json
import csv
import io
from app.core.database import weather_collection

router = APIRouter(prefix="/export", tags=["Data Export"])

class ExportFormat(str, Enum):
    json = "json"
    csv = "csv"
    markdown = "markdown"
    
@router.get(
    "/{format}",
    summary="Export the Weather Database",
    description="Downloads the entire database into your preferred chosen format. **Supported output formats:**\n- `json`\n- `csv`\n- `markdown`\n\nThe markdown output provides a clear, visually pleasing document perfect for reading."
)
async def export_data(format: ExportFormat):
    cursor = weather_collection.find({})
    records = await cursor.to_list(length=1000)

    if not records:
        raise HTTPException(status_code=404, detail="There are no records to export.")

    for record in records:
        record["_id"] = str(record["_id"])

    # ==========================================
    # 1. Export as JSON
    # ==========================================
    if format.value == "json":
        json_data = json.dumps(records, default=str, ensure_ascii=False, indent=2)
        return Response(
            content=json_data, 
            media_type="application/json", 
            headers={"Content-Disposition": "attachment; filename=weather_data.json"}
        )

    # ==========================================
    # 2. Export as CSV
    # ==========================================
    elif format.value == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["ID", "Location", "Start Date", "End Date", "Temperatures (JSON)", "Integrations (JSON)"])
        
        for r in records:
            writer.writerow([
                r.get("_id"),
                r.get("location"),
                r.get("start_date"),
                r.get("end_date"),
                json.dumps(r.get("temperatures", []), ensure_ascii=False),
                json.dumps(r.get("integrations", {}), ensure_ascii=False)
            ])
        
        return Response(
            content=output.getvalue(), 
            media_type="text/csv", 
            headers={"Content-Disposition": "attachment; filename=weather_data.csv"}
        )

    # ==========================================
    # 3. Export as MARKDOWN
    # ==========================================
    elif format.value == "markdown":
        md_content = "# Weather Data Export\n\n"
        
        for r in records:
            md_content += f"## Location: {r.get('location')}\n"
            md_content += f"- **Record ID:** {r.get('_id')}\n"
            md_content += f"- **Period:** {r.get('start_date')} to {r.get('end_date')}\n\n"
            
            md_content += "### Temperatures\n"
            for t in r.get("temperatures", []):
                md_content += f"- **{t['date']}:** {t['temp_celsius']}°C\n"
            
            integ = r.get("integrations", {})
            md_content += "\n### Extra Integrations\n"
            md_content += f"- [Open in Google Maps]({integ.get('google_maps_url', '')})\n"
            md_content += f"- **History:** {integ.get('wikipedia_summary', 'N/A')}\n"
            
            youtube_links = integ.get('youtube_videos', [])
            if youtube_links:
                md_content += "- **Videos / YouTube Search:**\n"
                for link in youtube_links:
                    md_content += f"  - [Access YouTube link]({link})\n"
                    
            md_content += "\n---\n\n"
            
        return Response(
            content=md_content, 
            media_type="text/markdown", 
            headers={"Content-Disposition": "attachment; filename=weather_data.md"}
        )