using System.Collections.Generic;
using System.IO;
using UnityEngine;

/// <summary>
/// Auto-loads textures from Assets/Textures/ and applies them to hex tiles and units.
/// Drop generated PNG files into Assets/Textures/ and they'll be picked up automatically.
/// 
/// Naming convention:
///   hex_sand.png       — sand tile texture
///   hex_rock.png       — rock tile texture  
///   hex_grass.png      — grass tile texture
///   unit_david.png     — David unit token
///   unit_swordsman.png — Swordsman unit token
///   unit_spearman.png  — Spearman unit token
///   unit_slinger.png   — Slinger unit token
///   unit_archer.png    — Archer unit token
///   unit_scout.png     — Scout unit token
///   enemy_raider.png   — Amalekite Raider token
///   enemy_slinger.png  — Amalekite Slinger token
///   enemy_archer.png   — Amalekite Archer token
///   enemy_scout.png    — Amalekite Scout token
///   enemy_camel.png    — Camel Rider token
///   enemy_chieftain.png— Amalekite Chieftain token
///   ui_endturn.png     — End Turn button
///   ui_overwork.png    — Overwork button
/// </summary>
public class TextureLoader : MonoBehaviour
{
    [Header("Hex Grid Reference")]
    [SerializeField] private HexGrid grid;

    // Cache loaded textures
    private Dictionary<string, Texture2D> loadedTextures = new Dictionary<string, Texture2D>();

    private void Start()
    {
        if (grid == null) grid = FindObjectOfType<HexGrid>();
        LoadAllTextures();
    }

    /// <summary>
    /// Scans Assets/Textures/ and loads all PNG files
    /// </summary>
    public void LoadAllTextures()
    {
        string texturesPath = Path.Combine(Application.dataPath, "Textures");
        if (!Directory.Exists(texturesPath))
        {
            Directory.CreateDirectory(texturesPath);
            Debug.Log("Created Textures folder at: " + texturesPath);
            return;
        }

        string[] files = Directory.GetFiles(texturesPath, "*.png");
        foreach (string file in files)
        {
            string fileName = Path.GetFileNameWithoutExtension(file);
            byte[] bytes = File.ReadAllBytes(file);
            Texture2D tex = new Texture2D(2, 2);
            if (tex.LoadImage(bytes))
            {
                tex.name = fileName;
                loadedTextures[fileName] = tex;
                Debug.Log($"Loaded texture: {fileName}");
            }
        }

        Debug.Log($"Loaded {loadedTextures.Count} textures from {texturesPath}");
    }

    /// <summary>
    /// Get a loaded texture by name (without extension)
    /// </summary>
    public Texture2D GetTexture(string name)
    {
        if (loadedTextures.TryGetValue(name, out Texture2D tex))
            return tex;
        return null;
    }

    /// <summary>
    /// Apply a tile texture to all hex tiles of a given type
    /// </summary>
    public void ApplyTileTexture(string textureName, System.Func<int, int, bool> matchFunc)
    {
        Texture2D tex = GetTexture(textureName);
        if (tex == null) return;

        if (grid == null) return;

        foreach (var kvp in grid.Tiles)
        {
            HexCoord coord = kvp.Key;
            GameObject tileObj = kvp.Value;

            if (matchFunc(coord.q, coord.r))
            {
                Renderer renderer = tileObj.GetComponent<Renderer>();
                if (renderer != null)
                {
                    Material mat = renderer.material;
                    mat.mainTexture = tex;
                }
            }
        }
    }

    /// <summary>
    /// Apply a unit texture to all spawned unit tokens matching the name
    /// </summary>
    public void ApplyUnitTexture(string unitName, string textureName)
    {
        Texture2D tex = GetTexture(textureName);
        if (tex == null) return;

        Unit[] allUnits = FindObjectsOfType<Unit>();
        foreach (Unit unit in allUnits)
        {
            if (unit.UnitName.ToLower().Contains(unitName.ToLower()))
            {
                ApplyTextureToChildren(unit.gameObject, tex);
            }
        }
    }

    private void ApplyTextureToChildren(GameObject obj, Texture2D tex)
    {
        Renderer[] renderers = obj.GetComponentsInChildren<Renderer>();
        foreach (Renderer renderer in renderers)
        {
            Material mat = renderer.material;
            mat.mainTexture = tex;
        }
    }
}