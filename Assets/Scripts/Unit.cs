using System;
using System.Collections.Generic;
using UnityEngine;

public enum UnitState
{
    Ready,
    Acted,     // Optional intermediate state for 3-state units
    Exhausted
}

public enum ArmorTier
{
    Leather,  // 1 HP
    Bronze,   // 2 HP
    Iron      // 3 HP
}

[Serializable]
public class UnitAction
{
    public string actionName;
    public int range;
    public int damage;
    public Func<Unit, Unit, bool> onExecute; // callback for special effects
}

[Serializable]
public class UnitStateActions
{
    public UnitState state;
    public List<UnitAction> actions = new List<UnitAction>();
}

public class Unit : MonoBehaviour
{
    [Header("Unit Identity")]
    [SerializeField] private string unitName = "Unit";
    [SerializeField] private bool isCommander = false;
    [SerializeField] private bool isEnemy = false;
    [SerializeField] private int maxActionsPerTurn = 1;

    [Header("Combat Stats")]
    [SerializeField] private ArmorTier armorTier = ArmorTier.Leather;
    [SerializeField] private int currentHP;
    [SerializeField] private int maxHP;

    [Header("State Machine")]
    [SerializeField] private UnitState currentState = UnitState.Ready;
    [SerializeField] private bool hasActedThisTurn = false;

    [Header("State Actions")]
    [SerializeField] private List<UnitStateActions> stateActions = new List<UnitStateActions>();

    // Events
    public event Action<Unit> OnUnitDied;
    public event Action<Unit, UnitState> OnStateChanged;

    // References
    public HexCoord GridPosition { get; set; }
    public bool IsEnemy => isEnemy;
    public bool IsCommander => isCommander;
    public string UnitName => unitName;
    public UnitState CurrentState => currentState;
    public int CurrentHP => currentHP;
    public int MaxHP => maxHP;

    private void Awake()
    {
        InitializeHP();
    }

    private void InitializeHP()
    {
        switch (armorTier)
        {
            case ArmorTier.Leather:
                maxHP = 1;
                break;
            case ArmorTier.Bronze:
                maxHP = 2;
                break;
            case ArmorTier.Iron:
                maxHP = 3;
                break;
        }
        currentHP = maxHP;
    }

    public bool CanAct()
    {
        return currentState != UnitState.Exhausted && !hasActedThisTurn;
    }

    public void Act()
    {
        if (!CanAct()) return;

        hasActedThisTurn = true;

        // Advance state
        switch (currentState)
        {
            case UnitState.Ready:
                SetState(UnitState.Acted);
                break;
            case UnitState.Acted:
                SetState(UnitState.Exhausted);
                break;
            case UnitState.Exhausted:
                // Already exhausted — shouldn't reach here with CanAct check
                break;
        }
    }

    public void Refresh()
    {
        // Advance one state toward Ready
        switch (currentState)
        {
            case UnitState.Exhausted:
                SetState(UnitState.Acted);
                break;
            case UnitState.Acted:
                SetState(UnitState.Ready);
                break;
            case UnitState.Ready:
                // Already ready, stay ready
                break;
        }
    }

    public void ResetForNewTurn()
    {
        hasActedThisTurn = false;
    }

    public void SetState(UnitState newState)
    {
        UnitState oldState = currentState;
        currentState = newState;
        OnStateChanged?.Invoke(this, newState);

        if (oldState != newState)
        {
            Debug.Log($"{unitName} state: {oldState} → {newState}");
        }
    }

    public void TakeDamage(int damage)
    {
        currentHP -= damage;
        Debug.Log($"{unitName} takes {damage} damage. HP: {currentHP}/{maxHP}");

        if (currentHP <= 0)
        {
            currentHP = 0;
            OnUnitDied?.Invoke(this);
            Destroy(gameObject);
        }
    }

    public void Heal(int amount)
    {
        currentHP = Mathf.Min(currentHP + amount, maxHP);
    }

    public List<UnitAction> GetCurrentActions()
    {
        foreach (UnitStateActions stateActionSet in stateActions)
        {
            if (stateActionSet.state == currentState)
            {
                return stateActionSet.actions;
            }
        }
        return new List<UnitAction>();
    }

    public bool CanPerformAction(UnitAction action, Unit target)
    {
        if (target == null) return false;
        if (target == this) return false;
        if (target.IsEnemy == IsEnemy) return false; // Can't target allies

        int distance = GridPosition.DistanceTo(target.GridPosition);
        return distance <= action.range;
    }

    public void PerformAction(UnitAction action, Unit target)
    {
        if (!CanPerformAction(action, target)) return;

        // Apply damage
        target.TakeDamage(action.damage);

        // Trigger special effect callback if exists
        action.onExecute?.Invoke(this, target);

        // Advance unit state
        Act();
    }
}