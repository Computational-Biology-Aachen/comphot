/**
 * PAM fluorometry protocol builders.
 *
 * These translate UI slider parameters into a flat protocol array that the
 * Python worker can run piecewise via solve_ivp.
 *
 * Protocol step format: { t_end: number; PPFD: number }
 * Each step describes the light intensity (PFD) that is applied from the
 * previous step's t_end up to this step's t_end.
 */

export interface ProtocolStep {
  t_end: number;
  PPFD: number;
  [key: string]: number;
}

export interface PamParams {
  /** Actinic light intensity in μmol m⁻² s⁻¹ */
  lightIntensity: number;
  /** Saturating pulse intensity in μmol m⁻² s⁻¹ */
  saturatingPulse: number;
  /** Total experiment duration in minutes */
  totalMinutes: number;
  /** Dark phase length in seconds */
  darkLength: number;
  /** Seconds between saturating pulses during the light phase */
  pulseInterval: number;
}

const PULSE_LENGTH = 0.8; // seconds — duration of each saturating pulse

/**
 * Build a PAM fluorometry protocol that replicates the `sim_model()` logic
 * from `_model_functions.py`.
 *
 * Structure:
 *  1. Dark period from t=0 to t=2
 *  2. Saturating pulse at t=2 (dark conditions)
 *  3. Continue dark until t=darkLength
 *  4. Saturating pulse at t=darkLength (transition)
 *  5. Light phase with pulses every pulseInterval seconds until totalMinutes
 */
export function buildPamProtocol(params: PamParams): ProtocolStep[] {
  const {
    lightIntensity,
    saturatingPulse,
    totalMinutes,
    darkLength,
    pulseInterval,
  } = params;
  const maxTime = totalMinutes * 60;
  const dark = 0;

  const steps: ProtocolStep[] = [];

  // Track the current time cursor
  let t = 0;

  // Helper to push a segment
  function addStep(t_end: number, PPFD: number) {
    if (t_end > t) {
      steps.push({ t_end, PPFD });
      t = t_end;
    }
  }

  // 1. Initial dark period up to t=2
  if (t < 2) {
    addStep(2, dark);
  }

  // 2. Saturating pulse at t=2
  addStep(2 + PULSE_LENGTH, saturatingPulse);

  // 3. Continue dark until t=darkLength
  if (t < darkLength) {
    addStep(darkLength, dark);
  }

  // 4. Saturating pulse at t=darkLength
  addStep(darkLength + PULSE_LENGTH, saturatingPulse);

  // 5. Light phase with pulses every pulseInterval
  //    Start of light phase: darkLength (after the SP above)
  const numPulses = Math.floor((maxTime - darkLength) / pulseInterval);
  for (let j = 0; j <= numPulses; j++) {
    const pulseStart = darkLength + pulseInterval * j;
    if (pulseStart >= maxTime) break;

    if (j > 0) {
      // Light segment up to next pulse
      addStep(pulseStart, lightIntensity);
    }

    // Saturating pulse
    const pulseEnd = Math.min(pulseStart + PULSE_LENGTH, maxTime);
    addStep(pulseEnd, saturatingPulse);
  }

  // 6. Final light segment to maxTime
  if (t < maxTime) {
    addStep(maxTime, lightIntensity);
  }

  return steps;
}

// ---------------------------------------------------------------------------

export interface MemoryPamParams {
  /** Actinic light intensity in μmol m⁻² s⁻¹ */
  lightIntensity: number;
  /** Saturating pulse intensity in μmol m⁻² s⁻¹ */
  saturatingPulse: number;
  /** Dark phase length in seconds */
  darkLength: number;
  /** Seconds between saturating pulses */
  pulseInterval: number;
  /** Training phase length in seconds */
  trainingLength: number;
  /** Relaxation phase length in seconds */
  relaxationLength: number;
  /** Memory phase length in seconds */
  memoryLength: number;
}

/**
 * Build a plant memory PAM protocol that replicates `sim_model_memory()`.
 *
 * Structure:
 *  1. Dark period with pulses (darkLength seconds)
 *  2. Training phase — actinic light with pulses (trainingLength seconds)
 *  3. Relaxation phase — dark with pulses (relaxationLength seconds)
 *  4. Memory phase — actinic light with pulses (memoryLength seconds)
 */
export function buildMemoryProtocol(params: MemoryPamParams): ProtocolStep[] {
  const {
    lightIntensity,
    saturatingPulse,
    darkLength,
    pulseInterval,
    trainingLength,
    relaxationLength,
    memoryLength,
  } = params;

  const dark = 0;
  const steps: ProtocolStep[] = [];
  let t = 0;

  function addStep(t_end: number, PPFD: number) {
    if (t_end > t) {
      steps.push({ t_end, PPFD });
      t = t_end;
    }
  }

  function simulatePeriod(
    startTime: number,
    phaseLength: number,
    duringLight: number,
    startingLight: number,
    isDark: boolean,
  ) {
    let cursor = startTime;

    // Opening SP
    addStep(startTime, startingLight);
    addStep(startTime + PULSE_LENGTH, saturatingPulse);
    cursor = startTime + PULSE_LENGTH;

    if (!isDark) {
      const numPulses = Math.floor(phaseLength / pulseInterval);
      for (let i = 1; i < numPulses; i++) {
        const pulseStart = startTime + pulseInterval * i;
        addStep(pulseStart, duringLight);
        addStep(pulseStart + PULSE_LENGTH, saturatingPulse);
        cursor = pulseStart + PULSE_LENGTH;
      }
    }
    void cursor; // suppress unused warning
  }

  // 1. Dark period
  if (darkLength > 0) {
    simulatePeriod(2, darkLength, dark, dark, true);
  }

  // 2. Training phase
  if (trainingLength > 0) {
    simulatePeriod(darkLength, trainingLength, lightIntensity, dark, false);
  }

  const relaxStart = darkLength + trainingLength;
  const relaxEnd = relaxStart + relaxationLength;

  // 3. Relaxation phase (two sub-periods as in _model_functions.py)
  if (relaxationLength > 0) {
    const relaxPeriod1End = relaxEnd - pulseInterval;
    simulatePeriod(
      relaxStart,
      relaxPeriod1End - relaxStart,
      dark,
      lightIntensity,
      true,
    );
    simulatePeriod(relaxPeriod1End, pulseInterval, dark, dark, true);
  }

  // 4. Memory phase
  if (memoryLength > 0) {
    simulatePeriod(relaxEnd, memoryLength, lightIntensity, dark, false);
  }

  // Final segment to total end
  const totalEnd =
    darkLength + trainingLength + relaxationLength + memoryLength;
  if (t < totalEnd) {
    addStep(totalEnd, lightIntensity);
  }

  return steps;
}
