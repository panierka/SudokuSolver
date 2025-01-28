using UnityEngine;
using UnityEngine.SceneManagement;

public class MainTransitionHandler : MonoBehaviour
{
	public void TransitionToMain()
	{
		SceneManager.LoadScene("Main");
	}
}
