import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import json

import parser

app = FastAPI()


class SudokuSolutionModel(BaseModel):
    InitialBoardState: List[List[int]]
    SolvedBoardState: List[List[int]]


@app.post("/upload-sudoku/")
async def upload_sudoku(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        np_arr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # ...

        i_placeholder = [[((i + j) % 9) + 1 if (i + 9) % 2 else 0 for j in range(9)] for i in range(9)]
        s_placeholder = [[((i + j) % 9) + 1 for j in range(9)] for i in range(9)]
        response = SudokuSolutionModel(
            InitialBoardState=i_placeholder,
            SolvedBoardState=s_placeholder
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Server error: {str(e)}')
