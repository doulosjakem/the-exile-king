using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public enum TurnPhase
{
    PlayerTurn,
    AITurn,
    GameOver
}

public class TurnManager : MonoBehaviour
{
    [Header("Turn Settings")]
    [SerializeField] private int playerActionsPerTurn = 2;
    [SerializeField] private int aiActionsPerTurn = 2;

    [Header("References")]
    [SerializeField] private HexGrid grid;
    [SerializeField] private AIDirector aiDirector;

    // State
    private TurnPhase currentPhase = TurnPhase.PlayerTurn;
    private int remainingPlayerActions = 0;
    private int remainingAIActions = 0;
    private List<Unit> playerUnits = new List<Unit>();
    private List<Unit> enemyUnits = new List<Unit>();

    // Events
    public UnityEvent<TurnPhase> OnPhaseChanged;
    public UnityEvent OnPlayerTurnStart;
    public UnityEvent OnPlayerTurnEnd;
    public UnityEvent OnAITurnStart;
    public UnityEvent OnAITurnEnd;
    public UnityEvent<Unit> OnUnitDied;
    public UnityEvent<bool> OnGameOver; // true = player won, false = player lost

    public TurnPhase CurrentPhase => currentPhase;
    public int RemainingPlayerActions => remainingPlayerActions;
    public int RemainingAIActions => remainingAIActions;
    public List<Unit> PlayerUnits => playerUnits;
    public List<Unit> EnemyUnits => enemyUnits;

    private void Start()
    {
        StartPlayerTurn();
    }

    public void RegisterUnit(Unit unit)
    {
        if (unit.IsEnemy)
        {
            if (!enemyUnits.Contains(unit))
            {
                enemyUnits.Add(unit);
                unit.OnUnitDied += OnAnyUnitDied;
            }
        }
        else
        {
            if (!playerUnits.Contains(unit))
            {
                playerUnits.Add(unit);
                unit.OnUnitDied += OnAnyUnitDied;
            }
        }
    }

    public void UnregisterUnit(Unit unit)
    {
        if (unit.IsEnemy)
        {
            enemyUnits.Remove(unit);
        }
        else
        {
            playerUnits.Remove(unit);
        }
        unit.OnUnitDied -= OnAnyUnitDied;
    }

    private void OnAnyUnitDied(Unit unit)
    {
        OnUnitDied?.Invoke(unit);

        // Check commander death
        if (unit.IsCommander)
        {
            if (unit.IsEnemy)
            {
                // Enemy commander died — player wins
                EndGame(true);
            }
            else
            {
                // David died — player loses
                EndGame(false);
            }
        }
    }

    public void StartPlayerTurn()
    {
        currentPhase = TurnPhase.PlayerTurn;
        remainingPlayerActions = playerActionsPerTurn;

        // Refresh all player units
        foreach (Unit unit in playerUnits)
        {
            unit.ResetForNewTurn();
            unit.Refresh();
        }

        // Refresh all enemy units
        foreach (Unit unit in enemyUnits)
        {
            unit.ResetForNewTurn();
            unit.Refresh();
        }

        OnPhaseChanged?.Invoke(currentPhase);
        OnPlayerTurnStart?.Invoke();

        Debug.Log($"Player turn started. Actions: {remainingPlayerActions}");
    }

    public bool SpendPlayerAction()
    {
        if (currentPhase != TurnPhase.PlayerTurn) return false;
        if (remainingPlayerActions <= 0) return false;

        remainingPlayerActions--;
        Debug.Log($"Player action spent. Remaining: {remainingPlayerActions}");

        if (remainingPlayerActions <= 0)
        {
            EndPlayerTurn();
        }

        return true;
    }

    /// <summary>
    /// David-only Overwork: spend a 3rd action. David skips next turn entirely.
    /// </summary>
    public bool SpendOverworkAction(Unit david)
    {
        if (currentPhase != TurnPhase.PlayerTurn) return false;
        if (remainingPlayerActions != 0) return false; // Must have used normal 2 actions first
        if (!david.IsCommander || david.IsEnemy) return false;

        // David skips his next turn entirely — set him to Exhausted and mark as acted
        david.SetState(UnitState.Exhausted);
        david.ResetForNewTurn(); // Reset so he can't act again this turn

        Debug.Log("David uses Overwork! He will skip his next turn.");

        EndPlayerTurn();
        return true;
    }

    public void EndPlayerTurn()
    {
        OnPlayerTurnEnd?.Invoke();
        StartAITurn();
    }

    public void StartAITurn()
    {
        currentPhase = TurnPhase.AITurn;
        remainingAIActions = aiActionsPerTurn;

        OnPhaseChanged?.Invoke(currentPhase);
        OnAITurnStart?.Invoke();

        Debug.Log("AI turn started.");

        // Let the AI director process its turn
        if (aiDirector != null)
        {
            aiDirector.ExecuteTurn(this, OnAITurnComplete);
        }
        else
        {
            // No AI director — just end AI turn immediately
            OnAITurnComplete();
        }
    }

    private void OnAITurnComplete()
    {
        OnAITurnEnd?.Invoke();
        StartPlayerTurn();
    }

    private void EndGame(bool playerWon)
    {
        currentPhase = TurnPhase.GameOver;
        OnPhaseChanged?.Invoke(currentPhase);
        OnGameOver?.Invoke(playerWon);

        Debug.Log(playerWon ? "Victory! Player wins." : "Defeat! Player loses.");
    }

    public bool IsPlayerTurn()
    {
        return currentPhase == TurnPhase.PlayerTurn;
    }

    public bool IsAITurn()
    {
        return currentPhase == TurnPhase.AITurn;
    }

    public bool IsGameOver()
    {
        return currentPhase == TurnPhase.GameOver;
    }
}