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
    [Header("References")]
    [SerializeField] private HexGrid grid;
    [SerializeField] private AIDirector aiDirector;
    [SerializeField] private CardDeckManager cardDeckManager;

    [Header("Turn Settings")]
    [SerializeField] private int handSize = 4;
    [SerializeField] private int aiActionsPerTurn = 2;

    private TurnPhase currentPhase = TurnPhase.PlayerTurn;
    private int remainingAIActions = 0;
    private List<Unit> playerUnits = new List<Unit>();
    private List<Unit> enemyUnits = new List<Unit>();

    public UnityEvent<TurnPhase> OnPhaseChanged;
    public UnityEvent OnPlayerTurnStart;
    public UnityEvent OnPlayerTurnEnd;
    public UnityEvent OnAITurnStart;
    public UnityEvent OnAITurnEnd;
    public UnityEvent<Unit> OnUnitDied;
    public UnityEvent<bool> OnGameOver;

    public TurnPhase CurrentPhase => currentPhase;
    public List<Unit> PlayerUnits => playerUnits;
    public List<Unit> EnemyUnits => enemyUnits;

    private void Start()
    {
        if (grid == null) grid = FindObjectOfType<HexGrid>();
        if (aiDirector == null) aiDirector = FindObjectOfType<AIDirector>();
        if (cardDeckManager == null) cardDeckManager = FindObjectOfType<CardDeckManager>();

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

        if (unit.IsCommander)
        {
            if (unit.IsEnemy)
            {
                EndGame(true);
            }
            else
            {
                EndGame(false);
            }
        }
    }

    public void StartPlayerTurn()
    {
        currentPhase = TurnPhase.PlayerTurn;

        ResetPlayerUnitActivations();

        cardDeckManager.DrawToHandSize(handSize);
        cardDeckManager.ApplyFatigue();

        OnPhaseChanged?.Invoke(currentPhase);
        OnPlayerTurnStart?.Invoke();

        Debug.Log("Player turn started.");
    }

    public void EndPlayerTurn()
    {
        if (currentPhase != TurnPhase.PlayerTurn) return;

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

        if (aiDirector != null)
        {
            aiDirector.ExecuteTurn(this, OnAITurnComplete);
        }
        else
        {
            OnAITurnComplete();
        }
    }

    public bool SpendAIAction()
    {
        if (currentPhase != TurnPhase.AITurn) return false;
        if (remainingAIActions <= 0) return false;

        remainingAIActions--;
        Debug.Log($"AI action spent. Remaining: {remainingAIActions}");

        return true;
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

    private void ResetPlayerUnitActivations()
    {
        foreach (Unit unit in playerUnits)
        {
            if (unit != null)
            {
                unit.ResetActivation();
            }
        }
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
