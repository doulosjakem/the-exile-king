using System.Collections.Generic;
using UnityEngine;

public class GameSetup : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private HexGrid grid;
    [SerializeField] private TurnManager turnManager;

    [Header("Unit Prefabs")]
    [SerializeField] private GameObject unitPrefab;

    [Header("Starting Units")]
    [SerializeField] private List<UnitTemplate> playerUnits = new List<UnitTemplate>();
    [SerializeField] private List<UnitTemplate> enemyUnits = new List<UnitTemplate>();

    private void Start()
    {
        if (grid == null) grid = FindObjectOfType<HexGrid>();
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
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
    }

    private void SetupDefaultBattle()
    {
        SpawnUnit(new UnitTemplate { unitName = "David", armorTier = ArmorTier.Bronze, isCommander = true },
            new HexCoord(1, 3), false);
        SpawnUnit(new UnitTemplate { unitName = "Scout", armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(1, 1), false);
        SpawnUnit(new UnitTemplate { unitName = "Scout", armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(1, 5), false);

        SpawnUnit(new UnitTemplate { unitName = "Amalekite Chieftain", armorTier = ArmorTier.Bronze, isCommander = true },
            new HexCoord(grid.Width - 2, 3), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Raider", armorTier = ArmorTier.Bronze, isCommander = false },
            new HexCoord(grid.Width - 2, 1), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Slinger", armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(grid.Width - 2, 5), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Scout", armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(grid.Width - 3, 4), true);
    }

    /// <summary>
    /// Spawn a battle at a given difficulty level (called by RunManager)
    /// </summary>
    public void SpawnBattle(int battleNumber, List<UnitTemplate> playerRoster)
    {
        // Spawn player units from roster
        for (int i = 0; i < playerRoster.Count; i++)
        {
            HexCoord coord = new HexCoord(1, 1 + i * 2);
            if (grid.IsValidCoord(coord))
                SpawnUnit(playerRoster[i], coord, false);
        }

        // Spawn enemies based on battle number
        int enemyCount = Mathf.Min(2 + battleNumber, 6);
        for (int i = 0; i < enemyCount; i++)
        {
            HexCoord coord = new HexCoord(grid.Width - 2, 1 + i * 2);
            if (!grid.IsValidCoord(coord)) continue;

            UnitTemplate enemy = GetEnemyForBattle(battleNumber, i);
            SpawnUnit(enemy, coord, true);
        }
    }

    /// <summary>
    /// Spawn the boss battle (called by RunManager)
    /// </summary>
    public void SpawnBossBattle(List<UnitTemplate> playerRoster)
    {
        // Spawn player units
        for (int i = 0; i < playerRoster.Count; i++)
        {
            HexCoord coord = new HexCoord(1, 1 + i * 2);
            if (grid.IsValidCoord(coord))
                SpawnUnit(playerRoster[i], coord, false);
        }

        // Boss: Chieftain + Camel Rider + 2 Raiders + 2 Slingers
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Chieftain", armorTier = ArmorTier.Bronze, isCommander = true },
            new HexCoord(grid.Width - 2, 3), true);
        SpawnUnit(new UnitTemplate { unitName = "Camel Rider", armorTier = ArmorTier.Iron, isCommander = false },
            new HexCoord(grid.Width - 2, 1), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Raider", armorTier = ArmorTier.Bronze, isCommander = false },
            new HexCoord(grid.Width - 2, 5), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Raider", armorTier = ArmorTier.Bronze, isCommander = false },
            new HexCoord(grid.Width - 3, 2), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Slinger", armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(grid.Width - 3, 4), true);
        SpawnUnit(new UnitTemplate { unitName = "Amalekite Slinger", armorTier = ArmorTier.Leather, isCommander = false },
            new HexCoord(grid.Width - 3, 6), true);
    }

    private UnitTemplate GetEnemyForBattle(int battleNumber, int index)
    {
        System.Random rng = new System.Random();
        string[] names = { "Amalekite Raider", "Amalekite Slinger", "Amalekite Scout", "Amalekite Archer" };
        ArmorTier[] armors = { ArmorTier.Bronze, ArmorTier.Leather, ArmorTier.Leather, ArmorTier.Bronze };

        int typeIndex = rng.Next(names.Length);
        return new UnitTemplate
        {
            unitName = names[typeIndex],
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
            unit.SetEnemy(isEnemy);
            unit.SetCommander(template.isCommander);
            unit.SetArmorTier(template.armorTier);
        }

        grid.PlaceUnit(unit, coord);

        if (turnManager != null)
            turnManager.RegisterUnit(unit);

        return unitObj;
    }
}

[System.Serializable]
public class UnitTemplate
{
    public string unitName = "Unit";
    public ArmorTier armorTier = ArmorTier.Leather;
    public bool isCommander = false;
}