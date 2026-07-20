using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class RunManager : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private HexGrid grid;
    [SerializeField] private TurnManager turnManager;
    [SerializeField] private GameSetup gameSetup;
    [SerializeField] private GameUIController uiController;
    [SerializeField] private GameObject unitPrefab;
    [SerializeField] private CardDeckManager cardDeckManager;

    [Header("Run Config")]
    [SerializeField] private int battlesBeforeBoss = 3;
    [SerializeField] private int maxPlayerUnits = 6;

    private int currentBattle = 0;
    private List<UnitTemplate> currentPlayerRoster = new List<UnitTemplate>();
    private List<string> pendingRewards;
    private bool isBossBattle = false;

    private void Start()
    {
        if (grid == null) grid = FindObjectOfType<HexGrid>();
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
        if (gameSetup == null) gameSetup = FindObjectOfType<GameSetup>();
        if (uiController == null) uiController = FindObjectOfType<GameUIController>();
        if (cardDeckManager == null) cardDeckManager = FindObjectOfType<CardDeckManager>();

        if (turnManager != null)
        {
            turnManager.OnUnitDied.AddListener(OnAnyUnitDied);
            turnManager.OnGameOver.AddListener(OnBattleEnded);
        }

        currentBattle = 1;
        isBossBattle = false;
    }

    private void OnAnyUnitDied(Unit unit)
    {
        if (unit.IsEnemy) return;

        List<Unit> playerUnits = turnManager.PlayerUnits;
        bool isLastOfType = !playerUnits.Any(u => u != unit && u.UnitType == unit.UnitType && u.CurrentHP > 0);

        if (isLastOfType && cardDeckManager != null)
        {
            cardDeckManager.OnCasualty(unit.UnitType);
        }
    }

    private void OnBattleEnded(bool playerWon)
    {
        if (!playerWon) return;

        if (isBossBattle)
        {
            if (uiController != null)
            {
                uiController.ShowRewardPanel(new string[] {
                    "Run Complete!",
                    "Start New Run",
                    "View Stats"
                });
            }
            return;
        }

        currentBattle++;
        Invoke("ShowRewards", 1.0f);
    }

    private void ShowRewards()
    {
        if (uiController == null) return;

        pendingRewards = GenerateRewardOptions();
        uiController.ShowRewardPanel(pendingRewards.ToArray());
    }

    private List<string> GenerateRewardOptions()
    {
        List<string> options = new List<string>();
        System.Random rng = new System.Random();

        string[] recruitTypes = { "Swordsman", "Spearman", "Slinger", "Archer", "Scout" };
        options.Add($"Recruit: {recruitTypes[rng.Next(recruitTypes.Length)]}");

        if (currentPlayerRoster.Count > 0)
        {
            int upgradeIndex = rng.Next(currentPlayerRoster.Count);
            options.Add($"Upgrade: {currentPlayerRoster[upgradeIndex].unitName} +1 HP");
        }
        else
        {
            options.Add("Heal all units +1 HP");
        }

        options.Add("Supplies: Heal all units");

        if (cardDeckManager != null && cardDeckManager.GetLostCount() > 0)
        {
            options.Add("Recover Lost Card");
        }

        return options;
    }

    public void OnRewardSelected(int index)
    {
        if (pendingRewards == null || index < 0 || index >= pendingRewards.Count) return;

        string reward = pendingRewards[index];
        Debug.Log($"Reward selected: {reward}");
        ApplyReward(reward);
        pendingRewards = null;

        SetupNextBattle();
    }

    private void ApplyReward(string reward)
    {
        if (reward.StartsWith("Recruit:"))
        {
            string typeName = reward.Substring("Recruit:".Length).Trim();
            if (System.Enum.TryParse<UnitType>(typeName, out UnitType type) && currentPlayerRoster.Count < maxPlayerUnits)
            {
                ArmorTier tier = type == UnitType.Slinger || type == UnitType.Archer || type == UnitType.Scout
                    ? ArmorTier.Leather : ArmorTier.Bronze;
                currentPlayerRoster.Add(new UnitTemplate
                {
                    unitName = typeName,
                    unitType = type,
                    armorTier = tier,
                    isCommander = false
                });
            }
        }
        else if (reward.StartsWith("Upgrade:"))
        {
            HealAllUnits(1);
        }
        else if (reward.StartsWith("Supplies") || reward.StartsWith("Heal all"))
        {
            HealAllUnits(99);
        }
        else if (reward.Contains("Recover Lost Card") && cardDeckManager != null)
        {
            cardDeckManager.RecoverLostCard();
        }
    }

    private void HealAllUnits(int amount)
    {
        foreach (Unit unit in turnManager.PlayerUnits)
        {
            unit.Heal(amount);
        }
    }

    private void SetupNextBattle()
    {
        isBossBattle = currentBattle > battlesBeforeBoss;
        StartNewBattle();
    }

    private void StartNewBattle()
    {
        if (turnManager != null)
        {
            foreach (var unit in turnManager.PlayerUnits.ToList())
            {
                turnManager.UnregisterUnit(unit);
                Destroy(unit.gameObject);
            }
            foreach (var unit in turnManager.EnemyUnits.ToList())
            {
                turnManager.UnregisterUnit(unit);
                Destroy(unit.gameObject);
            }
        }

        if (gameSetup != null)
        {
            if (isBossBattle)
            {
                gameSetup.SpawnBossBattle(currentPlayerRoster);
            }
            else
            {
                gameSetup.SpawnBattle(currentBattle, currentPlayerRoster);
            }
        }

        if (turnManager != null)
        {
            turnManager.StartPlayerTurn();
        }
    }
}
