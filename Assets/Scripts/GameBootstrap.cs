using UnityEngine;

public class GameBootstrap
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        HexGrid grid = Ensure<HexGrid>("HexGrid");
        CardAbilityResolver resolver = Ensure<CardAbilityResolver>("CardAbilityResolver");
        CardDeckManager deckManager = Ensure<CardDeckManager>("CardDeckManager");
        TurnManager turnManager = Ensure<TurnManager>("TurnManager");
        AIDirector aiDirector = Ensure<AIDirector>("AIDirector");
        PlayerInputHandler inputHandler = Ensure<PlayerInputHandler>("PlayerInputHandler");
        CardTurnController cardTurnController = Ensure<CardTurnController>("CardTurnController");
        GameUIController uiController = Ensure<GameUIController>("GameUIController");
        GameSetup gameSetup = Ensure<GameSetup>("GameSetup");
        Ensure<RunManager>("RunManager");

        GameObject unitPrefab = CreateUnitPrefab();
        gameSetup.SetUnitPrefab(unitPrefab);
    }

    private static T Ensure<T>(string name) where T : MonoBehaviour
    {
        T existing = Object.FindObjectOfType<T>();
        if (existing != null) return existing;

        GameObject obj = new GameObject(name);
        return obj.AddComponent<T>();
    }

    private static GameObject CreateUnitPrefab()
    {
        GameObject prefab = new GameObject("UnitPrefab");
        prefab.AddComponent<Unit>();
        prefab.AddComponent<UnitVisual>();
        prefab.SetActive(false);
        return prefab;
    }
}
