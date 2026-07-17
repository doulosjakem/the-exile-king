using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class AIDirector : MonoBehaviour
{
    [Header("AI Settings")]
    [SerializeField] private float commanderThreatRange = 2f;
    [SerializeField] private float retreatThreshold = 0.3f;

    private System.Random rng = new System.Random();
    private DamagePopup damagePopup;

    public void ExecuteTurn(TurnManager turnManager, Action onComplete)
    {
        if (damagePopup == null)
        {
            damagePopup = FindObjectOfType<DamagePopup>();
            if (damagePopup == null)
            {
                GameObject dp = new GameObject("DamagePopup");
                damagePopup = dp.AddComponent<DamagePopup>();
            }
        }

        List<Unit> enemies = turnManager.EnemyUnits;
        List<Unit> players = turnManager.PlayerUnits;

        List<Unit> readyUnits = enemies.Where(u => u.CanActivate()).ToList();

        foreach (Unit unit in readyUnits)
        {
            if (!turnManager.SpendAIAction()) break;

            AIAction bestAction = EvaluatePriorities(unit, players, enemies);

            if (bestAction != null)
            {
                ExecuteAIAction(unit, bestAction, turnManager);
            }
        }

        onComplete?.Invoke();
    }

    private AIAction EvaluatePriorities(Unit unit, List<Unit> players, List<Unit> enemies)
    {
        Unit commander = enemies.FirstOrDefault(u => u.IsCommander);
        if (commander != null && IsCommanderThreatened(commander, players))
        {
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
                return new AIAction
                {
                    type = AIActionType.MoveToward,
                    target = nearestEnemy,
                    priority = 4
                };
            }
        }

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
        Unit commander = enemies.FirstOrDefault(u => u.IsCommander);
        return commander;
    }

    private bool CanAttack(Unit attacker, Unit target)
    {
        if (target == null) return false;
        int distance = attacker.GridPosition.DistanceTo(target.GridPosition);
        return distance <= attacker.GetAttackRange();
    }

    private void ExecuteAIAction(Unit unit, AIAction action, TurnManager turnManager)
    {
        switch (action.type)
        {
            case AIActionType.Attack:
                int damage = unit.GetAttackRange() > 1 ? 2 : 2;
                if (damagePopup != null)
                {
                    damagePopup.ShowDamage(action.target.GridPosition, damage);
                }
                action.target.TakeDamage(damage);
                unit.Activate();
                break;

            case AIActionType.MoveToward:
                HexCoord currentPos = unit.GridPosition;
                HexCoord targetPos = action.target.GridPosition;
                HexCoord moveTarget = GetStepToward(currentPos, targetPos);

                if (moveTarget != currentPos)
                {
                    HexGrid grid = FindObjectOfType<HexGrid>();
                    if (grid != null)
                    {
                        grid.PlaceUnit(unit, moveTarget);
                    }
                    unit.Activate();
                }
                break;

            case AIActionType.Retreat:
                if (action.target != null)
                {
                    HexCoord unitPos = unit.GridPosition;
                    HexCoord commanderPos = action.target.GridPosition;
                    HexCoord retreatPos = GetStepAway(unitPos, commanderPos);

                    if (retreatPos != unitPos)
                    {
                        HexGrid grid = FindObjectOfType<HexGrid>();
                        if (grid != null)
                        {
                            grid.PlaceUnit(unit, retreatPos);
                        }
                        unit.Activate();
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
