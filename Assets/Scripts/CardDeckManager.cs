using System;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class CardDeckManager : MonoBehaviour
{
    [Header("Deck Settings")]
    [SerializeField] private int handSize = 4;

    [Header("References")]
    [SerializeField] private TurnManager turnManager;

    public List<CommandCard> Deck { get; private set; } = new List<CommandCard>();
    public List<CommandCard> Hand { get; private set; } = new List<CommandCard>();
    public List<CommandCard> SpentPile { get; private set; } = new List<CommandCard>();
    public List<CommandCard> LostPile { get; private set; } = new List<CommandCard>();

    public event Action<List<CommandCard>> OnHandChanged;
    public event Action<int> OnDeckRefreshed;
    public event Action<CommandCard> OnCardLostToFatigue;
    public event Action<CommandCard> OnCardLostToCasualty;
    public event Action<UnitType> OnCasualtyTriggered;

    private System.Random rng = new System.Random();

    private void Start()
    {
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
    }

    public void InitializeDeck(List<CommandCard> startingCards)
    {
        Deck.Clear();
        Hand.Clear();
        SpentPile.Clear();
        LostPile.Clear();

        foreach (CommandCard card in startingCards)
        {
            Deck.Add(card);
        }

        ShuffleDeck();

        for (int i = 0; i < 2 && i < Deck.Count; i++)
        {
            Hand.Add(Deck[0]);
            Deck.RemoveAt(0);
        }

        OnHandChanged?.Invoke(Hand);
    }

    public void ShuffleDeck()
    {
        for (int i = 0; i < Deck.Count; i++)
        {
            CommandCard temp = Deck[i];
            int randomIndex = rng.Next(Deck.Count);
            Deck[i] = Deck[randomIndex];
            Deck[randomIndex] = temp;
        }
    }

    public void DrawToHandSize(int targetSize)
    {
        while (Hand.Count < targetSize && (Deck.Count > 0 || SpentPile.Count > 0))
        {
            if (Deck.Count == 0)
            {
                RefreshDeckFromSpent();
            }

            if (Deck.Count > 0)
            {
                Hand.Add(Deck[0]);
                Deck.RemoveAt(0);
            }
        }

        OnHandChanged?.Invoke(Hand);
    }

    public void RefreshDeckFromSpent()
    {
        if (SpentPile.Count == 0) return;

        Deck.AddRange(SpentPile);
        SpentPile.Clear();
        ShuffleDeck();
        OnDeckRefreshed?.Invoke(Deck.Count);
    }

    public bool PlayCard(CommandCard card)
    {
        if (!Hand.Contains(card)) return false;

        Hand.Remove(card);

        if (card.isLostOnUse)
        {
            LostPile.Add(card);
        }
        else
        {
            SpentPile.Add(card);
        }

        OnHandChanged?.Invoke(Hand);
        return true;
    }

    public void DiscardToSpent(CommandCard card)
    {
        if (Hand.Contains(card))
        {
            Hand.Remove(card);
            SpentPile.Add(card);
            OnHandChanged?.Invoke(Hand);
        }
    }

    public void DiscardToLost(CommandCard card)
    {
        if (Hand.Contains(card))
        {
            Hand.Remove(card);
            LostPile.Add(card);
            OnHandChanged?.Invoke(Hand);
        }
    }

    public void OnCasualty(UnitType eliminatedType)
    {
        CommandCard cardToRemove = FindCardForCasualty(eliminatedType);

        if (cardToRemove != null)
        {
            RemoveCardFromAllPiles(cardToRemove);
            LostPile.Add(cardToRemove);
            OnCardLostToCasualty?.Invoke(cardToRemove);
            OnCasualtyTriggered?.Invoke(eliminatedType);
        }
    }

    private CommandCard FindCardForCasualty(UnitType eliminatedType)
    {
        foreach (CommandCard card in Deck)
        {
            if (card.MatchesUnitType(eliminatedType))
                return card;
        }

        foreach (CommandCard card in Hand)
        {
            if (card.MatchesUnitType(eliminatedType))
                return card;
        }

        foreach (CommandCard card in SpentPile)
        {
            if (card.MatchesUnitType(eliminatedType))
                return card;
        }

        return null;
    }

    private void RemoveCardFromAllPiles(CommandCard card)
    {
        Deck.Remove(card);
        Hand.Remove(card);
        SpentPile.Remove(card);
    }

    public void ApplyFatigue()
    {
        if (Hand.Count == 0) return;

        int index = rng.Next(Hand.Count);
        CommandCard fatiguedCard = Hand[index];
        Hand.RemoveAt(index);
        LostPile.Add(fatiguedCard);

        OnHandChanged?.Invoke(Hand);
        OnCardLostToFatigue?.Invoke(fatiguedCard);
    }

    public CommandCard RecoverLostCard()
    {
        if (LostPile.Count == 0) return null;

        int index = rng.Next(LostPile.Count);
        CommandCard recovered = LostPile[index];
        LostPile.RemoveAt(index);
        Hand.Add(recovered);

        OnHandChanged?.Invoke(Hand);
        return recovered;
    }

    public bool IsCardAvailable(CommandCard card)
    {
        return Hand.Contains(card) || Deck.Contains(card) || SpentPile.Contains(card);
    }

    public int GetDeckCount() => Deck.Count;
    public int GetHandCount() => Hand.Count;
    public int GetSpentCount() => SpentPile.Count;
    public int GetLostCount() => LostPile.Count;
}
