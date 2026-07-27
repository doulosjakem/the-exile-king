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
    public List<CommandCard> SpentPile { get; private set; } = new List<CommandCard>();
    public List<CommandCard> LostPile { get; private set; } = new List<CommandCard>();
    private readonly List<CommandCard>[] hands;
    private const int PlayerCount = 2;

    public event Action<int, List<CommandCard>> OnHandChanged;
    public event Action<int> OnDeckRefreshed;
    public event Action<int, CommandCard> OnCardLostToFatigue;
    public event Action<int, CommandCard> OnCardLostToCasualty;
    public event Action<int, UnitType> OnCasualtyTriggered;

    public int GetHandCount(int playerIndex) => hands != null && playerIndex >= 0 && playerIndex < PlayerCount ? hands[playerIndex].Count : 0;
    public List<CommandCard> GetHand(int playerIndex) => hands != null && playerIndex >= 0 && playerIndex < PlayerCount ? hands[playerIndex] : new List<CommandCard>();
    public List<CommandCard> Hand => GetHand(0);
    public int GetDeckCount() => Deck.Count;
    public int GetSpentCount() => SpentPile.Count;
    public int GetLostCount() => LostPile.Count;

    private void Awake()
    {
        hands = new List<CommandCard>[PlayerCount];
        for (int i = 0; i < PlayerCount; i++)
        {
            hands[i] = new List<CommandCard>();
        }
    }

    private System.Random rng = new System.Random();

    private void Start()
    {
        if (turnManager == null) turnManager = FindObjectOfType<TurnManager>();
    }

    public void InitializeDeck(List<CommandCard> startingCards)
    {
        Deck.Clear();
        for (int i = 0; i < PlayerCount; i++) hands[i].Clear();
        SpentPile.Clear();
        LostPile.Clear();

        foreach (CommandCard card in startingCards)
        {
            Deck.Add(card);
        }

        ShuffleDeck();

        for (int i = 0; i < 2 && i < Deck.Count; i++)
        {
            hands[0].Add(Deck[0]);
            Deck.RemoveAt(0);
        }

        OnHandChanged?.Invoke(0, hands[0]);
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

    public void DrawToHandSize(int playerIndex, int targetSize)
    {
        if (playerIndex < 0 || playerIndex >= PlayerCount) return;
        List<CommandCard> hand = hands[playerIndex];

        while (hand.Count < targetSize && (Deck.Count > 0 || SpentPile.Count > 0))
        {
            if (Deck.Count == 0)
            {
                RefreshDeckFromSpent();
            }

            if (Deck.Count > 0)
            {
                hand.Add(Deck[0]);
                Deck.RemoveAt(0);
            }
        }

        OnHandChanged?.Invoke(playerIndex, hand);
    }

    public void RefreshDeckFromSpent()
    {
        if (SpentPile.Count == 0) return;

        Deck.AddRange(SpentPile);
        SpentPile.Clear();
        ShuffleDeck();
        OnDeckRefreshed?.Invoke(Deck.Count);
    }

    public bool PlayCard(int playerIndex, CommandCard card)
    {
        if (playerIndex < 0 || playerIndex >= PlayerCount) return false;
        List<CommandCard> hand = hands[playerIndex];
        if (!hand.Contains(card)) return false;

        hand.Remove(card);

        if (card.isLostOnUse)
        {
            LostPile.Add(card);
        }
        else
        {
            SpentPile.Add(card);
        }

        OnHandChanged?.Invoke(playerIndex, hand);
        return true;
    }

    public void DiscardToSpent(int playerIndex, CommandCard card)
    {
        if (playerIndex < 0 || playerIndex >= PlayerCount) return;
        List<CommandCard> hand = hands[playerIndex];
        if (hand.Contains(card))
        {
            hand.Remove(card);
            SpentPile.Add(card);
            OnHandChanged?.Invoke(playerIndex, hand);
        }
    }

    public void DiscardToLost(int playerIndex, CommandCard card)
    {
        if (playerIndex < 0 || playerIndex >= PlayerCount) return;
        List<CommandCard> hand = hands[playerIndex];
        if (hand.Contains(card))
        {
            hand.Remove(card);
            LostPile.Add(card);
            OnHandChanged?.Invoke(playerIndex, hand);
        }
    }

    public void OnCasualty(UnitType eliminatedType)
    {
        CommandCard cardToRemove = FindCardForCasualty(eliminatedType);

        if (cardToRemove != null)
        {
            RemoveCardFromAllPiles(cardToRemove);
            LostPile.Add(cardToRemove);
            OnCardLostToCasualty?.Invoke(Array.IndexOf(hands, GetHandContainingCard(cardToRemove)), cardToRemove);
            OnCasualtyTriggered?.Invoke(Array.IndexOf(hands, GetHandContainingCard(cardToRemove)), eliminatedType);
        }
    }

    private List<CommandCard> GetHandContainingCard(CommandCard card)
    {
        for (int i = 0; i < PlayerCount; i++)
        {
            if (hands[i].Contains(card)) return hands[i];
        }
        return null;
    }

    private CommandCard FindCardForCasualty(UnitType eliminatedType)
    {
        foreach (CommandCard card in Deck)
        {
            if (card.MatchesUnitType(eliminatedType))
                return card;
        }

        for (int i = 0; i < PlayerCount; i++)
        {
            foreach (CommandCard card in hands[i])
            {
                if (card.MatchesUnitType(eliminatedType))
                    return card;
            }
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
        for (int i = 0; i < PlayerCount; i++)
        {
            hands[i].Remove(card);
        }
        SpentPile.Remove(card);
    }

    public void ApplyFatigue(int playerIndex)
    {
        if (playerIndex < 0 || playerIndex >= PlayerCount) return;
        List<CommandCard> hand = hands[playerIndex];
        if (hand.Count == 0) return;

        int index = rng.Next(hand.Count);
        CommandCard fatiguedCard = hand[index];
        hand.RemoveAt(index);
        LostPile.Add(fatiguedCard);

        OnHandChanged?.Invoke(playerIndex, hand);
        OnCardLostToFatigue?.Invoke(playerIndex, fatiguedCard);
    }

    public CommandCard RecoverLostCard(int playerIndex)
    {
        if (LostPile.Count == 0) return null;
        if (playerIndex < 0 || playerIndex >= PlayerCount) return null;

        int index = rng.Next(LostPile.Count);
        CommandCard recovered = LostPile[index];
        LostPile.RemoveAt(index);
        hands[playerIndex].Add(recovered);

        OnHandChanged?.Invoke(playerIndex, hands[playerIndex]);
        return recovered;
    }

    public bool IsCardAvailable(CommandCard card)
    {
        if (Deck.Contains(card)) return true;
        if (SpentPile.Contains(card)) return true;
        for (int i = 0; i < PlayerCount; i++)
        {
            if (hands[i].Contains(card)) return true;
        }
        return false;
    }

    public int GetDeckCount() => Deck.Count;
    public int GetHandCount() => Hand.Count;
    public int GetSpentCount() => SpentPile.Count;
    public int GetLostCount() => LostPile.Count;
}
