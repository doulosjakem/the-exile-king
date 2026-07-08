using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class GameUIController : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private TurnManager turnManager;
    [SerializeField] private PlayerInputHandler inputHandler;

    [Header("UI Elements")]
    [SerializeField] private GameObject canvas;
    [SerializeField] private Button endTurnButton;
    [SerializeField] private Button overworkButton;
    [SerializeField] private Text actionsRemainingText;
    [SerializeField] private Text phaseText;
    [SerializeField] private Text selectedUnitText;
    [SerializeField] private GameObject gameOverPanel;
    [SerializeField] private Text gameOverText;
    [SerializeField] private Button restartButton;
    [SerializeField] private GameObject rewardPanel;
    [SerializeField] private Button[] rewardButtons = new Button[3];

    private void Start()
    {
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
        if (inputHandler == null) inputHandler = FindObjectOfType<PlayerInputHandler>();

        CreateUI();
        SetupEvents();
    }

    private void CreateUI()
    {
        if (canvas == null)
        {
            canvas = new GameObject("GameCanvas");
            Canvas c = canvas.AddComponent<Canvas>();
            c.renderMode = RenderMode.ScreenSpaceOverlay;
            CanvasScaler scaler = canvas.AddComponent<CanvasScaler>();
            scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = new Vector2(1125, 2436);
            canvas.AddComponent<GraphicRaycaster>();

            if (FindObjectOfType<EventSystem>() == null)
            {
                GameObject es = new GameObject("EventSystem");
                es.AddComponent<EventSystem>();
                es.AddComponent<StandaloneInputModule>();
            }

            // --- End Turn Button ---
            endTurnButton = CreateButton("EndTurnButton", new Vector2(160, 50), new Vector2(0.5f, 0f), new Vector2(0.5f, 0f), new Vector2(0f, 30f), new Color(0.3f, 0.5f, 0.8f));
            SetButtonText(endTurnButton, "End Turn", 18);

            // --- Overwork Button ---
            overworkButton = CreateButton("OverworkButton", new Vector2(160, 50), new Vector2(0.5f, 0f), new Vector2(0.5f, 0f), new Vector2(0f, 90f), new Color(0.8f, 0.5f, 0.2f));
            SetButtonText(overworkButton, "Overwork", 16);
            overworkButton.gameObject.SetActive(false);

            // --- Actions Remaining ---
            actionsRemainingText = CreateText("ActionsRemaining", new Vector2(200, 40), new Vector2(1f, 1f), new Vector2(1f, 1f), new Vector2(-20f, -20f));
            actionsRemainingText.fontSize = 20;
            actionsRemainingText.alignment = TextAnchor.MiddleRight;

            // --- Phase Text ---
            phaseText = CreateText("PhaseText", new Vector2(300, 40), new Vector2(0.5f, 1f), new Vector2(0.5f, 1f), new Vector2(0f, -20f));
            phaseText.fontSize = 24;
            phaseText.alignment = TextAnchor.MiddleCenter;

            // --- Selected Unit ---
            selectedUnitText = CreateText("SelectedUnit", new Vector2(350, 40), new Vector2(0f, 1f), new Vector2(0f, 1f), new Vector2(20f, -20f));
            selectedUnitText.fontSize = 16;
            selectedUnitText.alignment = TextAnchor.MiddleLeft;

            // --- Game Over Panel ---
            gameOverPanel = CreatePanel("GameOverPanel", new Color(0f, 0f, 0f, 0.75f));
            gameOverText = CreateChildText(gameOverPanel, "GameOverText", new Vector2(500, 100), new Vector2(0.5f, 0.6f), new Vector2(0.5f, 0.6f), Vector2.zero);
            gameOverText.fontSize = 40;
            gameOverText.alignment = TextAnchor.MiddleCenter;

            restartButton = CreateChildButton(gameOverPanel, "RestartButton", new Vector2(220, 60), new Vector2(0.5f, 0.4f), new Vector2(0.5f, 0.4f), Vector2.zero, new Color(0.3f, 0.7f, 0.3f));
            SetButtonText(restartButton, "New Run", 22);
            gameOverPanel.SetActive(false);

            // --- Reward Panel ---
            rewardPanel = CreatePanel("RewardPanel", new Color(0f, 0f, 0f, 0.8f));
            Text rewardTitle = CreateChildText(rewardPanel, "RewardTitle", new Vector2(400, 60), new Vector2(0.5f, 0.85f), new Vector2(0.5f, 0.85f), Vector2.zero);
            rewardTitle.text = "Choose a Reward";
            rewardTitle.fontSize = 30;
            rewardTitle.alignment = TextAnchor.MiddleCenter;

            for (int i = 0; i < 3; i++)
            {
                float xPos = (i - 1) * 220f;
                rewardButtons[i] = CreateChildButton(rewardPanel, $"RewardButton_{i}", new Vector2(200, 80),
                    new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(xPos, 0f), new Color(0.3f, 0.5f, 0.8f));
                int capture = i;
                rewardButtons[i].onClick.AddListener(() => OnRewardClicked(capture));
            }
            rewardPanel.SetActive(false);

            // --- Damage Popup Pool ---
            // Will be created on demand by DamagePopup.cs
        }
    }

    private void SetupEvents()
    {
        if (endTurnButton != null)
            endTurnButton.onClick.AddListener(OnEndTurnClicked);

        if (overworkButton != null)
            overworkButton.onClick.AddListener(OnOverworkClicked);

        if (restartButton != null)
            restartButton.onClick.AddListener(OnRestartClicked);

        if (turnManager != null)
        {
            turnManager.OnPlayerTurnStart.AddListener(OnPlayerTurnStarted);
            turnManager.OnAITurnStart.AddListener(OnAITurnStarted);
            turnManager.OnPhaseChanged.AddListener(OnPhaseChanged);
            turnManager.OnGameOver.AddListener(OnGameOver);
        }

        if (inputHandler != null)
        {
            inputHandler.OnUnitSelected += OnUnitSelected;
            inputHandler.OnUnitDeselected += OnUnitDeselected;
        }
    }

    private void Update()
    {
        if (turnManager == null) return;

        if (turnManager.IsPlayerTurn())
        {
            if (actionsRemainingText != null)
                actionsRemainingText.text = $"Actions: {turnManager.RemainingPlayerActions}";

            // Show Overwork button if 0 actions left and David can still act
            bool showOverwork = turnManager.RemainingPlayerActions <= 0;
            if (showOverwork && inputHandler != null)
            {
                Unit selected = inputHandler.GetSelectedUnit();
                showOverwork = selected != null && selected.IsCommander && !selected.IsEnemy && selected.CanAct();
            }
            if (overworkButton != null)
                overworkButton.gameObject.SetActive(showOverwork);
        }
    }

    private void OnEndTurnClicked()
    {
        if (turnManager != null && turnManager.IsPlayerTurn())
        {
            if (inputHandler != null) inputHandler.DeselectUnit();
            turnManager.EndPlayerTurn();
        }
    }

    private void OnOverworkClicked()
    {
        if (turnManager == null || !turnManager.IsPlayerTurn()) return;
        if (inputHandler == null) return;

        Unit selected = inputHandler.GetSelectedUnit();
        if (selected != null && selected.IsCommander && !selected.IsEnemy && selected.CanAct())
        {
            // Perform Overwork: David attacks or does something, then skips next turn
            // For simplicity, we just spend the overwork action and deselect
            inputHandler.DeselectUnit();
            turnManager.SpendOverworkAction(selected);
        }
    }

    private void OnRestartClicked()
    {
        UnityEngine.SceneManagement.SceneManager.LoadScene(
            UnityEngine.SceneManagement.SceneManager.GetActiveScene().buildIndex);
    }

    private void OnPlayerTurnStarted()
    {
        if (phaseText != null) phaseText.text = "Your Turn";
        if (overworkButton != null) overworkButton.gameObject.SetActive(false);
    }

    private void OnAITurnStarted()
    {
        if (phaseText != null) phaseText.text = "Enemy Turn...";
        if (overworkButton != null) overworkButton.gameObject.SetActive(false);
    }

    private void OnPhaseChanged(TurnPhase phase)
    {
        if (phase == TurnPhase.GameOver) return;
    }

    private void OnGameOver(bool playerWon)
    {
        if (gameOverPanel != null)
        {
            gameOverPanel.SetActive(true);
            if (gameOverText != null)
                gameOverText.text = playerWon ? "Victory!" : "Defeat";
        }
    }

    private void OnUnitSelected(Unit unit)
    {
        if (selectedUnitText != null)
            selectedUnitText.text = $"{unit.UnitName} | HP: {unit.CurrentHP}/{unit.MaxHP} | {unit.CurrentState}";
    }

    private void OnUnitDeselected(Unit unit)
    {
        if (selectedUnitText != null)
            selectedUnitText.text = "";
    }

    // --- Reward System ---
    public void ShowRewardPanel(string[] options)
    {
        if (rewardPanel == null) return;
        rewardPanel.SetActive(true);

        for (int i = 0; i < 3 && i < rewardButtons.Length; i++)
        {
            if (i < options.Length)
            {
                rewardButtons[i].gameObject.SetActive(true);
                SetButtonText(rewardButtons[i], options[i], 16);
            }
            else
            {
                rewardButtons[i].gameObject.SetActive(false);
            }
        }
    }

    private void OnRewardClicked(int index)
    {
        rewardPanel.SetActive(false);
        // The RunManager will handle the reward application
        // This event is wired up externally
    }

    // --- Factory Methods ---
    private GameObject CreatePanel(string name, Color color)
    {
        GameObject obj = new GameObject(name);
        obj.transform.SetParent(canvas.transform, false);
        Image img = obj.AddComponent<Image>();
        img.color = color;

        RectTransform rect = obj.GetComponent<RectTransform>();
        rect.anchorMin = Vector2.zero;
        rect.anchorMax = Vector2.one;
        rect.sizeDelta = Vector2.zero;
        return obj;
    }

    private Button CreateButton(string name, Vector2 size, Vector2 anchorMin, Vector2 anchorMax, Vector2 position, Color color)
    {
        GameObject obj = new GameObject(name);
        obj.transform.SetParent(canvas.transform, false);

        RectTransform rect = obj.AddComponent<RectTransform>();
        rect.anchorMin = anchorMin;
        rect.anchorMax = anchorMax;
        rect.sizeDelta = size;
        rect.anchoredPosition = position;

        Image img = obj.AddComponent<Image>();
        img.color = color;

        Button button = obj.AddComponent<Button>();
        ColorBlock colors = button.colors;
        colors.normalColor = color;
        colors.highlightedColor = color * 1.2f;
        colors.pressedColor = color * 0.8f;
        button.colors = colors;

        return button;
    }

    private Button CreateChildButton(GameObject parent, string name, Vector2 size, Vector2 anchorMin, Vector2 anchorMax, Vector2 position, Color color)
    {
        GameObject obj = new GameObject(name);
        obj.transform.SetParent(parent.transform, false);

        RectTransform rect = obj.AddComponent<RectTransform>();
        rect.anchorMin = anchorMin;
        rect.anchorMax = anchorMax;
        rect.sizeDelta = size;
        rect.anchoredPosition = position;

        Image img = obj.AddComponent<Image>();
        img.color = color;

        Button button = obj.AddComponent<Button>();
        ColorBlock colors = button.colors;
        colors.normalColor = color;
        colors.highlightedColor = color * 1.2f;
        colors.pressedColor = color * 0.8f;
        button.colors = colors;

        return button;
    }

    private void SetButtonText(Button button, string text, int fontSize)
    {
        GameObject textObj = new GameObject("Text");
        textObj.transform.SetParent(button.transform, false);
        Text t = textObj.AddComponent<Text>();
        t.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
        t.text = text;
        t.fontSize = fontSize;
        t.color = Color.white;
        t.alignment = TextAnchor.MiddleCenter;

        RectTransform textRect = textObj.GetComponent<RectTransform>();
        textRect.anchorMin = Vector2.zero;
        textRect.anchorMax = Vector2.one;
        textRect.sizeDelta = Vector2.zero;
    }

    private Text CreateText(string name, Vector2 size, Vector2 anchorMin, Vector2 anchorMax, Vector2 position)
    {
        GameObject obj = new GameObject(name);
        obj.transform.SetParent(canvas.transform, false);

        RectTransform rect = obj.AddComponent<RectTransform>();
        rect.anchorMin = anchorMin;
        rect.anchorMax = anchorMax;
        rect.sizeDelta = size;
        rect.anchoredPosition = position;

        Text text = obj.AddComponent<Text>();
        text.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
        text.color = Color.white;
        text.text = "";
        return text;
    }

    private Text CreateChildText(GameObject parent, string name, Vector2 size, Vector2 anchorMin, Vector2 anchorMax, Vector2 position)
    {
        GameObject obj = new GameObject(name);
        obj.transform.SetParent(parent.transform, false);

        RectTransform rect = obj.AddComponent<RectTransform>();
        rect.anchorMin = anchorMin;
        rect.anchorMax = anchorMax;
        rect.sizeDelta = size;
        rect.anchoredPosition = position;

        Text text = obj.AddComponent<Text>();
        text.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
        text.color = Color.white;
        text.text = "";
        return text;
    }
}