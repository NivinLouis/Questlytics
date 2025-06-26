from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from datetime import datetime, timezone
import os

from utils.pdf_utils import extract_text_from_pdf
from question_extractor import extract_questions
from frequency_analyzer import rank_questions
from document_generator import create_report
from analysis_llm import analyse_questions

from models import UploadedFile
from database import SessionLocal

router = APIRouter()
MAX_FILE_SIZE_MB = 5


@router.post("/upload-question")
async def upload_question_files(files: List[UploadFile] = File(...)):
    os.makedirs("uploads/questions", exist_ok=True)
    db = SessionLocal()
    results = []

    for file in files:
        # Type check
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail=f"{file.filename} is not a PDF")

        content = await file.read()

        # Size check
        if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"{file.filename} exceeds 5MB")

        # Save the file
        file_path = os.path.join("uploads/questions", file.filename)
        with open(file_path, "wb") as f:
            f.write(content)

        # Extract text
        text = extract_text_from_pdf(file_path)

        # LLM optional analysis
        insights = analyse_questions(text)

        # Extract & rank questions
        questions = extract_questions(text)
        ranked = rank_questions(questions)

        # Generate report
        report_path = create_report(ranked, file.filename)

        # Save to DB
        db_file = UploadedFile(
            filename=file.filename,
            content_type=file.content_type,
            upload_time=datetime.now(timezone.utc)
        )
        db.add(db_file)
        db.commit()

        results.append({
            "filename": file.filename,
            "report": report_path,
            "questions_found": len(questions),
            "llm_summary": insights
        })

    return {"message": "Analysis complete", "results": results}


@router.post("/upload-syllabus")
async def upload_syllabus_files(files: List[UploadFile] = File(...)):
    os.makedirs("uploads/syllabus", exist_ok=True)
    uploaded_files = []

    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail=f"{file.filename} is not a PDF")

        content = await file.read()

        if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"{file.filename} exceeds 5MB")

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        new_filename = f"syllabus_uploaded_on_{timestamp}.pdf"
        save_path = os.path.join("uploads/syllabus", new_filename)

        with open(save_path, "wb") as f:
            f.write(content)

        uploaded_files.append(new_filename)

    return {"message": "Syllabus uploaded successfully", "files": uploaded_files}
