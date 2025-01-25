using Assets.Scripts.Api.Model;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Assets.Scripts.Handlers
{
    public class SceneTransitionHandler : MonoBehaviour
    {
        public void TransitionToAwaiting(Texture2D texture)
        {
            AppFlowDao.Instance.CurrentSentTexture = texture;
            SceneManager.LoadScene("Waiting");
        }

        public void TransitionToSolution(SudokuSolutionModel solution)
        {
            AppFlowDao.Instance.CurrentSudokuSolution = solution;
            StartCoroutine(
                DelayedCall(() => SceneManager.LoadScene("SolutionScene"), 2f)
            );
        }

        private IEnumerator DelayedCall(Action action, float delay)
        {
            yield return new WaitForSeconds(delay);
            action();
        }
    }
}
