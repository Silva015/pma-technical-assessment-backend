from fastapi import FastAPI
from app.routers import weather, export

description = """
**Welcome to the Weather App API!** 🌍☀️

This API was developed by **Arthur Silva Carneiro** as part of a Technical Assessment and provides a complete system for managing weather data with third-party integrations.

### Key Features:
* **Weather CRUD:** Create, read, update, and delete temperature histories for any location.
* **Intelligent Validation:** The system validates date ranges and verifies location existence via geocoding.
* **API Integrations:** Each search automatically generates:
  * 📍 An exact **Google Maps** link.
  * 📖 A clean historical/cultural summary from **Wikipedia**.
  * 🎥 Tourism search links for **YouTube**.
* **Data Export:** Download the entire database in `JSON`, `CSV`, or `Markdown` formats.

---

### About the Product Manager Accelerator

The Product Manager Accelerator Program is designed to support PM professionals through every stage of their careers. From students looking for entry-level jobs to Directors looking to take on a leadership role, the program has helped over hundreds of students fulfill their career aspirations.

The Product Manager Accelerator community is ambitious and committed. Through the program they have learnt, honed and developed new PM and leadership skills, giving them a strong foundation for their future endeavors.

Here are examples of services they offer. Check out their website to learn more about their services:

🚀 **PMA Pro**
End-to-end product manager job hunting program that helps you master FAANG-level Product Management skills, conduct unlimited mock interviews, and gain job referrals through their largest alumni network. 25% of their offers came from tier 1 companies and get paid as high as $800K/year.

🚀 **AI PM Bootcamp**
Gain hands-on AI Product Management skills by building a real-life AI product with a team of AI Engineers, data scientists, and designers. They will also help you launch your product with real user engagement using their 100,000+ PM community and social media channels.

🚀 **PMA Power Skills**
Designed for existing product managers to sharpen their product management skills, leadership skills, and executive presentation skills.

🚀 **PMA Leader**
They help you accelerate your product management career, get promoted to Director and product executive levels, and win in the board room.

🚀 **1:1 Resume Review**
They help you rewrite your killer product manager resume to stand out from the crowd, with an interview guarantee.

Get started by using their FREE killer PM resume template used by over 14,000 product managers: https://www.drnancyli.com/pmresume

🚀 They also publish over 500+ free training and courses. Please go to Dr. Nancy Li's YouTube channel https://www.youtube.com/c/drnancyli and Instagram @drnancyli to start learning for free today.
"""

app = FastAPI(
    title="Weather App API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Arthur Silva Carneiro",
        "url": "https://www.linkedin.com/in/arthur-carneiro-7b0538234/",
    }
)

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "API is up and running!"}

app.include_router(weather.router)
app.include_router(export.router)