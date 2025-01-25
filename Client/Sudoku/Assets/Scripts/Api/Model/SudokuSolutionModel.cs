using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Assets.Scripts.Api.Model
{
    public class SudokuSolutionModel
    {
        public List<List<int>> InitialBoardState { get; set; }

        public List<List<int>> SolvedBoardState { get; set; }
    }
}
