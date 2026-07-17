using System.Collections.Generic;
using UnityEngine;

public class CardAbilityResolver : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private HexGrid grid;
    [SerializeField] private TurnManager turnManager;
    [SerializeField] private DamagePopup damagePopup;

    private CardDeckManager cardDeckManager;
    private CommandCard currentCard;
    private CardHalf currentHalf;

    private void Start()
    {
        if (grid == null) grid = FindObjectOfType<HexGrid>();
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
        if (damagePopup == null) damagePopup = FindObjectOfType<DamagePopup>();
        if (cardDeckManager == null) cardDeckManager = FindObjectOfType<CardDeckManager>();
    }

    public void BeginResolution(CommandCard card, CardHalf half)
    {
        currentCard = card;
        currentHalf = half;
    }

    public void EndResolution()
    {
        currentCard = null;
        currentHalf = null;
    }

    public bool IsResolving => currentCard != null;

    public CardEffectType GetCurrentEffect()
    {
        if (currentCard == null) return CardEffectType.Move;
        return currentHalf == CardHalf.Top ? currentCard.topEffect : currentCard.bottomEffect;
    }

    public List<Unit> GetValidTargets()
    {
        if (currentCard == null) return new List<Unit>();

        UnitTypeFilter filter = currentHalf == CardHalf.Top ? currentCard.topUnitFilter : currentCard.bottomUnitFilter;
        UnitType specificType = currentHalf == CardHalf.Top ? currentCard.topSpecificUnitType : currentCard.bottomSpecificUnitType;
        int maxActivations = currentHalf == CardHalf.Top ? currentCard.topMaxActivations : currentCard.bottomMaxActivations;

        List<Unit> allPlayerUnits = turnManager != null ? turnManager.PlayerUnits : new List<Unit>();
        List<Unit> validTargets = new List<Unit>();

        foreach (Unit unit in allPlayerUnits)
        {
            if (!unit.CanActivate()) continue;
            if (!MatchesFilter(unit, filter, specificType)) continue;

            validTargets.Add(unit);
        }

        if (maxActivations > 0 && validTargets.Count > maxActivations)
        {
            validTargets = validTargets.GetRange(0, maxActivations);
        }

        return validTargets;
    }

    public List<HexCoord> GetValidMoveHexes(Unit unit)
    {
        if (currentCard == null || !unit.CanActivate()) return new List<HexCoord>();

        CardEffectType effect = currentHalf == CardHalf.Top ? currentCard.topEffect : currentCard.bottomEffect;
        if (effect != CardEffectType.Move && effect != CardEffectType.MultiMove) return new List<HexCoord>();

        int moveRange = currentHalf == CardHalf.Top ? currentCard.topValue : currentCard.bottomValue;
        if (moveRange <= 0) return new List<HexCoord>();

        return grid.GetReachableHexes(unit.GridPosition, moveRange);
    }

    public List<HexCoord> GetValidAttackTargets(Unit unit)
    {
        if (currentCard == null || !unit.CanActivate()) return new List<HexCoord>();

        CardEffectType effect = currentHalf == CardHalf.Top ? currentCard.topEffect : currentCard.bottomEffect;
        if (effect != CardEffectType.Attack && effect != CardEffectType.MultiAttack) return new List<HexCoord>();

        int attackRange = currentHalf == CardHalf.Top ? currentCard.topValue : currentCard.bottomValue;
        if (attackRange <= 0) return new List<HexCoord>();

        List<HexCoord> targetHexes = new List<HexCoord>();
        List<HexCoord> inRange = grid.GetHexesInRange(unit.GridPosition, attackRange);

        foreach (HexCoord hex in inRange)
        {
            Unit target = grid.GetUnitAt(hex);
            if (target != null && target.IsEnemy)
            {
                targetHexes.Add(hex);
            }
        }

        return targetHexes;
    }

    public void ResolveMove(Unit unit, HexCoord targetHex)
    {
        if (currentCard == null || !unit.CanActivate()) return;

        grid.PlaceUnit(unit, targetHex);
        unit.Activate();
    }

    public void ResolveAttack(Unit attacker, Unit target)
    {
        if (currentCard == null || !attacker.CanActivate()) return;

        int damage = currentHalf == CardHalf.Top ? currentCard.topValue : currentCard.bottomValue;

        if (damagePopup != null)
        {
            damagePopup.ShowDamage(target.GridPosition, damage);
        }

        target.TakeDamage(damage);
        attacker.Activate();
    }

    public void ResolveBuff(Unit unit)
    {
        if (currentCard == null || !unit.CanActivate()) return;

        int buffValue = currentHalf == CardHalf.Top ? currentCard.topValue : currentCard.bottomValue;

        unit.Heal(buffValue);
        unit.Activate();
    }

    private bool MatchesFilter(Unit unit, UnitTypeFilter filter, UnitType specificType)
    {
        switch (filter)
        {
            case UnitTypeFilter.Any:
                return true;
            case UnitTypeFilter.SpecificType:
                return specificType != UnitType.None && unit.UnitType == specificType;
            case UnitTypeFilter.RangedOnly:
                return unit.UnitType == UnitType.Archer || unit.UnitType == UnitType.Slinger ||
                       unit.UnitType == UnitType.EnemyArcher;
            case UnitTypeFilter.MeleeOnly:
                return unit.UnitType == UnitType.Swordsman || unit.UnitType == UnitType.Spearman ||
                       unit.UnitType == UnitType.David || unit.UnitType == UnitType.Raider ||
                       unit.UnitType == UnitType.Chieftain || unit.UnitType == UnitType.CamelRider;
            case UnitTypeFilter.CommanderOnly:
                return unit.IsCommander;
            default:
                return true;
        }
    }
}
