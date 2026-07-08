using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "NewUnitType", menuName = "Game/Unit Type")]
public class UnitData : ScriptableObject
{
    [Header("Identity")]
    public string unitName = "Unit";
    public bool isCommander = false;
    public bool isEnemy = false;

    [Header("Combat")]
    public ArmorTier armorTier = ArmorTier.Leather;
    public int maxHP = 1;

    [Header("State Actions")]
    public List<UnitStateActionData> stateActions = new List<UnitStateActionData>();

    [Header("Visual")]
    public Color teamColor = Color.blue;
    public UnitShape shape = UnitShape.Standard;
}

[System.Serializable]
public class UnitStateActionData
{
    public UnitState state;
    public List<ActionData> actions = new List<ActionData>();
}

[System.Serializable]
public class ActionData
{
    public string actionName = "Attack";
    public int range = 1;
    public int damage = 1;
    public bool isMovement = false;
}

public enum UnitShape
{
    Standard,   // Swordsman/Spearman
    Ranged,     // Slinger/Archer
    Scout,      // Scout
    Commander,   // David/Chieftain
    Heavy       // Camel Rider
}

[CreateAssetMenu(fileName = "NewEncounter", menuName = "Game/Encounter")]
public class EncounterData : ScriptableObject
{
    public string encounterName = "Battle";
    public int difficultyLevel = 1;
    public bool isBoss = false;

    public List<EncounterUnit> playerUnits = new List<EncounterUnit>();
    public List<EncounterUnit> enemyUnits = new List<EncounterUnit>();
}

[System.Serializable]
public class EncounterUnit
{
    public UnitData unitData;
    public HexCoord spawnPosition;
}