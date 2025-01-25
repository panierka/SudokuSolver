using Assets.Scripts.Utils;
using Assets.Scripts;
using System.Collections.Generic;
using UnityEngine;

public class ImageDisplay : MonoBehaviour
{
	void Start()
	{
		Texture2D texture = AppFlowDao.Instance.CurrentSentTexture;
		Rect rect = new Rect(0, 0, texture.width, texture.height);
		Vector2 pivot = new Vector2(0.5f, 0.5f);
		GetComponent<SpriteRenderer>().sprite = Sprite.Create(texture, rect, pivot);
	}
}
