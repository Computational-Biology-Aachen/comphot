export function normalizeToMax(data: number[]): number[] {
  const max = Math.max(...data.filter(Number.isFinite));
  if (max === 0 || !Number.isFinite(max)) return data;
  return data.map((v) => v / max);
}

export function findPeaks(data: number[], minProminence: number): number[] {
  const n = data.length;
  const candidates: number[] = [];
  for (let i = 1; i < n - 1; i++) {
    if (data[i] > data[i - 1] && data[i] > data[i + 1]) candidates.push(i);
  }
  return candidates.filter((peakIdx) => {
    const peakVal = data[peakIdx];
    let leftMin = peakVal;
    for (let j = peakIdx - 1; j >= 0; j--) {
      if (data[j] > peakVal) break;
      leftMin = Math.min(leftMin, data[j]);
    }
    let rightMin = peakVal;
    for (let j = peakIdx + 1; j < n; j++) {
      if (data[j] > peakVal) break;
      rightMin = Math.min(rightMin, data[j]);
    }
    return peakVal - Math.max(leftMin, rightMin) >= minProminence;
  });
}

export function interpolateAtIndices(
  indices: number[],
  values: number[],
  length: number,
  method: "linear" | "akima" = "linear",
): number[] {
  const out = new Array(length).fill(NaN);
  if (indices.length === 0) return out;

  if (method === "akima") {
    const n = indices.length;
    if (n === 1) {
      for (let k = 0; k < length; k++) out[k] = values[0];
      return out;
    }
    const m: number[] = [];
    for (let i = 0; i < n - 1; i++) {
      m.push((values[i + 1] - values[i]) / (indices[i + 1] - indices[i]));
    }
    const mExt = [
      2 * m[0] - m[1],
      2 * m[0] - m[1],
      ...m,
      2 * m[n - 2] - m[n - 3 < 0 ? 0 : n - 3],
      2 * m[n - 2] - m[n - 3 < 0 ? 0 : n - 3],
    ];
    const t: number[] = [];
    for (let i = 0; i < n; i++) {
      const w1 = Math.abs(mExt[i + 3] - mExt[i + 2]);
      const w2 = Math.abs(mExt[i + 1] - mExt[i]);
      const denom = w1 + w2;
      t.push(
        denom < 1e-14
          ? (mExt[i + 1] + mExt[i + 2]) / 2
          : (w1 * mExt[i + 1] + w2 * mExt[i + 2]) / denom,
      );
    }
    for (let p = 0; p < n - 1; p++) {
      const x0 = indices[p],
        x1 = indices[p + 1];
      const y0 = values[p],
        y1 = values[p + 1];
      const t0 = t[p],
        t1 = t[p + 1];
      const h = x1 - x0;
      const end = p === n - 2 ? x1 : x1 - 1;
      for (let k = x0; k <= end; k++) {
        const u = (k - x0) / h,
          u2 = u * u,
          u3 = u2 * u;
        out[k] =
          (2 * u3 - 3 * u2 + 1) * y0 +
          (u3 - 2 * u2 + u) * h * t0 +
          (-2 * u3 + 3 * u2) * y1 +
          (u3 - u2) * h * t1;
      }
    }
    return out;
  }

  // linear
  indices.forEach((i, j) => {
    out[i] = values[j];
  });
  for (let p = 0; p < indices.length - 1; p++) {
    const i0 = indices[p],
      i1 = indices[p + 1],
      v0 = values[p],
      v1 = values[p + 1];
    for (let k = i0 + 1; k < i1; k++) {
      out[k] = v0 + ((v1 - v0) * (k - i0)) / (i1 - i0);
    }
  }
  return out;
}

export function computeNpq(
  fluoNorm: number[],
  peakIndices: number[],
): number[] {
  if (peakIndices.length === 0) return [];
  const Fm0 = fluoNorm[peakIndices[0]];
  return peakIndices.map((i) => (Fm0 - fluoNorm[i]) / fluoNorm[i]);
}

export function computePhiPsii(
  fluoNorm: number[],
  peakIndices: number[],
): number[] {
  return peakIndices.map((peakIdx, i) => {
    const Fm = fluoNorm[peakIdx];
    const leftBoundary = i > 0 ? peakIndices[i - 1] : 0;
    let Fo = Fm;
    for (let j = peakIdx - 1; j >= leftBoundary; j--) {
      if (fluoNorm[j] < Fo) Fo = fluoNorm[j];
    }
    return (Fm - Fo) / Fm;
  });
}
