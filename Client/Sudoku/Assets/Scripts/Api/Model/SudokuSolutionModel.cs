using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Assets.Scripts.Api.Model
{
    [Serializable]
    public class SudokuSolutionModel
    {
        public List<InnerList> initialBoardState;

        public List<InnerList> solvedBoardState;
    }

    [Serializable]
    public class InnerList
    {
        public List<int> data;
    }
}
