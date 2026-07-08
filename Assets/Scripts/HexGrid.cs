using System;
using System.Collections.Generic;
using UnityEngine;

[Serializable]
public struct HexCoord
{
    public int q; // column
    public int r; // row

    public HexCoord(int q, int r)
    {
        this.q = q;
        this.r = r;
    }

    // Axial coordinate distance (hex grid)
    public int DistanceTo(HexCoord other)
    {
        int dq = Math.Abs(q - other.q);
        int dr = Math.Abs(r - other.r);
        return Math.Max(Math.Max(dq, dr), Math.Abs(dq - dr));
    }

    public static HexCoord operator +(HexCoord a, HexCoord b)
    {
        return new HexCoord(a.q + b.q, a.r + b.r);
    }

    public static HexCoord operator -(HexCoord a, HexCoord b)
    {
        return new HexCoord(a.q - b.q, a.r - b.r);
    }

    public static bool operator ==(HexCoord a, HexCoord b)
    {
        return a.q == b.q && a.r == b.r;
    }

    public static bool operator !=(HexCoord a, HexCoord b)
    {
        return !(a == b);
    }

    public override bool Equals(object obj)
    {
        if (obj is HexCoord other)
            return this == other;
        return false;
    }

    public override int GetHashCode()
    {
        return HashCode.Combine(q, r);
    }

    public override string ToString()
    {
        return $"({q}, {r})";
    }

    // Returns the 6 neighbors of this hex in clockwise order
    public List<HexCoord> GetNeighbors()
    {
        return new List<HexCoord>
        {
            new HexCoord(q + 1, r),     // E
            new HexCoord(q + 1, r - 1), // NE
            new HexCoord(q, r - 1),     // NW
            new HexCoord(q - 1, r),     // W
            new HexCoord(q - 1, r + 1), // SW
            new HexCoord(q, r + 1)      // SE
        };
    }
}

public class HexGrid : MonoBehaviour
{
    [Header("Grid Settings")]
    [SerializeField] private int width = 8;
    [SerializeField] private int height = 8;
    [SerializeField] private float hexSize = 1.0f;

    private Dictionary<HexCoord, GameObject> hexTiles = new Dictionary<HexCoord, GameObject>();

    public int Width => width;
    public int Height => height;

    private void Awake()
    {
        InitializeGrid();
    }

    private void InitializeGrid()
    {
        for (int r = 0; r < height; r++)
        {
            for (int q = 0; q < width; q++)
            {
                HexCoord coord = new HexCoord(q, r);
                // Placeholder: hexTiles will be populated with visual hex objects
                // using a factory method once we have hex prefabs
            }
        }
    }

    public bool IsValidCoord(HexCoord coord)
    {
        return coord.q >= 0 && coord.q < width &&
               coord.r >= 0 && coord.r < height;
    }

    public Vector3 HexToWorldPosition(HexCoord coord)
    {
        // Flat-top hex layout
        float x = hexSize * (3.0f / 2.0f * coord.q);
        float z = hexSize * (Mathf.Sqrt(3.0f) / 2.0f * coord.q + Mathf.Sqrt(3.0f) * coord.r);
        return new Vector3(x, 0f, z);
    }

    public HexCoord WorldToHexPosition(Vector3 worldPos)
    {
        float q = (2.0f / 3.0f * worldPos.x) / hexSize;
        float r = (-1.0f / 3.0f * worldPos.x + Mathf.Sqrt(3.0f) / 3.0f * worldPos.z) / hexSize;

        // Round to nearest hex
        return HexRound(new HexCoord(Mathf.RoundToInt(q), Mathf.RoundToInt(r)));
    }

    private HexCoord HexRound(HexCoord raw)
    {
        int rq = raw.q;
        int rr = raw.r;
        int rs = -rq - rr;

        int rqRound = Mathf.RoundToInt(rq);
        int rrRound = Mathf.RoundToInt(rr);
        int rsRound = Mathf.RoundToInt(rs);

        float qDiff = Math.Abs(rqRound - rq);
        float rDiff = Math.Abs(rrRound - rr);
        float sDiff = Math.Abs(rsRound - rs);

        if (qDiff > rDiff && qDiff > sDiff)
            rqRound = -rrRound - rsRound;
        else if (rDiff > sDiff)
            rrRound = -rqRound - rsRound;

        return new HexCoord(rqRound, rrRound);
    }

    public List<HexCoord> GetHexesInRange(HexCoord center, int range)
    {
        List<HexCoord> results = new List<HexCoord>();
        for (int dq = -range; dq <= range; dq++)
        {
            for (int dr = Math.Max(-range, -dq - range); dr <= Math.Min(range, -dq + range); dr++)
            {
                HexCoord coord = new HexCoord(center.q + dq, center.r + dr);
                if (IsValidCoord(coord))
                {
                    results.Add(coord);
                }
            }
        }
        return results;
    }
}