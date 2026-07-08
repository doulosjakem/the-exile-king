using UnityEngine;

/// <summary>
/// Extends input handling with mobile-specific features:
/// pinch-to-zoom, two-finger pan, and tap feedback.
/// Attach this to the same GameObject as PlayerInputHandler.
/// </summary>
public class MobileInputHandler : MonoBehaviour
{
    [Header("Zoom Settings")]
    [SerializeField] private Camera targetCamera;
    [SerializeField] private float zoomSpeed = 0.1f;
    [SerializeField] private float minZoom = 5f;
    [SerializeField] private float maxZoom = 15f;

    [Header("Pan Settings")]
    [SerializeField] private float panSpeed = 0.5f;

    private PlayerInputHandler inputHandler;
    private Vector2 lastTouchPosition;
    private float lastPinchDistance;

    private void Start()
    {
        if (targetCamera == null) targetCamera = Camera.main;
        inputHandler = GetComponent<PlayerInputHandler>();
    }

    private void Update()
    {
        if (targetCamera == null) return;

        // Pinch-to-zoom
        if (Input.touchCount == 2)
        {
            Touch touch0 = Input.GetTouch(0);
            Touch touch1 = Input.GetTouch(1);

            float currentPinchDistance = Vector2.Distance(touch0.position, touch1.position);
            float pinchDelta = currentPinchDistance - lastPinchDistance;

            if (targetCamera.orthographic)
            {
                targetCamera.orthographicSize = Mathf.Clamp(
                    targetCamera.orthographicSize - pinchDelta * zoomSpeed,
                    minZoom, maxZoom);
            }

            lastPinchDistance = currentPinchDistance;
        }
        else
        {
            lastPinchDistance = 0f;
        }

        // Two-finger pan
        if (Input.touchCount == 2)
        {
            Touch touch0 = Input.GetTouch(0);
            Touch touch1 = Input.GetTouch(1);

            if (touch0.phase == TouchPhase.Moved || touch1.phase == TouchPhase.Moved)
            {
                Vector2 delta = (touch0.deltaPosition + touch1.deltaPosition) / 2f;
                Vector3 move = new Vector3(-delta.x, 0f, -delta.y) * panSpeed * Time.deltaTime;
                targetCamera.transform.Translate(move, Space.World);

                // Clamp to grid bounds
                HexGrid grid = FindObjectOfType<HexGrid>();
                if (grid != null)
                {
                    Vector3 pos = targetCamera.transform.position;
                    pos.x = Mathf.Clamp(pos.x, -5f, grid.Width * 1.5f);
                    pos.z = Mathf.Clamp(pos.z, -10f, 5f);
                    targetCamera.transform.position = pos;
                }
            }
        }
    }
}