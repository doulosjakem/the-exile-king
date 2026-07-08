using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class AIDirector : MonoBehaviour
{
    [Header("AI Settings")]
    [SerializeField] private float commanderThreatRange = 2f;
    [SerializeField] private float retreatThreshold = 0.3f; // 30% HP

    private System.Random rng = new System.Random();

    /// <summary>
    /// Executes the AI turn using priority-based evaluation.
    /// Calls onComplete when all AI actions are spent.
    /// </summary>
    public void ExecuteTurn(TurnManager turnManager, Action onComplete)
    {
        List<Unit> enemies = turnManager.EnemyUnits;
        List<Unit> players = turnManager.PlayerUnits;

        // Get all ready enemy units
        List<Unit> readyUnits = enemies.Where(u => u.CanAct()).ToList();

        int actionsRemaining = turnManager.RemainingAIActions;

        foreach (Unit unit in readyUnits)
        {
            if (actionsRemaining <= 0) break;

            // Evaluate priorities for this unit
            AIAction bestAction = EvaluatePriorities(unit, players, enemies);

            if (bestAction != null)
            {
                ExecuteAIAction(unit, bestAction, turnManager);
                actionsRemaining--;
            }
        }

        onComplete?.Invoke();
    }

    private AIAction EvaluatePriorities(Unit unit, List<Unit> players, List<Unit> enemies)
    {
        // Priority 1: Protect commander
        Unit commander = enemies.FirstOrDefault(u => u.IsCommander);
        if (commander != null && IsCommanderThreatened(commander, players))
        {
            // Move toward the nearest threat to the commander
            Unit nearestThreat = FindNearestEnemy(commander.GridPosition, players);
            if (nearestThreat != null)
            {
                return new AIAction
                {
                    type = AIActionType.MoveToward,
                    target = nearestThreat,
                    priority = 1
                };
            }
        }

        // Priority 2: Attack weak / isolated units
        Unit weakTarget = FindWeakestTarget(unit, players);
        if (weakTarget != null && CanAttack(unit, weakTarget))
        {
            return new AIAction
            {
                type = AIActionType.Attack,
                target = weakTarget,
                priority = 2
            };
        }

        // Priority 3: Focus isolated enemies
        Unit isolatedTarget = FindIsolatedTarget(unit, players);
        if (isolatedTarget != null && CanAttack(unit, isolatedTarget))
        {
            return new AIAction
            {
                type = AIActionType.Attack,
                target = isolatedTarget,
                priority = 3
            };
        }

        // Priority 4: Attack nearest enemy
        Unit nearestEnemy = FindNearestEnemy(unit.GridPosition, players);
        if (nearestEnemy != null)
        {
            if (CanAttack(unit, nearestEnemy))
            {
                return new AIAction
                {
                    type = AIActionType.Attack,
                    target = nearestEnemy,
                    priority = 4
                };
            }
            else
            {
                // Move toward nearest enemy
                return new AIAction
                {
                    type = AIActionType.MoveToward,
                    target = nearestEnemy,
                    priority = 4
                };
            }
        }

        // Priority 5: Retreat if low HP
        if (unit.CurrentHP < unit.MaxHP * retreatThreshold)
        {
            Unit retreatTarget = FindRetreatPosition(unit, enemies);
            if (retreatTarget != null)
            {
                return new AIAction
                {
                    type = AIActionType.Retreat,
                    target = retreatTarget,
                    priority = 5
                };
            }
        }

        // No valid action found
        return null;
    }

    private bool IsCommanderThreatened(Unit commander, List<Unit> players)
    {
        foreach (Unit player in players)
        {
            int distance = commander.GridPosition.DistanceTo(player.GridPosition);
            if (distance <= commanderThreatRange)
            {
                return true;
            }
        }
        return false;
    }

    private Unit FindNearestEnemy(HexCoord position, List<Unit> enemies)
    {
        Unit nearest = null;
        int minDistance = int.MaxValue;

        foreach (Unit enemy in enemies)
        {
            int distance = position.DistanceTo(enemy.GridPosition);
            if (distance < minDistance)
            {
                minDistance = distance;
                nearest = enemy;
            }
        }

        return nearest;
    }

    private Unit FindWeakestTarget(Unit unit, List<Unit> players)
    {
        Unit weakest = null;
        int minHP = int.MaxValue;

        foreach (Unit player in players)
        {
            if (player.CurrentHP < minHP)
            {
                minHP = player.CurrentHP;
                weakest = player;
            }
        }

        return weakest;
    }

    private Unit FindIsolatedTarget(Unit unit, List<Unit> players)
    {
        foreach (Unit player in players)
        {
            bool hasAllyNearby = false;
            foreach (Unit otherPlayer in players)
            {
                if (otherPlayer == player) continue;
                int distance = player.GridPosition.DistanceTo(otherPlayer.GridPosition);
                if (distance <= 2)
                {
                    hasAllyNearby = true;
                    break;
                }
            }

            if (!hasAllyNearby)
            {
                return player;
            }
        }

        return null;
    }

    private Unit FindRetreatPosition(Unit unit, List<Unit> enemies)
    {
        // Simple retreat: move toward the commander
        Unit commander = enemies.FirstOrDefault(u => u.IsCommander);
        return commander;
    }

    private bool CanAttack(Unit attacker, Unit target)
    {
        List<UnitAction> actions = attacker.GetCurrentActions();
        foreach (UnitAction action in actions)
        {
            if (attacker.CanPerformAction(action, target))
            {
                return true;
            }
        }
        return false;
    }

    private void ExecuteAIAction(Unit unit, AIAction action, TurnManager turnManager)
    {
        switch (action.type)
        {
            case AIActionType.Attack:
                // Find the best action to use against the target
                List<UnitAction> availableActions = unit.GetCurrentActions();
                UnitAction bestAction = null;
                int bestDamage = 0;

                foreach (UnitAction a in availableActions)
                {
                    if (unit.CanPerformAction(a, action.target) && a.damage > bestDamage)
                    {
                        bestDamage = a.damage;
                        bestAction = a;
                    }
                }

                if (bestAction != null)
                {
                    unit.PerformAction(bestAction, action.target);
                    turnManager.SpendPlayerAction(); // Spend AI action (using same method for simplicity)
                }
                break;

            case AIActionType.MoveToward:
                // Move one step toward the target
                HexCoord currentPos = unit.GridPosition;
                HexCoord targetPos = action.target.GridPosition;
                HexCoord moveTarget = GetStepToward(currentPos, targetPos);

                if (moveTarget != currentPos)
                {
                    unit.GridPosition = moveTarget;
                    unit.Act();
                    turnManager.SpendPlayerAction();
                }
                break;

            case AIActionType.Retreat:
                // Move one step toward the commander
                if (action.target != null)
                {
                    HexCoord unitPos = unit.GridPosition;
                    HexCoord commanderPos = action.target.GridPosition;
                    HexCoord retreatPos = GetStepAway(unitPos, commanderPos);

                    if (retreatPos != unitPos)
                    {
                        unit.GridPosition = retreatPos;
                        unit.Act();
                        turnManager.SpendPlayerAction();
                    }
                }
                break;
        }
    }

    private HexCoord GetStepToward(HexCoord from, HexCoord to)
    {
        List<HexCoord> neighbors = from.GetNeighbors();
        HexCoord best = from;
        int minDistance = from.DistanceTo(to);

        foreach (HexCoord neighbor in neighbors)
        {
            int distance = neighbor.DistanceTo(to);
            if (distance < minDistance)
            {
                minDistance = distance;
                best = neighbor;
            }
        }

        return best;
    }

    private HexCoord GetStepAway(HexCoord from, HexCoord awayFrom)
    {
        List<HexCoord> neighbors = from.GetNeighbors();
        HexCoord best = from;
        int maxDistance = from.DistanceTo(awayFrom);

        foreach (HexCoord neighbor in neighbors)
        {
            int distance = neighbor.DistanceTo(awayFrom);
            if (distance > maxDistance)
            {
                maxDistance = distance;
                best = neighbor;
            }
        }

        return best;
    }

    private enum AIActionType
    {
        Attack,
        MoveToward,
        Retreat
    }

    private class AIAction
    {
        public AIActionType type;
        public Unit target;
        public int priority;
    }
}