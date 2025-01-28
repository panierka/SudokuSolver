using Assets.Scripts.Api.Model;
using Assets.Scripts.Utils;
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
            Debug.Log("transition to awaiting");
            AppFlowDao.Instance.CurrentSentTexture = texture;
            CoroutineHost.Instance.StartCoroutine(
                DelayedCall(() => SceneManager.LoadScene("Waiting"), 0.5f)
            );
        }

        public void TransitionToSolution(SudokuSolutionModel solution)
        {
            Debug.Log("transition to solution");
            AppFlowDao.Instance.CurrentSudokuSolution = solution;
            CoroutineHost.Instance.StartCoroutine(
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
