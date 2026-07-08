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

    [Header("Run Config")]
    [SerializeField] private int battlesBeforeBoss = 3;
    [SerializeField] private int maxPlayerUnits = 6;

    // Run state
    private int currentBattle = 0;
    private List<UnitTemplate> currentPlayerRoster = new List<UnitTemplate>();
    private bool isBossBattle = false;

    private void Start()
    {
        if (grid == null) grid = FindObjectOfType<HexGrid>();
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
        if (gameSetup == null) gameSetup = FindObjectOfType<GameSetup>();
        if (uiController == null) uiController = FindObjectOfType<GameUIController>();

        // Listen for game over
        if (turnManager != null)
        {
            turnManager.OnGameOver.AddListener(OnBattleEnded);
        }

        // Start first battle with default setup
        currentBattle = 1;
        isBossBattle = false;
    }

    private void OnBattleEnded(bool playerWon)
    {
        if (!playerWon) return;

        // Check if this was the boss battle
        if (isBossBattle)
        {
            // Player beat the boss — run complete!
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

        // Advance to next battle
        currentBattle++;

        // Show reward selection after delay
        Invoke("ShowRewards", 1.0f);
    }

    private void ShowRewards()
    {
        if (uiController == null) return;

        // Generate 3 random reward options
        string[] options = GenerateRewardOptions();
        uiController.ShowRewardPanel(options);
    }

    private string[] GenerateRewardOptions()
    {
        List<string> options = new List<string>();
        System.Random rng = new System.Random();

        // Option 1: Recruit a new unit
        string[] recruitTypes = { "Swordsman", "Spearman", "Slinger", "Archer", "Scout" };
        options.Add($"Recruit: {recruitTypes[rng.Next(recruitTypes.Length)]}");

        // Option 2: Upgrade a random existing unit
        if (currentPlayerRoster.Count > 0)
        {
            int upgradeIndex = rng.Next(currentPlayerRoster.Count);
            options.Add($"Upgrade: {currentPlayerRoster[upgradeIndex].unitName} +1 HP");
        }
        else
        {
            options.Add("Heal all units +1 HP");
        }

        // Option 3: Supplies (heal)
        options.Add("Supplies: Heal all units");

        return options.ToArray();
    }

    public void OnRewardSelected(int index, string rewardDescription)
    {
        // Apply the reward
        Debug.Log($"Reward selected: {rewardDescription}");

        // Start the next battle
        SetupNextBattle();
    }

    private void SetupNextBattle()
    {
        // Determine if this is the boss battle
        isBossBattle = currentBattle > battlesBeforeBoss;

        // Save current player roster from game setup
        // (In a full implementation, we'd track individual unit HP/upgrades)

        // Reload the scene or reset the grid for the next battle
        // For now, we just restart the setup
        StartNewBattle();
    }

    private void StartNewBattle()
    {
        // Clear existing units
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

        // Clear grid
        if (grid != null)
        {
            // Grid tiles stay, just units are cleared
        }

        // Spawn new battle based on currentBattle
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

        // Start the turn cycle
        if (turnManager != null)
        {
            turnManager.StartPlayerTurn();
        }
    }
}