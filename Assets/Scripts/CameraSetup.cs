using UnityEngine;

public class CameraSetup : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private HexGrid grid;

    [Header("Camera Settings")]
    [SerializeField] private float zoomLevel = 8f;
    [SerializeField] private float angle = 45f;
    [SerializeField] private Vector3 offset = new Vector3(3f, 0f, -1f);

    private void Start()
    {
        Camera cam = Camera.main;
        if (cam == null) return;

        if (grid == null) grid = FindObjectOfType<HexGrid>();

        // Set orthographic
        cam.orthographic = true;
        cam.orthographicSize = zoomLevel;

        // Position camera to center on grid
        Vector3 gridCenter = Vector3.zero;
        if (grid != null)
        {
            HexCoord centerCoord = new HexCoord(grid.Width / 2, grid.Height / 2);
            gridCenter = grid.HexToWorldPosition(centerCoord);
        }

        // Isometric angle
        cam.transform.position = gridCenter + new Vector3(0f, Mathf.Tan(angle * Mathf.Deg2Rad) * zoomLevel, -zoomLevel) + offset;
        cam.transform.rotation = Quaternion.Euler(angle, 0f, 0f);
    }
}