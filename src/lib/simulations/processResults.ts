/**
 * Post-processing for PAM simulation results.
 * Converts raw worker output into Fluorescence, NPQ, and PhiPSII traces.
 */

export interface ProcessedResults {
	time: number[];
	fluo: number[];
	npqTime: number[];
	npq: number[];
	phiTime: number[];
	phiPSII: number[];
}

/**
 * Find indices of local maxima in arr.
 * A local maximum satisfies arr[i] > arr[i-1] && arr[i] > arr[i+1].
 */
export function findPeaks(arr: number[]): number[] {
	return arr.reduce<number[]>((acc, v, i) => {
		if (i > 0 && i < arr.length - 1 && v > arr[i - 1] && v > arr[i + 1]) {
			acc.push(i);
		}
		return acc;
	}, []);
}

/**
 * Process raw simulation output into normalised Fluo, NPQ, and PhiPSII.
 *
 * Worker output columns: P, H, E, A, Pr, V, Fluo  (index 6 = Fluo)
 *
 * @param time - time array in seconds
 * @param values - 2D array [n_points × 7] from worker
 */
export function processResults(time: number[], values: number[][]): ProcessedResults {
	if (!time.length || !values.length) {
		return { time: [], fluo: [], npqTime: [], npq: [], phiTime: [], phiPSII: [] };
	}

	// Extract and normalise fluorescence
	const fluoRaw = values.map((row) => row[6]);
	const fluoMax = Math.max(...fluoRaw);
	const fluo = fluoMax > 0 ? fluoRaw.map((v) => v / fluoMax) : fluoRaw;

	// Find peaks (local maxima)
	const peaks = findPeaks(fluo);

	if (peaks.length === 0) {
		return { time, fluo, npqTime: [], npq: [], phiTime: [], phiPSII: [] };
	}

	const Fm = fluo[peaks[0]];

	// NPQ = (Fm - Fm') / Fm'   where Fm' = fluo[peak]
	const npqTime = peaks.map((i) => time[i]);
	const npq = peaks.map((i) => {
		const fm_prime = fluo[i];
		return fm_prime > 0 ? (Fm - fm_prime) / fm_prime : 0;
	});

	// PhiPSII = (Fm_i - Fo_i) / Fm_i
	// Fo_i = minimum of fluo in the interval before each peak
	const phiPSII = peaks.map((peakIdx, j) => {
		const searchStart = j === 0 ? 0 : peaks[j - 1];
		const window = fluo.slice(searchStart, peakIdx);
		const Fo = window.length ? Math.min(...window) : 0;
		const fm_i = fluo[peakIdx];
		return fm_i > 0 ? (fm_i - Fo) / fm_i : 0;
	});

	return { time, fluo, npqTime, npq, phiTime: npqTime, phiPSII };
}
