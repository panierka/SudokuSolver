using Assets.Scripts.Api.Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;

namespace Assets.Scripts
{
    public class AppFlowDao
    {
        public SudokuSolutionModel CurrentSudokuSolution { get; set; }

        public Texture2D CurrentSentTexture { get; set; }

        private static AppFlowDao instance;

        public static AppFlowDao Instance => instance ??= new();

        private AppFlowDao()
        {

        }
    }
}
