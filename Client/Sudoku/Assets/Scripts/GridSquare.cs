using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GridSquare : MonoBehaviour
{
	public GameObject image;
	public GameObject number_text;
    private int number_ = 0;
	public Color color = new Color32(125, 125, 125, 255);

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

	public void ChangeBackground()
	{
		image.GetComponent<Image>().color = color;
	}
}
