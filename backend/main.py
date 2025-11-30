from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
from datetime import datetime
from database import get_db
from vision_pipeline import robust_inventory_pipeline, ImageQualityError, LowConfidenceError
from models import InventoryExtractionResult

app = FastAPI(title="Visual Inventory Manager API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload", response_model=InventoryExtractionResult)
async def upload_image(file: UploadFile = File(...), db = Depends(get_db)):
    # 1. Save file locally
    file_extension = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Create Scan Event Record
    scan_id = str(uuid.uuid4())
    scan_data = {
        "id": scan_id,
        "image_url": file_path,
        "status": "PENDING",
        "scan_timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        db.table("scan_events").insert(scan_data).execute()
    except Exception as e:
        print(f"DB Error: {e}")
        # Continue even if DB fails, to show result to user? No, better to fail.
        # But for now let's assume it works or we just log it.
        pass

    try:
        # 3. Process Image
        result = robust_inventory_pipeline(file_path)
        
        # 4. Update Scan Event
        db.table("scan_events").update({
            "status": "PROCESSED",
            "confidence_score": result.confidence_score,
            "raw_llm_response": result.model_dump(mode='json')
        }).eq("id", scan_id).execute()

        # 5. Save Items
        items_data = []
        for item in result.items:
            items_data.append({
                "scan_id": scan_id,
                "item_name": item.item_name,
                "category": item.category,
                "quantity": item.quantity,
                "unit": item.unit,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
                "detected_at": datetime.utcnow().isoformat()
            })
        
        if items_data:
            db.table("inventory_items").insert(items_data).execute()
        
        return result

    except ImageQualityError as e:
        db.table("scan_events").update({
            "status": "FAILED",
            "metadata_info": {"error": str(e)}
        }).eq("id", scan_id).execute()
        raise HTTPException(status_code=400, detail=str(e))
    except LowConfidenceError as e:
        db.table("scan_events").update({
            "status": "FAILED",
            "metadata_info": {"error": str(e)}
        }).eq("id", scan_id).execute()
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # db.table("scan_events").update({
        #     "status": "FAILED",
        #     "metadata_info": {"error": str(e)}
        # }).eq("id", scan_id).execute()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/scans")
def get_scans(db = Depends(get_db)):
    response = db.table("scan_events").select("*").execute()
    return response.data

@app.get("/inventory")
def get_inventory(db = Depends(get_db)):
    response = db.table("inventory_items").select("*").execute()
    return response.data
