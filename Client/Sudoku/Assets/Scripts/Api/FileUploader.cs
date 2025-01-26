using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UnityEngine.Networking;
using UnityEngine;

namespace Assets.Scripts.Api
{
    public class FileUploader
    {
        public IEnumerator SendFileToServer<TResponse>(byte[] rawData, string url, Callback<TResponse> callback, Callback<string> fallback)
        {
            Debug.Log(rawData);
            var form = new WWWForm();
            form.AddBinaryData("file", rawData);

            using var request = UnityWebRequest.Post(url, form);
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                var responseText = request.downloadHandler.text;
                var responseObject = JsonUtility.FromJson<TResponse>(responseText);
                callback(responseObject);
            }
            else
            {
                fallback(request.error);
            }
        }
    }
}
