from fastapi import APIRouter, WebSocket, HTTPException
from services.proctor_service import ProctorService
from fastapi.responses import JSONResponse
import asyncio

router = APIRouter()
proctor_service = ProctorService()

@router.post("/proctor/start/{candidate_id}")
async def start_proctoring(candidate_id: str):
    """Start proctoring session"""
    if not proctor_service.initialize_cameras():
        raise HTTPException(status_code=500, detail="Failed to initialize cameras")
    
    success = proctor_service.start_proctoring(candidate_id)
    if not success:
        raise HTTPException(status_code=400, detail="Proctoring session already active")
    
    return {"status": "success", "message": "Proctoring started"}

@router.post("/proctor/stop")
async def stop_proctoring():
    """Stop proctoring session"""
    proctor_service.stop_proctoring()
    return {"status": "success", "message": "Proctoring stopped"}

@router.websocket("/proctor/ws/{candidate_id}")
async def proctor_websocket(websocket: WebSocket, candidate_id: str):
    """WebSocket connection for real-time proctoring updates"""
    await websocket.accept()
    
    try:
        while proctor_service.is_active:
            # Send proctoring status updates to client
            if proctor_service.warning_count > 0:
                await websocket.send_json({
                    "warning_count": proctor_service.warning_count,
                    "max_warnings": proctor_service.MAX_WARNINGS
                })
            await asyncio.sleep(1)
    except:
        pass
    finally:
        await websocket.close() 