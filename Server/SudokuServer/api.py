import logging
import math

import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import json

import detector
import parser
import solver

app = FastAPI(debug=True)
logger = logging.getLogger('uvicorn.error')


class InnerListModel(BaseModel):
    data: List[int]


class SudokuSolutionModel(BaseModel):
    initialBoardState: List[InnerListModel]
    solvedBoardState: List[InnerListModel]


@app.post("/upload-sudoku/")
async def upload_sudoku(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        np_arr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

        cells = parser.extract_cells(image, 50)
        dim = int(math.sqrt(len(cells)))

        matrix = [
            [detector.detect_digit(cell) for cell in cells[i * dim:(i + 1) * dim]]
            for i in range(dim)
        ]

        solution = solver.solve_sudoku(matrix)

        initial = [InnerListModel(data=row) for row in matrix]
        solved = [InnerListModel(data=row) for row in solution]

        response = SudokuSolutionModel(
            initialBoardState=initial,
            solvedBoardState=solved
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Server error: {str(e)}')


if __name__ == '__main__':
    uvicorn.run(app)
