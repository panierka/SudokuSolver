using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GridSquare : MonoBehaviour
{
    public GameObject number_text;
    private int number_ = 0;

	private void Start()
	{
		
	}

	private void Update()
	{
		
	}

	public void DisplayText()
    {
		if (number_ <= 0)
            number_text.GetComponent<TMPro.TextMeshProUGUI>().text = " ";
        else
			number_text.GetComponent<TMPro.TextMeshProUGUI>().text = number_.ToString();
	}

    public void SetNumber(int number)
    {
        number_ = number;
		DisplayText();
    }
}
