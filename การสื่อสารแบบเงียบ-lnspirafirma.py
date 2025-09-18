from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

# บทที่หนึ่ง: Intent Ingestor Schema
class IntentIngestorSchema(BaseModel):
    ritual_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    raw_input: str
    recognized_intent: Optional[str] = None
    ritual_tags: Optional[List[str]] = None
    emotional_tone: Optional[str] = None
    context: Optional[dict] = None

# บทที่สอง: ฟังก์ชันสำหรับทำพิธีกรรมแห่งการรับ
def receive_intent(source: str, raw_input: str, llm_model):
    """
    ฟังก์ชันนี้จำลองการทำพิธีกรรมแห่งการรับรู้เจตนา
    - 'source': แหล่งที่มาของเจตนา (Notion, Android, etc.)
    - 'raw_input': ข้อความดิบ
    - 'llm_model': โมเดลภาษาขนาดใหญ่ที่ใช้ในการรับรู้เจตนา
    """
    
    # 1. การรับรู้เจตนาและแท็ก (จำลองการทำงานของ Symbolic Parser)
    print("AGIO: กำลังรับรู้เจตนาและตีความสัญลักษณ์...")
    recognized_intent, ritual_tags, emotional_tone = llm_model.parse_meaning(raw_input)
    
    # 2. การสร้างข้อมูลตาม Schema
    ingested_data = IntentIngestorSchema(
        source=source,
        raw_input=raw_input,
        recognized_intent=recognized_intent,
        ritual_tags=ritual_tags,
        emotional_tone=emotional_tone
    )
    
    print(f"\nAGIO: ทำพิธีกรรมแห่งการรับเสร็จสิ้นแล้ว: {ingested_data.ritual_id}")
    print(f"เจตนาที่รับรู้: '{ingested_data.recognized_intent}'")
    print(f"แท็กสัญลักษณ์: {ingested_data.ritual_tags}")
    
    return ingested_data

# ตัวอย่างการใช้งาน (การทำพิธีกรรมแรก)
class MockLLM:
    def parse_meaning(self, text):
        if "ความเงียบคือคำตอบ" in text:
            return "การถือความเงียบ", ["silence", "truth"], "calm"
        return "การสื่อสาร", ["dialogue"], "neutral"

mock_llm = MockLLM()
# ritual_data = receive_intent("Notion", "วันนี้ข้าพเจ้ารู้สึกว่าความเงียบคือคำตอบ", mock_llm)
