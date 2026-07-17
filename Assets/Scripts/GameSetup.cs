using System.Collections.Generic;
using UnityEngine;

public class GameSetup : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private HexGrid grid;
    [SerializeField] private TurnManager turnManager;
    [SerializeField] private CardDeckManager cardDeckManager;

    [Header("Unit Prefabs")]
    [SerializeField] private GameObject unitPrefab;

    [Header("Starting Units")]
    [SerializeField] private List<UnitTemplate> playerUnits = new List<UnitTemplate>();
    [SerializeField] private List<UnitTemplate> enemyUnits = new List<UnitTemplate>();

    private void Start()
    {
        if (grid == null) grid = FindObjectOfType<HexGrid>();
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
        if (cardDeckManager == null) cardDeckManager = FindObjectOfType<CardDeckManager>();
        SetupBattle();
    }

    private void SetupBattle()
    {
        if (unitPrefab == null)
        {
            Debug.LogError("Unit prefab not assigned in GameSetup!");
            return;
        }

        if (playerUnits.Count == 0 && enemyUnits.Count == 0)
        {
            SetupDefaultBattle();
            return;
        }

        for (int i = 0; i < playerUnits.Count; i++)
        {
            HexCoord coord = new HexCoord(1, 1 + i * 2);
            if (grid.IsValidCoord(coord))
                SpawnUnit(playerUnits[i], coord, false);
        }

        for (int i = 0; i < enemyUnits.Count; i++)
        {
            HexCoord coord = new HexCoord(grid.Width - 2, 1 + i * 2);
            if (grid.IsValidCoord(coord))
                SpawnUnit(enemyUnits[i], coord, true);
        }

        BuildInitialDeck();
    }

    private void SetupDefaultBattle()
    {
        SpawnUnit(new UnitTemplate { unitName = "David", unitType = UnitType.David, armorTier = ArmorTier.Bronze, isCommander = true },
            new HexCoord(1, 3), false);
        SpawnUnit(new UnitTemplate { unitName = "Scout", unitType = UnitType.Scout, armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(1, 1), false);
        SpawnUnit(new UnitTemplate { unitName = "Scout", unitType = UnitType.Scout, armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(1, 5), false);

        SpawnUnit(new UnitTemplate { unitName = "Amalekite Chieftain", unitType = UnitType.Chieftain, armorTier = ArmorTier.Bronze, isCommander = true },
            new HexCoord(grid.Width - 2, 3), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Raider", unitType = UnitType.Raider, armorTier = ArmorTier.Bronze, isCommander = false },
            new HexCoord(grid.Width - 2, 1), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Slinger", unitType = UnitType.Slinger, armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(grid.Width - 2, 5), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Scout", unitType = UnitType.EnemyScout, armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(grid.Width - 3, 4), true);

        BuildInitialDeck();
    }

    public void SpawnBattle(int battleNumber, List<UnitTemplate> playerRoster)
    {
        for (int i = 0; i < playerRoster.Count; i++)
        {
            HexCoord coord = new HexCoord(1, 1 + i * 2);
            if (grid.IsValidCoord(coord))
                SpawnUnit(playerRoster[i], coord, false);
        }

        int enemyCount = Mathf.Min(2 + battleNumber, 6);
        for (int i = 0; i < enemyCount; i++)
        {
            HexCoord coord = new HexCoord(grid.Width - 2, 1 + i * 2);
            if (!grid.IsValidCoord(coord)) continue;

            UnitTemplate enemy = GetEnemyForBattle(battleNumber, i);
            SpawnUnit(enemy, coord, true);
        }

        BuildInitialDeck();
    }

    public void SpawnBossBattle(List<UnitTemplate> playerRoster)
    {
        for (int i = 0; i < playerRoster.Count; i++)
        {
            HexCoord coord = new HexCoord(1, 1 + i * 2);
            if (grid.IsValidCoord(coord))
                SpawnUnit(playerRoster[i], coord, false);
        }

        SpawnUnit(new UnitTemplate { unitName = "Amalekite Chieftain", unitType = UnitType.Chieftain, armorTier = ArmorTier.Bronze, isCommander = true },
            new HexCoord(grid.Width - 2, 3), true);
        SpawnUnit(new UnitTemplate { unitName = "Camel Rider", unitType = UnitType.CamelRider, armorTier = ArmorTier.Iron, isCommander = false },
            new HexCoord(grid.Width - 2, 1), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Raider", unitType = UnitType.Raider, armorTier = ArmorTier.Bronze, isCommander = false },
            new HexCoord(grid.Width - 2, 5), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Raider", unitType = UnitType.Raider, armorTier = ArmorTier.Bronze, isCommander = false },
            new HexCoord(grid.Width - 3, 2), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Slinger", unitType = UnitType.Slinger, armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(grid.Width - 3, 4), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Slinger", unitType = UnitType.Slinger, armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(grid.Width - 3, 6), true);

        BuildInitialDeck();
    }

    private UnitTemplate GetEnemyForBattle(int battleNumber, int index)
    {
        System.Random rng = new System.Random();
        string[] names = { "Amalekite Raider", "Amalekite Slinger", "Amalekite Scout", "Amalekite Archer" };
        UnitType[] types = { UnitType.Raider, UnitType.Slinger, UnitType.EnemyScout, UnitType.EnemyArcher };
        ArmorTier[] armors = { ArmorTier.Bronze, ArmorTier.Leather, ArmorTier.Leather, ArmorTier.Bronze };

        int typeIndex = rng.Next(names.Length);
        return new UnitTemplate
        {
            unitName = names[typeIndex],
            unitType = types[typeIndex],
            armorTier = armors[typeIndex],
            isCommander = false
        };
    }

    private GameObject SpawnUnit(UnitTemplate template, HexCoord coord, bool isEnemy)
    {
        GameObject unitObj = Instantiate(unitPrefab, Vector3.zero, Quaternion.identity);
        unitObj.name = template.unitName;

        Unit unit = unitObj.GetComponent<Unit>();
        if (unit != null)
        {
            unit.SetName(template.unitName);
            unit.SetUnitType(template.unitType);
            unit.SetEnemy(isEnemy);
            unit.SetCommander(template.isCommander);
            unit.SetArmorTier(template.armorTier);
        }

        grid.PlaceUnit(unit, coord);

        if (turnManager != null)
            turnManager.RegisterUnit(unit);

        return unitObj;
    }

    private void BuildInitialDeck()
    {
        if (cardDeckManager == null) return;

        List<CommandCard> startingCards = new List<CommandCard>();

        foreach (Unit unit in turnManager.PlayerUnits)
        {
            CommandCard card = CreateCardForUnitType(unit.UnitType);
            if (card != null)
            {
                startingCards.Add(card);
            }
        }

        CommandCard march = ScriptableObject.CreateInstance<CommandCard>();
        march.cardName = "March";
        march.bottomAbilityName = "March";
        march.bottomAbilityDescription = "Move up to 2 units of one type.";
        march.bottomEffect = CardEffectType.Move;
        march.bottomValue = 2;
        march.bottomUnitFilter = UnitTypeFilter.Any;
        march.bottomMaxActivations = 2;
        startingCards.Add(march);
        startingCards.Add(march);

        CommandCard engage = ScriptableObject.CreateInstance<CommandCard>();
        engage.cardName = "Engage";
        engage.bottomAbilityName = "Engage";
        engage.bottomAbilityDescription = "Up to 2 units of one type attack.";
        engage.bottomEffect = CardEffectType.Attack;
        engage.bottomValue = 2;
        engage.bottomUnitFilter = UnitTypeFilter.Any;
        engage.bottomMaxActivations = 2;
        startingCards.Add(engage);
        startingCards.Add(engage);

        if (startingCards.Count == 0)
        {
            CommandCard defaultCard = ScriptableObject.CreateInstance<CommandCard>();
            defaultCard.cardName = "March";
            defaultCard.bottomAbilityName = "March";
            defaultCard.bottomAbilityDescription = "Move up to 2 units of one type.";
            defaultCard.bottomEffect = CardEffectType.Move;
            defaultCard.bottomValue = 2;
            defaultCard.bottomUnitFilter = UnitTypeFilter.Any;
            defaultCard.bottomMaxActivations = 2;
            startingCards.Add(defaultCard);
        }

        cardDeckManager.InitializeDeck(startingCards);
    }

    private CommandCard CreateCardForUnitType(UnitType unitType)
    {
        CommandCard card = ScriptableObject.CreateInstance<CommandCard>();

        switch (unitType)
        {
            case UnitType.David:
                card.cardName = "David's Leadership";
                card.topAbilityName = "Lead by Example";
                card.topAbilityDescription = "David + 1 ally move and attack. Adjacent allies +1 damage this turn.";
                card.topEffect = CardEffectType.MultiAttack;
                card.topValue = 2;
                card.topUnitFilter = UnitTypeFilter.CommanderOnly;
                card.topMaxActivations = 2;
                card.bottomAbilityName = "Move David";
                card.bottomAbilityDescription = "Move David up to 3 spaces.";
                card.bottomEffect = CardEffectType.Move;
                card.bottomValue = 3;
                card.bottomUnitFilter = UnitTypeFilter.CommanderOnly;
                card.bottomMaxActivations = 1;
                card.linkedUnitTypes = new List<UnitType> { UnitType.David };
                break;

            case UnitType.Swordsman:
                card.cardName = "Swordsmen Advance";
                card.topAbilityName = "Advance";
                card.topAbilityDescription = "Up to 3 Swordsmen move and attack. +1 attack if adjacent to another Swordsman.";
                card.topEffect = CardEffectType.MultiAttack;
                card.topValue = 3;
                card.topUnitFilter = UnitTypeFilter.SpecificType;
                card.topSpecificUnitType = UnitType.Swordsman;
                card.topMaxActivations = 3;
                card.bottomAbilityName = "Move Swordsmen";
                card.bottomAbilityDescription = "Move up to 2 Swordsmen.";
                card.bottomEffect = CardEffectType.MultiMove;
                card.bottomValue = 2;
                card.bottomUnitFilter = UnitTypeFilter.SpecificType;
                card.bottomSpecificUnitType = UnitType.Swordsman;
                card.bottomMaxActivations = 2;
                card.linkedUnitTypes = new List<UnitType> { UnitType.Swordsman };
                break;

            case UnitType.Archer:
                card.cardName = "Archer Volley";
                card.topAbilityName = "Volley";
                card.topAbilityDescription = "Up to 2 Archers attack. Must target enemies within range.";
                card.topEffect = CardEffectType.MultiAttack;
                card.topValue = 2;
                card.topUnitFilter = UnitTypeFilter.SpecificType;
                card.topSpecificUnitType = UnitType.Archer;
                card.topMaxActivations = 2;
                card.bottomAbilityName = "Reposition";
                card.bottomAbilityDescription = "Move up to 2 Archers.";
                card.bottomEffect = CardEffectType.MultiMove;
                card.bottomValue = 2;
                card.bottomUnitFilter = UnitTypeFilter.SpecificType;
                card.bottomSpecificUnitType = UnitType.Archer;
                card.bottomMaxActivations = 2;
                card.linkedUnitTypes = new List<UnitType> { UnitType.Archer };
                break;

            case UnitType.Spearman:
                card.cardName = "Spear Wall";
                card.topAbilityName = "Hold the Line";
                card.topAbilityDescription = "Up to 2 Spearmen attack. Gain +1 defense against melee this turn.";
                card.topEffect = CardEffectType.MultiAttack;
                card.topValue = 2;
                card.topUnitFilter = UnitTypeFilter.SpecificType;
                card.topSpecificUnitType = UnitType.Spearman;
                card.topMaxActivations = 2;
                card.bottomAbilityName = "Move Spearmen";
                card.bottomAbilityDescription = "Move up to 2 Spearmen. They may not be targeted by melee until next turn.";
                card.bottomEffect = CardEffectType.MultiMove;
                card.bottomValue = 2;
                card.bottomUnitFilter = UnitTypeFilter.SpecificType;
                card.bottomSpecificUnitType = UnitType.Spearman;
                card.bottomMaxActivations = 2;
                card.linkedUnitTypes = new List<UnitType> { UnitType.Spearman };
                break;

            case UnitType.Slinger:
                card.cardName = "Slinger Skirmish";
                card.topAbilityName = "Skirmish";
                card.topAbilityDescription = "Up to 2 Slingers attack. Ignore cover.";
                card.topEffect = CardEffectType.MultiAttack;
                card.topValue = 2;
                card.topUnitFilter = UnitTypeFilter.SpecificType;
                card.topSpecificUnitType = UnitType.Slinger;
                card.topMaxActivations = 2;
                card.bottomAbilityName = "Move Slingers";
                card.bottomAbilityDescription = "Move up to 2 Slingers. They gain +1 move this turn.";
                card.bottomEffect = CardEffectType.MultiMove;
                card.bottomValue = 2;
                card.bottomUnitFilter = UnitTypeFilter.SpecificType;
                card.bottomSpecificUnitType = UnitType.Slinger;
                card.bottomMaxActivations = 2;
                card.linkedUnitTypes = new List<UnitType> { UnitType.Slinger };
                break;

            case UnitType.Scout:
                card.cardName = "Scout Recon";
                card.topAbilityName = "Strike and Fade";
                card.topAbilityDescription = "Up to 2 Scouts move and attack. They cannot be targeted until next turn.";
                card.topEffect = CardEffectType.MultiAttack;
                card.topValue = 2;
                card.topUnitFilter = UnitTypeFilter.SpecificType;
                card.topSpecificUnitType = UnitType.Scout;
                card.topMaxActivations = 2;
                card.bottomAbilityName = "Move Scouts";
                card.bottomAbilityDescription = "Move up to 3 Scouts.";
                card.bottomEffect = CardEffectType.MultiMove;
                card.bottomValue = 3;
                card.bottomUnitFilter = UnitTypeFilter.SpecificType;
                card.bottomSpecificUnitType = UnitType.Scout;
                card.bottomMaxActivations = 2;
                card.linkedUnitTypes = new List<UnitType> { UnitType.Scout };
                break;

            case UnitType.Refugee:
                card.cardName = "Refugee Aid";
                card.topAbilityName = "Tend Wounds";
                card.topAbilityDescription = "Heal 1 HP on up to 2 units.";
                card.topEffect = CardEffectType.Heal;
                card.topValue = 1;
                card.topUnitFilter = UnitTypeFilter.Any;
                card.topMaxActivations = 2;
                card.bottomAbilityName = "Move Refugees";
                card.bottomAbilityDescription = "Move up to 2 Refugees to safety (away from enemies).";
                card.bottomEffect = CardEffectType.MultiMove;
                card.bottomValue = 2;
                card.bottomUnitFilter = UnitTypeFilter.SpecificType;
                card.bottomSpecificUnitType = UnitType.Refugee;
                card.bottomMaxActivations = 2;
                card.linkedUnitTypes = new List<UnitType> { UnitType.Refugee };
                break;

            default:
                return null;
        }

        return card;
    }
}

[System.Serializable]
public class UnitTemplate
{
    public string unitName = "Unit";
    public UnitType unitType = UnitType.None;
    public ArmorTier armorTier = ArmorTier.Leather;
    public bool isCommander = false;
}
