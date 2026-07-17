using System.Collections.Generic;
using UnityEngine;

public class PlayerInputHandler : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private HexGrid grid;
    [SerializeField] private TurnManager turnManager;
    [SerializeField] private CardAbilityResolver abilityResolver;

    [Header("Visual Feedback")]
    [SerializeField] private GameObject moveHighlightPrefab;
    [SerializeField] private GameObject attackHighlightPrefab;

    private Unit selectedUnit;
    private List<HexCoord> currentValidMoves = new List<HexCoord>();
    private List<HexCoord> currentValidAttacks = new List<HexCoord>();
    private List<GameObject> highlightObjects = new List<GameObject>();
    private List<Unit> selectedUnitsForAbility = new List<Unit>();

    public System.Action<Unit> OnUnitSelected;
    public System.Action<Unit> OnUnitDeselected;
    public System.Action<Unit, HexCoord> OnUnitMoved;
    public System.Action<Unit, Unit> OnUnitAttacked;

    private Camera mainCamera;
    private DamagePopup damagePopup;

    private void Start()
    {
        mainCamera = Camera.main;
        if (grid == null) grid = FindObjectOfType<HexGrid>();
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
        if (abilityResolver == null) abilityResolver = FindObjectOfType<CardAbilityResolver>();
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

        if (Input.GetMouseButtonDown(0))
        {
            HandleInput(Input.mousePosition);
        }

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
            Unit clickedUnit = hit.collider.GetComponentInParent<Unit>();
            if (clickedUnit != null)
            {
                HandleUnitClick(clickedUnit);
                return;
            }

            HexCoord? clickedHex = GetHexFromRaycast(hit);
            if (clickedHex.HasValue)
            {
                HandleHexClick(clickedHex.Value);
                return;
            }
        }

        DeselectUnit();
    }

    private void HandleUnitClick(Unit clickedUnit)
    {
        if (abilityResolver != null && abilityResolver.IsResolving)
        {
            HandleCardAbilityUnitClick(clickedUnit);
            return;
        }

        if (selectedUnit != null && !selectedUnit.IsEnemy && clickedUnit.IsEnemy)
        {
            if (selectedUnit.CanActivate())
            {
                foreach (HexCoord attackHex in currentValidAttacks)
                {
                    if (attackHex == clickedUnit.GridPosition)
                    {
                        int damage = 2;
                        if (damagePopup != null)
                        {
                            damagePopup.ShowDamage(clickedUnit.GridPosition, damage);
                        }
                        clickedUnit.TakeDamage(damage);
                        selectedUnit.Activate();
                        OnUnitAttacked?.Invoke(selectedUnit, clickedUnit);
                        DeselectUnit();

                        if (turnManager != null && turnManager.IsGameOver())
                        {
                            ClearHighlights();
                        }
                        return;
                    }
                }
            }
        }

        if (!clickedUnit.IsEnemy && clickedUnit.CanActivate())
        {
            SelectUnit(clickedUnit);
        }
    }

    private void HandleCardAbilityUnitClick(Unit clickedUnit)
    {
        List<Unit> validTargets = abilityResolver.GetValidTargets();

        if (validTargets.Contains(clickedUnit))
        {
            if (!selectedUnitsForAbility.Contains(clickedUnit))
            {
                selectedUnitsForAbility.Add(clickedUnit);
                UnitVisual visual = clickedUnit.GetComponent<UnitVisual>();
                if (visual != null) visual.SetSelected(true);
            }

            int maxActivations = abilityResolver.GetValidTargets().Count;
            if (selectedUnitsForAbility.Count >= maxActivations || maxActivations <= 0)
            {
                ResolveCardAbility();
            }
        }
    }

    private void HandleHexClick(HexCoord hex)
    {
        if (abilityResolver != null && abilityResolver.IsResolving)
        {
            HandleCardAbilityHexClick(hex);
            return;
        }

        if (selectedUnit == null) return;
        if (!selectedUnit.CanActivate()) return;

        foreach (HexCoord moveHex in currentValidMoves)
        {
            if (moveHex == hex)
            {
                grid.PlaceUnit(selectedUnit, hex);
                selectedUnit.Activate();
                OnUnitMoved?.Invoke(selectedUnit, hex);
                DeselectUnit();

                if (turnManager != null && turnManager.IsGameOver())
                {
                    ClearHighlights();
                }
                return;
            }
        }

        DeselectUnit();
    }

    private void HandleCardAbilityHexClick(HexCoord hex)
    {
        if (selectedUnit == null) return;
        if (!selectedUnit.CanActivate()) return;

        List<HexCoord> validMoves = abilityResolver.GetValidMoveHexes(selectedUnit);
        if (validMoves.Contains(hex))
        {
            abilityResolver.ResolveMove(selectedUnit, hex);
            ClearHighlights();
            DeselectUnit();
            ResolveCardAbility();
        }
    }

    private void SelectUnit(Unit unit)
    {
        DeselectUnit();

        selectedUnit = unit;

        UnitVisual visual = unit.GetComponent<UnitVisual>();
        if (visual != null) visual.SetSelected(true);

        currentValidMoves = GetValidMoveHexes(unit);
        currentValidAttacks = GetValidAttackHexes(unit);

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
        return grid.GetReachableHexes(unit.GridPosition, unit.UnitType == UnitType.Scout ? 3 : 2);
    }

    private List<HexCoord> GetValidAttackHexes(Unit unit)
    {
        List<HexCoord> attackHexes = new List<HexCoord>();
        List<HexCoord> inRange = grid.GetHexesInRange(unit.GridPosition, unit.GetAttackRange());

        foreach (HexCoord hex in inRange)
        {
            Unit target = grid.GetUnitAt(hex);
            if (target != null && target.IsEnemy != unit.IsEnemy)
            {
                if (!attackHexes.Contains(hex))
                    attackHexes.Add(hex);
            }
        }

        return attackHexes;
    }

    private HexCoord? GetHexFromRaycast(RaycastHit hit)
    {
        HexTileGenerator tile = hit.collider.GetComponentInParent<HexTileGenerator>();
        if (tile != null)
        {
            Vector3 worldPos = tile.transform.position;
            return grid.WorldToHexPosition(worldPos);
        }
        return null;
    }

    private void ResolveCardAbility()
    {
        if (abilityResolver == null || selectedUnitsForAbility.Count == 0) return;

        CardEffectType effect = abilityResolver.GetCurrentEffect();

        foreach (Unit unit in selectedUnitsForAbility)
        {
            switch (effect)
            {
                case CardEffectType.Attack:
                case CardEffectType.MultiAttack:
                    Unit nearestEnemy = FindNearestEnemy(unit);
                    if (nearestEnemy != null)
                    {
                        abilityResolver.ResolveAttack(unit, nearestEnemy);
                    }
                    break;
                case CardEffectType.Heal:
                    abilityResolver.ResolveBuff(unit);
                    break;
                case CardEffectType.Move:
                case CardEffectType.MultiMove:
                    abilityResolver.ResolveMove(unit, unit.GridPosition);
                    break;
            }
        }

        foreach (Unit unit in selectedUnitsForAbility)
        {
            UnitVisual visual = unit.GetComponent<UnitVisual>();
            if (visual != null) visual.SetSelected(false);
        }

        selectedUnitsForAbility.Clear();
        ClearHighlights();
        DeselectUnit();
    }

    private Unit FindNearestEnemy(Unit fromUnit)
    {
        List<Unit> enemies = turnManager != null ? turnManager.EnemyUnits : new List<Unit>();
        Unit nearest = null;
        int minDistance = int.MaxValue;

        foreach (Unit enemy in enemies)
        {
            int distance = fromUnit.GridPosition.DistanceTo(enemy.GridPosition);
            if (distance < minDistance)
            {
                minDistance = distance;
                nearest = enemy;
            }
        }

        return nearest;
    }

    #region Highlight Visualization

    private void ShowMoveHighlights(List<HexCoord> hexes)
    {
        foreach (HexCoord hex in hexes)
        {
            Color moveColor = new Color(0.2f, 0.8f, 0.3f, 0.4f);
            CreateHighlight(hex, moveColor);
        }
    }

    private void ShowAttackHighlights(List<HexCoord> hexes)
    {
        foreach (HexCoord hex in hexes)
        {
            Color attackColor = new Color(0.9f, 0.2f, 0.2f, 0.5f);
            CreateHighlight(hex, attackColor);
        }
    }

    private void CreateHighlight(HexCoord hex, Color color)
    {
        Vector3 worldPos = grid.HexToWorldPosition(hex);
        worldPos.y = 0.02f;

        GameObject highlight = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        highlight.name = "Highlight";
        highlight.transform.position = worldPos;
        highlight.transform.localScale = new Vector3(0.5f, 0.02f, 0.5f);

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

    public Unit GetSelectedUnit()
    {
        return selectedUnit;
    }
}
