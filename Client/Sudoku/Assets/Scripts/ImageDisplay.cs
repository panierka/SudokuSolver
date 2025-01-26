using Assets.Scripts.Utils;
using Assets.Scripts;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ImageDisplay : MonoBehaviour
{
	public Image targetImage;
	void Start()
	{
		Texture2D texture = AppFlowDao.Instance.CurrentSentTexture;
		Rect rect = new Rect(0, 0, texture.width, texture.height);
		Vector2 pivot = new Vector2(0.5f, 0.5f);
		targetImage.GetComponent<RectTransform>().sizeDelta = new Vector2(texture.width, texture.height);
		targetImage.sprite = Sprite.Create(texture, rect, pivot);
		Debug.Log($"texture.width: {texture.width}");
		Debug.Log($"texture.height: {texture.height}");
	}
}
