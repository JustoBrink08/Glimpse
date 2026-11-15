# Glimpse API Contract (Frontend <-> Backend)

This document defines the exact handoff between **Joseph (Frontend)** and **Nazar (Backend)**. Do not change function names or dictionary keys without notifying the team.

---

## 1. Master Function Signature
* **File Location:** `Backend/gemini_client.py` (Note capital `B` in `Backend`)
* **Import Statement for `app.py`:** 
  ```python
  from Backend.gemini_client import generate_social_story
