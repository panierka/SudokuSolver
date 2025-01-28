using Assets.Scripts;
using Assets.Scripts.Utils;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SudokuGrid : MonoBehaviour
{
    public int columns = 0;
    public int rows = 0;
    public float square_offset = 0.0f;
    public GameObject grid_square;
    public Vector2 start_position = new Vector2(0.0f, 0.0f);
    public float square_scale = 1.0f;

    private List<GameObject> grid_squares_ = new List<GameObject>();

	void Start()
	{
        if (grid_square.GetComponent<GridSquare>() == null)
            Debug.LogError("This Game Object need to have GridSquare script attached");

        CreateGrid();

        int[,] matrix =
        {
            {5, 3, 0, 0, 7, 0, 0, 0, 0},
            {6, 0, 0, 1, 9, 5, 0, 0, 0},
            {0, 9, 8, 0, 0, 0, 0, 6, 0},
            {8, 0, 0, 0, 6, 0, 0, 0, 3},
            {4, 0, 0, 8, 0, 3, 0, 0, 1},
            {7, 0, 0, 0, 2, 0, 0, 0, 6},
            {0, 6, 0, 0, 0, 0, 2, 8, 0},
            {0, 0, 0, 4, 1, 9, 0, 0, 5},
            {0, 0, 0, 0, 8, 0, 0, 7, 9}
        };

        List<List<int>> t = new() 
        {
            new() {5, 3, 0, 0, 7, 0, 0, 0, 0},
            new() {6, 0, 0, 1, 9, 5, 0, 0, 0},
            new() {0, 9, 8, 0, 0, 0, 0, 6, 0},
            new() {8, 0, 0, 0, 6, 0, 0, 0, 3},
            new() {4, 0, 0, 8, 0, 3, 0, 0, 1},
            new() {7, 0, 0, 0, 2, 0, 0, 0, 6},
            new() {0, 6, 0, 0, 0, 0, 2, 8, 0},
            new() {0, 0, 0, 4, 1, 9, 0, 0, 5},
            new() {0, 0, 0, 0, 8, 0, 0, 7, 9}
        };


		var solution = AppFlowDao.Instance.CurrentSudokuSolution;
        Debug.Log($"solution: {solution}");
        Debug.Log($"initial: {solution.initialBoardState}");
        Debug.Log($"solvder: {solution.solvedBoardState}");

		var mInitial = Array2dUtils.FromList(solution.initialBoardState);
		var mSolved = Array2dUtils.FromList(solution.solvedBoardState);

        // Testing display with static numbers
		//var mInitial = Array2dUtils.FromList(t);
		//var mSolved = Array2dUtils.FromList(t);

		SetGridNumber(mInitial, mSolved);
	}


	private void CreateGrid()
	{
        SpawnGridSquares();
        SetSquaresPositions();
	}

    private void SpawnGridSquares()
    {
        for (int row = 0; row < rows; row++)
        {
            for (int column = 0; column < columns; column++)
            {
                grid_squares_.Add(Instantiate(grid_square) as GameObject);
                grid_squares_[grid_squares_.Count -1].transform.parent = this.transform;
                grid_squares_[grid_squares_.Count - 1].transform.localScale = new Vector3(square_scale, square_scale, square_scale);
			}
        }
    }

	private void SetSquaresPositions()
	{
        var square_rect = grid_squares_[0].GetComponent<RectTransform>();
        Vector2 offset = new Vector2();
        offset.x = square_rect.rect.width * square_rect.transform.localScale.x + square_offset;
		offset.y = square_rect.rect.height * square_rect.transform.localScale.y + square_offset;

        int column_number = 0;
		int row_number = 0;

        foreach (GameObject square in grid_squares_)
        {
            if (column_number +1 > columns)
            {
                row_number++;
                column_number = 0;
            }

            var pos_x_offsett = offset.x * column_number;
            var pos_y_offsett = offset.y * row_number;
            square.GetComponent<RectTransform>().anchoredPosition = new Vector2(start_position.x + pos_x_offsett, start_position.y + pos_y_offsett);
            column_number++;
        }
	}

	private void SetGridNumber(int[,] initialMatrix, int[,] solutionMatrix)
	{
		int rows = solutionMatrix.GetLength(0);
		int cols = solutionMatrix.GetLength(1);
		int index = 0;

		for (int row = 0; row < 9; row++)
		{
			for (int col = 0; col < 9; col++)
			{
				int reversedRow = 8 - row;
				index = reversedRow * 9 + col;
				grid_squares_[index].GetComponent<GridSquare>().SetNumber(solutionMatrix[col, row]);
                if (solutionMatrix[col, row] == initialMatrix[col, row])
                {
                    grid_squares_[index].GetComponent<GridSquare>().ChangeBackground();
                }
            }
		}
		
		// Testing assigning random numbers

		//foreach (var square in grid_squares_)
		//{
		//	square.GetComponent<GridSquare>().SetNumber(Random.Range(0, 10));
		//}
	}
}
