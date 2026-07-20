using System;
using System.Collections.Generic;
using UnityEngine;

public class CardTurnController : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private CardDeckManager cardDeckManager;
    [SerializeField] private CardAbilityResolver resolver;
    [SerializeField] private TurnManager turnManager;
    [SerializeField] private PlayerInputHandler inputHandler;
    [SerializeField] private HexGrid grid;

    public event Action<List<CommandCard>> OnSelectionUpdated;
    public event Action<CommandCard, CommandCard> OnRevealed;
    public event Action<CommandCard, CardHalf> OnHalfResolving;
    public event Action OnResolutionComplete;
    public event Action<string> OnPromptChanged;

    private CommandCard cardA;
    private CommandCard cardB;
    private readonly List<CommandCard> selectedCards = new List<CommandCard>();

    private int resolvingHalfIndex = 0;
    private readonly List<Unit> halfSelection = new List<Unit>();
    private int destinationIndex = 0;
    private readonly List<GameObject> highlightObjects = new List<GameObject>();

    public bool IsAwaitingInput => turnManager != null && turnManager.CurrentCardPhase == CardPhase.Resolution
                                   && resolvingHalfIndex <= 1 && !AwaitingConfirmation;

    public bool AwaitingConfirmation { get; private set; }

    private void Start()
    {
        if (cardDeckManager == null) cardDeckManager = FindObjectOfType<CardDeckManager>();
        if (resolver == null) resolver = FindObjectOfType<CardAbilityResolver>();
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
        if (inputHandler == null) inputHandler = FindObjectOfType<PlayerInputHandler>();
        if (grid == null) grid = FindObjectOfType<HexGrid>();

        if (turnManager != null)
        {
            turnManager.OnCardPhaseChanged.AddListener(OnCardPhaseChanged);
        }
    }

    private void OnCardPhaseChanged(CardPhase phase)
    {
        if (phase == CardPhase.Selection)
        {
            BeginSelection();
        }
        else if (phase == CardPhase.Resolution)
        {
            BeginResolution();
        }
        else
        {
            cardA = null;
            cardB = null;
            selectedCards.Clear();
            resolver.EndResolution();
        }
    }

    private void BeginSelection()
    {
        cardA = null;
        cardB = null;
        selectedCards.Clear();
        resolver.EndResolution();
        OnSelectionUpdated?.Invoke(selectedCards);
        OnPromptChanged?.Invoke("Choose 2 Command Cards");
    }

    public List<CommandCard> GetHand()
    {
        return cardDeckManager != null ? cardDeckManager.Hand : new List<CommandCard>();
    }

    public void ToggleCardSelection(CommandCard card)
    {
        if (turnManager == null || turnManager.CurrentCardPhase != CardPhase.Selection) return;
        if (card == null || !cardDeckManager.Hand.Contains(card)) return;

        if (selectedCards.Contains(card))
        {
            selectedCards.Remove(card);
        }
        else
        {
            if (selectedCards.Count >= 2) return;
            selectedCards.Add(card);
        }

        OnSelectionUpdated?.Invoke(selectedCards);

        if (selectedCards.Count == 2)
        {
            OnPromptChanged?.Invoke("Reveal your orders!");
        }
        else
        {
            OnPromptChanged?.Invoke("Choose 2 Command Cards");
        }
    }

    public bool CanReveal()
    {
        return selectedCards.Count == 2;
    }

    public void Reveal()
    {
        if (!CanReveal()) return;

        cardA = selectedCards[0];
        cardB = selectedCards[1];

        OnRevealed?.Invoke(cardA, cardB);
        turnManager.SetCardPhase(CardPhase.Resolution);
    }

    private void BeginResolution()
    {
        resolvingHalfIndex = 0;
        destinationIndex = 0;
        halfSelection.Clear();
        StartHalf();
    }

    private void StartHalf()
    {
        CommandCard card = resolvingHalfIndex == 0 ? cardA : cardB;
        CardHalf half = resolvingHalfIndex == 0 ? CardHalf.Top : CardHalf.Bottom;

        resolver.BeginResolution(card, half);
        halfSelection.Clear();
        destinationIndex = 0;
        AwaitingConfirmation = false;

        OnHalfResolving?.Invoke(card, half);
        PromptForSelection(card, half);
    }

    private void PromptForSelection(CommandCard card, CardHalf half)
    {
        List<Unit> valid = resolver.GetValidTargets();
        CardEffectType effect = resolver.GetCurrentEffect();
        string abilityName = half == CardHalf.Top ? card.topAbilityName : card.bottomAbilityName;

        if (valid.Count == 0)
        {
            OnPromptChanged?.Invoke($"No valid units for {abilityName} — skipping.");
            CompleteHalf();
            return;
        }

        int maxActivations = Math.Min(resolver.CurrentMaxActivations, valid.Count);
        OnPromptChanged?.Invoke($"Tap up to {maxActivations} unit(s) to {abilityName}");
    }

    public void OnUnitClicked(Unit unit)
    {
        if (turnManager == null || turnManager.CurrentCardPhase != CardPhase.Resolution) return;
        if (resolvingHalfIndex > 1) return;

        List<Unit> valid = resolver.GetValidTargets();
        if (!valid.Contains(unit)) return;

        if (!halfSelection.Contains(unit))
        {
            int max = resolver.CurrentMaxActivations;
            if (halfSelection.Count >= max) return;
            halfSelection.Add(unit);
            UnitVisual visual = unit.GetComponent<UnitVisual>();
            if (visual != null) visual.SetSelected(true);
        }

        int maxActivations = Math.Min(resolver.CurrentMaxActivations, valid.Count);
        if (halfSelection.Count < maxActivations) return;

        CardEffectType effect = resolver.GetCurrentEffect();
        if (effect == CardEffectType.Move || effect == CardEffectType.MultiMove)
        {
            destinationIndex = 0;
            ShowNextMoveTarget();
        }
        else
        {
            ResolveCurrentHalf();
        }
    }

    private void ShowNextMoveTarget()
    {
        ClearHighlights();
        if (destinationIndex < 0 || destinationIndex >= halfSelection.Count) return;

        Unit unit = halfSelection[destinationIndex];
        List<HexCoord> validMoves = resolver.GetValidMoveHexes(unit);
        foreach (HexCoord hex in validMoves)
        {
            ShowHighlight(hex, new Color(0.2f, 0.8f, 0.3f, 0.4f));
        }

        OnPromptChanged?.Invoke($"Move {unit.UnitName} — tap a green hex");
    }

    public void OnHexClicked(HexCoord hex)
    {
        if (turnManager == null || turnManager.CurrentCardPhase != CardPhase.Resolution) return;
        if (resolvingHalfIndex > 1) return;

        CardEffectType effect = resolver.GetCurrentEffect();
        if (effect != CardEffectType.Move && effect != CardEffectType.MultiMove) return;
        if (destinationIndex < 0 || destinationIndex >= halfSelection.Count) return;

        Unit unit = halfSelection[destinationIndex];
        List<HexCoord> validMoves = resolver.GetValidMoveHexes(unit);
        if (!validMoves.Contains(hex)) return;

        resolver.ResolveMove(unit, hex);
        UnitVisual visual = unit.GetComponent<UnitVisual>();
        if (visual != null) visual.SetSelected(false);

        destinationIndex++;
        if (destinationIndex >= halfSelection.Count)
        {
            ClearHighlights();
            ResolveCurrentHalf();
        }
        else
        {
            ShowNextMoveTarget();
        }
    }

    private void ResolveCurrentHalf()
    {
        CardEffectType effect = resolver.GetCurrentEffect();

        foreach (Unit unit in halfSelection)
        {
            switch (effect)
            {
                case CardEffectType.Attack:
                case CardEffectType.MultiAttack:
                    Unit target = resolver.FindAttackTarget(unit);
                    if (target != null) resolver.ResolveAttack(unit, target);
                    break;
                case CardEffectType.Heal:
                case CardEffectType.Buff:
                    resolver.ResolveBuff(unit);
                    break;
                case CardEffectType.Move:
                case CardEffectType.MultiMove:
                    break;
            }
        }

        foreach (Unit unit in halfSelection)
        {
            UnitVisual visual = unit.GetComponent<UnitVisual>();
            if (visual != null) visual.SetSelected(false);
        }

        CompleteHalf();
    }

    private void CompleteHalf()
    {
        CommandCard card = resolvingHalfIndex == 0 ? cardA : cardB;
        if (card != null)
        {
            cardDeckManager.PlayCard(card);
        }

        resolver.EndResolution();
        halfSelection.Clear();
        destinationIndex = 0;
        resolvingHalfIndex++;

        if (resolvingHalfIndex >= 2)
        {
            FinishTurn();
        }
        else
        {
            StartHalf();
        }
    }

    private void FinishTurn()
    {
        OnResolutionComplete?.Invoke();
        OnPromptChanged?.Invoke("Orders complete — end your turn.");
        turnManager.SetCardPhase(CardPhase.Done);
    }

    #region Highlight Visualization

    private void ShowHighlight(HexCoord hex, Color color)
    {
        if (grid == null) return;

        Vector3 worldPos = grid.HexToWorldPosition(hex);
        worldPos.y = 0.02f;

        GameObject highlight = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        highlight.name = "CardHighlight";
        highlight.transform.position = worldPos;
        highlight.transform.localScale = new Vector3(0.5f, 0.02f, 0.5f);

        Renderer renderer = highlight.GetComponent<Renderer>();
        Material mat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
        mat.color = color;
        mat.SetFloat("_Metallic", 0f);
        mat.SetFloat("_Smoothness", 0.1f);
        renderer.material = mat;

        highlightObjects.Add(highlight);
    }

    private void ClearHighlights()
    {
        foreach (GameObject obj in highlightObjects)
        {
            Destroy(obj);
        }
        highlightObjects.Clear();
    }

    #endregion
}
