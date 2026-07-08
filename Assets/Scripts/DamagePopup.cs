using UnityEngine;
using UnityEngine.UI;

public class DamagePopup : MonoBehaviour
{
    [Header("Settings")]
    [SerializeField] private float popupDuration = 1.0f;
    [SerializeField] private float floatSpeed = 1.0f;
    [SerializeField] private Color damageColor = Color.red;
    [SerializeField] private Color healColor = Color.green;

    private Camera mainCamera;

    private void Start()
    {
        mainCamera = Camera.main;
    }

    public void ShowDamage(int amount, Vector3 worldPosition)
    {
        GameObject popupObj = CreatePopupObject(worldPosition);
        Text text = popupObj.GetComponent<Text>();
        text.text = $"-{amount}";
        text.color = damageColor;
        text.fontSize = 28;

        Destroy(popupObj, popupDuration);
    }

    public void ShowHeal(int amount, Vector3 worldPosition)
    {
        GameObject popupObj = CreatePopupObject(worldPosition);
        Text text = popupObj.GetComponent<Text>();
        text.text = $"+{amount}";
        text.color = healColor;
        text.fontSize = 24;

        Destroy(popupObj, popupDuration);
    }

    public void ShowText(string message, Vector3 worldPosition, Color color)
    {
        GameObject popupObj = CreatePopupObject(worldPosition);
        Text text = popupObj.GetComponent<Text>();
        text.text = message;
        text.color = color;
        text.fontSize = 20;

        Destroy(popupObj, popupDuration);
    }

    private GameObject CreatePopupObject(Vector3 worldPosition)
    {
        GameObject canvas = GameObject.Find("GameCanvas");
        if (canvas == null)
        {
            canvas = new GameObject("GameCanvas");
            Canvas c = canvas.AddComponent<Canvas>();
            c.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.AddComponent<CanvasScaler>();
            canvas.AddComponent<GraphicRaycaster>();
        }

        GameObject popupObj = new GameObject("DamagePopup");
        popupObj.transform.SetParent(canvas.transform, false);

        Text text = popupObj.AddComponent<Text>();
        text.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
        text.alignment = TextAnchor.MiddleCenter;
        text.fontSize = 28;
        text.color = damageColor;

        // Convert world position to screen position
        if (mainCamera == null) mainCamera = Camera.main;
        Vector3 screenPos = mainCamera.WorldToScreenPoint(worldPosition);
        RectTransform rect = popupObj.GetComponent<RectTransform>();
        rect.anchorMin = new Vector2(0, 0);
        rect.anchorMax = new Vector2(0, 0);
        rect.anchoredPosition = new Vector2(screenPos.x, screenPos.y);
        rect.sizeDelta = new Vector2(100, 40);

        // Add floating animation
        FloatUpAnimation anim = popupObj.AddComponent<FloatUpAnimation>();
        anim.floatSpeed = floatSpeed;

        return popupObj;
    }
}

public class FloatUpAnimation : MonoBehaviour
{
    public float floatSpeed = 1.0f;
    private RectTransform rect;

    private void Start()
    {
        rect = GetComponent<RectTransform>();
    }

    private void Update()
    {
        if (rect != null)
        {
            rect.anchoredPosition += new Vector2(0, floatSpeed * Time.deltaTime * 50f);
        }
    }
}