using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class GameUIController : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private TurnManager turnManager;
    [SerializeField] private PlayerInputHandler inputHandler;
    [SerializeField] private CardDeckManager cardDeckManager;
    [SerializeField] private CardTurnController cardTurnController;
    [SerializeField] private RunManager runManager;

    [Header("UI Elements")]
    [SerializeField] private GameObject canvas;
    [SerializeField] private Button endTurnButton;
    [SerializeField] private Text phaseText;
    [SerializeField] private Text selectedUnitText;
    [SerializeField] private Text handSizeText;
    [SerializeField] private Text fatigueText;
    [SerializeField] private Text promptText;
    [SerializeField] private GameObject gameOverPanel;
    [SerializeField] private Text gameOverText;
    [SerializeField] private Button restartButton;
    [SerializeField] private GameObject rewardPanel;
    [SerializeField] private Button[] rewardButtons = new Button[3];

    [Header("Hand UI")]
    [SerializeField] private int maxHandButtons = 8;

    private readonly List<Button> handButtons = new List<Button>();
    private Button revealButton;
    private readonly Dictionary<CommandCard, Button> cardButtons = new Dictionary<CommandCard, Button>();

    private void Start()
    {
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
        if (inputHandler == null) inputHandler = FindObjectOfType<PlayerInputHandler>();
        if (cardDeckManager == null) cardDeckManager = FindObjectOfType<CardDeckManager>();
        if (cardTurnController == null) cardTurnController = FindObjectOfType<CardTurnController>();
        if (runManager == null) runManager = FindObjectOfType<RunManager>();

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

            endTurnButton = CreateButton("EndTurnButton", new Vector2(180, 54), new Vector2(0.5f, 0f), new Vector2(0.5f, 0f), new Vector2(0f, 300f), new Color(0.3f, 0.5f, 0.8f));
            SetButtonText(endTurnButton, "End Turn", 18);

            revealButton = CreateButton("RevealButton", new Vector2(180, 54), new Vector2(0.5f, 0f), new Vector2(0.5f, 0f), new Vector2(0f, 230f), new Color(0.8f, 0.6f, 0.2f));
            SetButtonText(revealButton, "Reveal", 18);
            revealButton.gameObject.SetActive(false);

            phaseText = CreateText("PhaseText", new Vector2(300, 40), new Vector2(0.5f, 1f), new Vector2(0.5f, 1f), new Vector2(0f, -20f));
            phaseText.fontSize = 24;
            phaseText.alignment = TextAnchor.MiddleCenter;

            promptText = CreateText("PromptText", new Vector2(600, 40), new Vector2(0.5f, 1f), new Vector2(0.5f, 1f), new Vector2(0f, -60f));
            promptText.fontSize = 18;
            promptText.alignment = TextAnchor.MiddleCenter;
            promptText.color = new Color(1f, 1f, 0.8f, 1f);

            handSizeText = CreateText("HandSizeText", new Vector2(200, 40), new Vector2(1f, 1f), new Vector2(1f, 1f), new Vector2(-20f, -20f));
            handSizeText.fontSize = 20;
            handSizeText.alignment = TextAnchor.MiddleRight;

            fatigueText = CreateText("FatigueText", new Vector2(300, 40), new Vector2(0.5f, 1f), new Vector2(0.5f, 1f), new Vector2(0f, -100f));
            fatigueText.fontSize = 18;
            fatigueText.alignment = TextAnchor.MiddleCenter;
            fatigueText.color = new Color(1f, 0.8f, 0.2f, 1f);

            selectedUnitText = CreateText("SelectedUnit", new Vector2(350, 40), new Vector2(0f, 1f), new Vector2(0f, 1f), new Vector2(20f, -20f));
            selectedUnitText.fontSize = 16;
            selectedUnitText.alignment = TextAnchor.MiddleLeft;

            gameOverPanel = CreatePanel("GameOverPanel", new Color(0f, 0f, 0f, 0.75f));
            gameOverText = CreateChildText(gameOverPanel, "GameOverText", new Vector2(500, 100), new Vector2(0.5f, 0.6f), new Vector2(0.5f, 0.6f), Vector2.zero);
            gameOverText.fontSize = 40;
            gameOverText.alignment = TextAnchor.MiddleCenter;

            restartButton = CreateChildButton(gameOverPanel, "RestartButton", new Vector2(220, 60), new Vector2(0.5f, 0.4f), new Vector2(0.5f, 0.4f), Vector2.zero, new Color(0.3f, 0.7f, 0.3f));
            SetButtonText(restartButton, "New Run", 22);
            gameOverPanel.SetActive(false);

            rewardPanel = CreatePanel("RewardPanel", new Color(0f, 0f, 0f, 0.8f));
            Text rewardTitle = CreateChildText(rewardPanel, "RewardTitle", new Vector2(400, 60), new Vector2(0.5f, 0.85f), new Vector2(0.5f, 0.85f), Vector2.zero);
            rewardTitle.text = "Choose a Reward";
            rewardTitle.fontSize = 30;
            rewardTitle.alignment = TextAnchor.MiddleCenter;

            for (int i = 0; i < 3; i++)
            {
                float xPos = (i - 1) * 240f;
                rewardButtons[i] = CreateChildButton(rewardPanel, $"RewardButton_{i}", new Vector2(220, 80),
                    new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(xPos, 0f), new Color(0.3f, 0.5f, 0.8f));
                int capture = i;
                rewardButtons[i].onClick.AddListener(() => OnRewardClicked(capture));
            }
            rewardPanel.SetActive(false);
        }

        BuildHandButtons();
    }

    private void BuildHandButtons()
    {
        for (int i = 0; i < maxHandButtons; i++)
        {
            float spacing = 150f;
            float xPos = (i - (maxHandButtons - 1) / 2f) * spacing;
            Button cardBtn = CreateChildButton(canvas, $"HandCard_{i}", new Vector2(140, 190),
                new Vector2(0.5f, 0f), new Vector2(0.5f, 0f), new Vector2(xPos, 110f), new Color(0.85f, 0.8f, 0.7f));
            cardBtn.gameObject.SetActive(false);
            int capture = i;
            cardBtn.onClick.AddListener(() => OnHandCardClicked(capture));
            handButtons.Add(cardBtn);
        }
    }

    private void SetupEvents()
    {
        if (endTurnButton != null)
            endTurnButton.onClick.AddListener(OnEndTurnClicked);

        if (revealButton != null)
            revealButton.onClick.AddListener(OnRevealClicked);

        if (restartButton != null)
            restartButton.onClick.AddListener(OnRestartClicked);

        if (turnManager != null)
        {
            turnManager.OnPlayerTurnStart.AddListener(OnPlayerTurnStarted);
            turnManager.OnAITurnStart.AddListener(OnAITurnStarted);
            turnManager.OnCardPhaseChanged.AddListener(OnCardPhaseChanged);
            turnManager.OnPhaseChanged.AddListener(OnPhaseChanged);
            turnManager.OnGameOver.AddListener(OnGameOver);
        }

        if (inputHandler != null)
        {
            inputHandler.OnUnitSelected += OnUnitSelected;
            inputHandler.OnUnitDeselected += OnUnitDeselected;
        }

        if (cardDeckManager != null)
        {
            cardDeckManager.OnHandChanged += OnHandChanged;
            cardDeckManager.OnCardLostToFatigue += OnCardLostToFatigue;
            cardDeckManager.OnCardLostToCasualty += OnCardLostToCasualty;
        }

        if (cardTurnController != null)
        {
            cardTurnController.OnSelectionUpdated += OnSelectionUpdated;
            cardTurnController.OnRevealed += OnCardsRevealed;
            cardTurnController.OnHalfResolving += OnHalfResolving;
            cardTurnController.OnResolutionComplete += OnResolutionComplete;
            cardTurnController.OnPromptChanged += OnPromptChanged;
        }
    }

    private void Update()
    {
        if (turnManager == null) return;

        if (handSizeText != null && cardDeckManager != null)
        {
            handSizeText.text = $"Hand:{cardDeckManager.GetHandCount()} Deck:{cardDeckManager.GetDeckCount()} Spent:{cardDeckManager.GetSpentCount()} Lost:{cardDeckManager.GetLostCount()}";
        }

        if (endTurnButton != null)
        {
            endTurnButton.interactable = turnManager.CanEndPlayerTurn();
        }
    }

    private void OnEndTurnClicked()
    {
        if (turnManager != null && turnManager.CanEndPlayerTurn())
        {
            if (inputHandler != null) inputHandler.DeselectUnit();
            turnManager.EndPlayerTurn();
        }
    }

    private void OnRevealClicked()
    {
        if (cardTurnController != null && cardTurnController.CanReveal())
        {
            cardTurnController.Reveal();
        }
    }

    private void OnHandCardClicked(int index)
    {
        if (cardTurnController == null) return;
        if (turnManager == null || !turnManager.IsPlayerTurn()) return;
        if (turnManager.CurrentCardPhase != CardPhase.Selection) return;

        if (index < 0 || index >= cardDeckManager.Hand.Count) return;
        cardTurnController.ToggleCardSelection(cardDeckManager.Hand[index]);
    }

    private void OnRestartClicked()
    {
        UnityEngine.SceneManagement.SceneManager.LoadScene(
            UnityEngine.SceneManagement.SceneManager.GetActiveScene().buildIndex);
    }

    private void OnPlayerTurnStarted()
    {
        if (phaseText != null) phaseText.text = "Your Turn";
    }

    private void OnAITurnStarted()
    {
        if (phaseText != null) phaseText.text = "Enemy Turn...";
        if (revealButton != null) revealButton.gameObject.SetActive(false);
        ClearHandButtons();
    }

    private void OnCardPhaseChanged(CardPhase phase)
    {
        if (phase == CardPhase.Selection)
        {
            if (revealButton != null) revealButton.gameObject.SetActive(false);
            RefreshHandDisplay();
        }
        else if (phase == CardPhase.Resolution)
        {
            if (revealButton != null) revealButton.gameObject.SetActive(false);
        }
        else if (phase == CardPhase.Done)
        {
            ClearHandButtons();
        }
    }

    private void OnPhaseChanged(TurnPhase phase)
    {
        if (phase == TurnPhase.GameOver) return;
    }

    private void OnGameOver(bool playerWon)
    {
        ClearHandButtons();
        if (revealButton != null) revealButton.gameObject.SetActive(false);

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
            selectedUnitText.text = $"{unit.UnitName} | HP: {unit.CurrentHP}/{unit.MaxHP} | {unit.UnitType}";
    }

    private void OnUnitDeselected(Unit unit)
    {
        if (selectedUnitText != null)
            selectedUnitText.text = "";
    }

    private void OnHandChanged(List<CommandCard> hand)
    {
        RefreshHandDisplay();
    }

    private void OnSelectionUpdated(List<CommandCard> selected)
    {
        RefreshHandDisplay(selected);
        if (revealButton != null)
            revealButton.gameObject.SetActive(cardTurnController != null && cardTurnController.CanReveal());
    }

    private void OnCardsRevealed(CommandCard cardA, CommandCard cardB)
    {
        ClearHandButtons();
    }

    private void OnHalfResolving(CommandCard card, CardHalf half)
    {
        if (promptText != null)
        {
            string abilityName = half == CardHalf.Top ? card.topAbilityName : card.bottomAbilityName;
            promptText.text = $"Resolving: {card.cardName} — {abilityName}";
        }
    }

    private void OnResolutionComplete()
    {
        if (promptText != null) promptText.text = "Orders complete. End your turn.";
    }

    private void OnPromptChanged(string prompt)
    {
        if (promptText != null) promptText.text = prompt;
    }

    private void OnCardLostToFatigue(CommandCard card)
    {
        if (promptText != null)
        {
            promptText.text = $"Fatigue: {card.cardName} lost!";
            Invoke("ClearPromptText", 2.0f);
        }
    }

    private void OnCardLostToCasualty(CommandCard card)
    {
        if (promptText != null)
        {
            promptText.text = $"Casualty: {card.cardName} lost!";
            Invoke("ClearPromptText", 2.0f);
        }
    }

    private void ClearPromptText()
    {
        if (promptText != null) promptText.text = "";
    }

    private void RefreshHandDisplay()
    {
        RefreshHandDisplay(null);
    }

    private void RefreshHandDisplay(List<CommandCard> selected)
    {
        if (cardDeckManager == null) return;

        List<CommandCard> hand = cardDeckManager.Hand;
        cardButtons.Clear();

        for (int i = 0; i < handButtons.Count; i++)
        {
            Button btn = handButtons[i];
            if (i >= hand.Count)
            {
                btn.gameObject.SetActive(false);
                continue;
            }

            CommandCard card = hand[i];
            btn.gameObject.SetActive(true);
            cardButtons[card] = btn;

            Text txt = btn.GetComponentInChildren<Text>();
            if (txt != null)
            {
                bool isSelected = selected != null && selected.Contains(card);
                string marker = isSelected ? "[x] " : "";
                txt.text = $"{marker}{card.cardName}\n---\nTOP: {card.topAbilityName}\n{card.topAbilityDescription}\n---\nBOT: {card.bottomAbilityName}\n{card.bottomAbilityDescription}";
                txt.fontSize = 11;
                txt.alignment = TextAnchor.UpperLeft;
                txt.color = isSelected ? Color.yellow : Color.black;
            }

            ColorBlock colors = btn.colors;
            colors.normalColor = selected != null && selected.Contains(card) ? new Color(1f, 0.9f, 0.4f) : new Color(0.85f, 0.8f, 0.7f);
            colors.highlightedColor = colors.normalColor * 1.1f;
            colors.pressedColor = colors.normalColor * 0.8f;
            btn.colors = colors;
        }
    }

    private void ClearHandButtons()
    {
        foreach (Button btn in handButtons)
        {
            btn.gameObject.SetActive(false);
        }
        cardButtons.Clear();
    }

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
        if (runManager != null)
        {
            runManager.OnRewardSelected(index);
        }
        rewardPanel.SetActive(false);
    }

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
        Text existing = button.GetComponentInChildren<Text>();
        if (existing != null)
        {
            existing.text = text;
            existing.fontSize = fontSize;
            return;
        }

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
