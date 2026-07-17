using System.Collections.Generic;
using UnityEngine;

public enum CardEffectType
{
    Move,
    Attack,
    Buff,
    Heal,
    MultiMove,
    MultiAttack
}

public enum UnitTypeFilter
{
    Any,
    SpecificType,
    RangedOnly,
    MeleeOnly,
    CommanderOnly
}

[CreateAssetMenu(fileName = "CommandCard", menuName = "Cards/CommandCard")]
public class CommandCard : ScriptableObject
{
    [Header("Card Identity")]
    public string cardName;
    public Sprite cardArt;

    [Header("Top Ability")]
    public string topAbilityName;
    public string topAbilityDescription;
    public CardEffectType topEffect;
    public int topValue;
    public UnitTypeFilter topUnitFilter;
    public UnitType topSpecificUnitType;
    public int topMaxActivations;

    [Header("Bottom Ability")]
    public string bottomAbilityName;
    public string bottomAbilityDescription;
    public CardEffectType bottomEffect;
    public int bottomValue;
    public UnitTypeFilter bottomUnitFilter;
    public UnitType bottomSpecificUnitType;
    public int bottomMaxActivations;

    [Header("Card Properties")]
    public bool isLostOnUse;
    public List<UnitType> linkedUnitTypes = new List<UnitType>();

    public bool MatchesUnitType(UnitType type)
    {
        return linkedUnitTypes != null && linkedUnitTypes.Contains(type);
    }

    public bool IsHalfAvailable(CardHalf half)
    {
        UnitTypeFilter filter = half == CardHalf.Top ? topUnitFilter : bottomUnitFilter;
        UnitType specificType = half == CardHalf.Top ? topSpecificUnitType : bottomSpecificUnitType;
        return filter != UnitTypeFilter.SpecificType || specificType != UnitType.None;
    }
}

public enum CardHalf
{
    Top,
    Bottom
}
