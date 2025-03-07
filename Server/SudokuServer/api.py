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
import file_parser
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

        cells = file_parser.extract_cells(image, 50)
        dim = int(math.sqrt(len(cells)))

        def classify(cell):
            if file_parser.detect_empty(cell):
                return 0
            else:
                return detector.detect_digit(cell)

        matrix = [
            [classify(cell) for cell in cells[i * dim:(i + 1) * dim]]
            for i in range(dim)
        ]

        initial = [InnerListModel(data=list(row)) for row in matrix]
        solution = solver.solve_sudoku(matrix)
        if solution:
            solved = [InnerListModel(data=row) for row in solution]
        else:
            solved = initial

        response = SudokuSolutionModel(
            initialBoardState=initial,
            solvedBoardState=solved
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Server error: {str(e)}')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
