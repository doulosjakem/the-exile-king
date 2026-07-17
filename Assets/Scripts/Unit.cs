using System;
using UnityEngine;

public enum ArmorTier
{
    Leather,
    Bronze,
    Iron
}

public class Unit : MonoBehaviour
{
    [Header("Unit Identity")]
    [SerializeField] private string unitName = "Unit";
    [SerializeField] private UnitType unitType = UnitType.None;
    [SerializeField] private bool isCommander = false;
    [SerializeField] private bool isEnemy = false;

    [Header("Combat Stats")]
    [SerializeField] private ArmorTier armorTier = ArmorTier.Leather;
    [SerializeField] private int currentHP;
    [SerializeField] private int maxHP;

    [Header("Activation")]
    [SerializeField] private bool hasActivatedThisTurn = false;

    public event Action<Unit> OnUnitDied;

    public HexCoord GridPosition { get; set; }
    public bool IsEnemy => isEnemy;
    public bool IsCommander => isCommander;
    public string UnitName => unitName;
    public UnitType UnitType => unitType;
    public int CurrentHP => currentHP;
    public int MaxHP => maxHP;
    public bool HasActivatedThisTurn => hasActivatedThisTurn;

    private void Awake()
    {
        InitializeHP();
    }

    private void InitializeHP()
    {
        switch (armorTier)
        {
            case ArmorTier.Leather:
                maxHP = 1;
                break;
            case ArmorTier.Bronze:
                maxHP = 2;
                break;
            case ArmorTier.Iron:
                maxHP = 3;
                break;
        }
        currentHP = maxHP;
    }

    public bool CanActivate()
    {
        return !hasActivatedThisTurn && currentHP > 0;
    }

    public void Activate()
    {
        if (!CanActivate()) return;
        hasActivatedThisTurn = true;
    }

    public void ResetActivation()
    {
        hasActivatedThisTurn = false;
    }

    public void TakeDamage(int damage)
    {
        currentHP -= damage;
        Debug.Log($"{unitName} takes {damage} damage. HP: {currentHP}/{maxHP}");

        if (currentHP <= 0)
        {
            currentHP = 0;
            OnUnitDied?.Invoke(this);
            Destroy(gameObject);
        }
    }

    public void Heal(int amount)
    {
        currentHP = Mathf.Min(currentHP + amount, maxHP);
    }

    public int GetAttackRange()
    {
        switch (unitType)
        {
            case UnitType.Spearman:
                return 2;
            case UnitType.Archer:
            case UnitType.Slinger:
            case UnitType.EnemyArcher:
                return 3;
            case UnitType.Scout:
            case UnitType.EnemyScout:
                return 2;
            default:
                return 1;
        }
    }

    public void SetName(string name)
    {
        unitName = name;
    }

    public void SetUnitType(UnitType type)
    {
        unitType = type;
    }

    public void SetEnemy(bool enemy)
    {
        isEnemy = enemy;
    }

    public void SetCommander(bool commander)
    {
        isCommander = commander;
    }

    public void SetArmorTier(ArmorTier tier)
    {
        armorTier = tier;
        InitializeHP();
    }
}
