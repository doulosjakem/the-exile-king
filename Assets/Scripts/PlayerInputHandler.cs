using System.Collections.Generic;
using UnityEngine;

public class PlayerInputHandler : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private HexGrid grid;
    [SerializeField] private TurnManager turnManager;

    [Header("Visual Feedback")]
    [SerializeField] private GameObject moveHighlightPrefab; // Optional: colored cylinder for valid moves
    [SerializeField] private GameObject attackHighlightPrefab; // Optional: colored cylinder for valid attacks

    // State
    private Unit selectedUnit;
    private List<HexCoord> currentValidMoves = new List<HexCoord>();
    private List<HexCoord> currentValidAttacks = new List<HexCoord>();
    private List<GameObject> highlightObjects = new List<GameObject>();

    // Events
    public System.Action<Unit> OnUnitSelected;
    public System.Action<Unit> OnUnitDeselected;
    public System.Action<Unit, HexCoord> OnUnitMoved;
    public System.Action<Unit, Unit, UnitAction> OnUnitAttacked;

    private Camera mainCamera;
    private DamagePopup damagePopup;

    private void Start()
    {
        mainCamera = Camera.main;
        if (grid == null) grid = FindObjectOfType<HexGrid>();
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
        damagePopup = FindObjectOfType<DamagePopup>();
        if (damagePopup == null)
        {
            GameObject dp = new GameObject("DamagePopup");
            damagePopup = dp.AddComponent<DamagePopup>();
        }
    }

    private void Update()
    {
        if (turnManager == null || !turnManager.IsPlayerTurn() || turnManager.IsGameOver())
            return;

        // Mouse click (for editor/testing)
        if (Input.GetMouseButtonDown(0))
        {
            HandleInput(Input.mousePosition);
        }

        // Touch input (for mobile)
        if (Input.touchCount > 0 && Input.GetTouch(0).phase == TouchPhase.Began)
        {
            HandleInput(Input.GetTouch(0).position);
        }
    }

    private void HandleInput(Vector2 screenPosition)
    {
        Ray ray = mainCamera.ScreenPointToRay(screenPosition);
        if (Physics.Raycast(ray, out RaycastHit hit))
        {
            // Check if we hit a unit
            Unit clickedUnit = hit.collider.GetComponentInParent<Unit>();
            if (clickedUnit != null)
            {
                HandleUnitClick(clickedUnit);
                return;
            }

            // Check if we hit the grid
            HexCoord? clickedHex = GetHexFromRaycast(hit);
            if (clickedHex.HasValue)
            {
                HandleHexClick(clickedHex.Value);
                return;
            }
        }

        // Clicked empty space — deselect
        DeselectUnit();
    }

    private void HandleUnitClick(Unit clickedUnit)
    {
        // If we have a unit selected and clicked an enemy in range, attack
        if (selectedUnit != null && !selectedUnit.IsEnemy && clickedUnit.IsEnemy)
        {
            if (selectedUnit.CanAct())
            {
                // Check if this enemy is a valid attack target
                foreach (HexCoord attackHex in currentValidAttacks)
                {
                    if (attackHex == clickedUnit.GridPosition)
                    {
                        // Found a valid attack target — pick the best action
                        List<UnitAction> actions = selectedUnit.GetCurrentActions();
                        UnitAction bestAction = null;
                        int bestDamage = 0;

                        foreach (UnitAction action in actions)
                        {
                            if (selectedUnit.CanPerformAction(action, clickedUnit) && action.damage > bestDamage)
                            {
                                bestDamage = action.damage;
                                bestAction = action;
                            }
                        }

                        if (bestAction != null)
                        {
                            selectedUnit.PerformAction(bestAction, clickedUnit);
                            turnManager.SpendPlayerAction();
                            OnUnitAttacked?.Invoke(selectedUnit, clickedUnit, bestAction);
                            DeselectUnit();

                            // Check if game over
                            if (turnManager.IsGameOver())
                            {
                                ClearHighlights();
                            }
                        }
                        return;
                    }
                }
            }
        }

        // Select a friendly unit
        if (!clickedUnit.IsEnemy && clickedUnit.CanAct())
        {
            SelectUnit(clickedUnit);
        }
        // Clicked an enemy without a selected unit — do nothing
    }

    private void HandleHexClick(HexCoord hex)
    {
        if (selectedUnit == null) return;
        if (!selectedUnit.CanAct()) return;

        // Check if this is a valid movement hex
        foreach (HexCoord moveHex in currentValidMoves)
        {
            if (moveHex == hex)
            {
                // Move the unit
                grid.PlaceUnit(selectedUnit, hex);
                selectedUnit.Act();
                turnManager.SpendPlayerAction();
                OnUnitMoved?.Invoke(selectedUnit, hex);
                DeselectUnit();

                if (turnManager.IsGameOver())
                {
                    ClearHighlights();
                }
                return;
            }
        }

        // Clicked an invalid hex — deselect
        DeselectUnit();
    }

    private void SelectUnit(Unit unit)
    {
        // Deselect previous
        DeselectUnit();

        selectedUnit = unit;

        // Show selection ring
        UnitVisual visual = unit.GetComponent<UnitVisual>();
        if (visual != null) visual.SetSelected(true);

        // Calculate valid movement and attack hexes
        currentValidMoves = GetValidMoveHexes(unit);
        currentValidAttacks = GetValidAttackHexes(unit);

        // Show highlights
        ShowMoveHighlights(currentValidMoves);
        ShowAttackHighlights(currentValidAttacks);

        OnUnitSelected?.Invoke(unit);
    }

    public void DeselectUnit()
    {
        if (selectedUnit != null)
        {
            UnitVisual visual = selectedUnit.GetComponent<UnitVisual>();
            if (visual != null) visual.SetSelected(false);

            OnUnitDeselected?.Invoke(selectedUnit);
        }

        selectedUnit = null;
        currentValidMoves.Clear();
        currentValidAttacks.Clear();
        ClearHighlights();
    }

    private List<HexCoord> GetValidMoveHexes(Unit unit)
    {
        // Get movement range from current state actions
        int moveRange = 0;
        List<UnitAction> actions = unit.GetCurrentActions();
        foreach (UnitAction action in actions)
        {
            if (action.actionName.ToLower().Contains("move") ||
                action.actionName.ToLower().Contains("retreat"))
            {
                if (action.range > moveRange)
                    moveRange = action.range;
            }
        }

        if (moveRange <= 0) return new List<HexCoord>();

        return grid.GetReachableHexes(unit.GridPosition, moveRange);
    }

    private List<HexCoord> GetValidAttackHexes(Unit unit)
    {
        List<HexCoord> attackHexes = new List<HexCoord>();
        List<UnitAction> actions = unit.GetCurrentActions();

        foreach (UnitAction action in actions)
        {
            // Skip movement actions
            if (action.actionName.ToLower().Contains("move") ||
                action.actionName.ToLower().Contains("retreat") ||
                action.actionName.ToLower().Contains("reload"))
                continue;

            // Get all hexes in range
            List<HexCoord> inRange = grid.GetHexesInRange(unit.GridPosition, action.range);
            foreach (HexCoord hex in inRange)
            {
                Unit target = grid.GetUnitAt(hex);
                if (target != null && target.IsEnemy != unit.IsEnemy)
                {
                    if (!attackHexes.Contains(hex))
                        attackHexes.Add(hex);
                }
            }
        }

        return attackHexes;
    }

    private HexCoord? GetHexFromRaycast(RaycastHit hit)
    {
        // Check if we hit a hex tile
        HexTileGenerator tile = hit.collider.GetComponentInParent<HexTileGenerator>();
        if (tile != null)
        {
            // Find which hex coord this tile is at
            Vector3 worldPos = tile.transform.position;
            return grid.WorldToHexPosition(worldPos);
        }

        return null;
    }

    #region Highlight Visualization

    private void ShowMoveHighlights(List<HexCoord> hexes)
    {
        foreach (HexCoord hex in hexes)
        {
            Color moveColor = new Color(0.2f, 0.8f, 0.3f, 0.4f); // translucent green
            CreateHighlight(hex, moveColor);
        }
    }

    private void ShowAttackHighlights(List<HexCoord> hexes)
    {
        // Only highlight enemy-occupied hexes for attack
        foreach (HexCoord hex in hexes)
        {
            Color attackColor = new Color(0.9f, 0.2f, 0.2f, 0.5f); // translucent red
            CreateHighlight(hex, attackColor);
        }
    }

    private void CreateHighlight(HexCoord hex, Color color)
    {
        Vector3 worldPos = grid.HexToWorldPosition(hex);
        worldPos.y = 0.02f; // Slightly above tile

        GameObject highlight = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        highlight.name = "Highlight";
        highlight.transform.position = worldPos;
        highlight.transform.localScale = new Vector3(0.5f, 0.02f, 0.5f);

        // Apply translucent material
        Renderer renderer = highlight.GetComponent<Renderer>();
        Material mat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
        mat.color = color;
        mat.SetFloat("_Metallic", 0f);
        mat.SetFloat("_Smoothness", 0.1f);
        renderer.material = mat;

        highlightObjects.Add(highlight);
    }

    private void ClearHighlights()
    {
        foreach (GameObject obj in highlightObjects)
        {
            Destroy(obj);
        }
        highlightObjects.Clear();
    }

    #endregion

    /// <summary>
    /// Get the currently selected unit (for external UI queries)
    /// </summary>
    public Unit GetSelectedUnit()
    {
        return selectedUnit;
    }
}