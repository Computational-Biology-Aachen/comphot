<script lang="ts">
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import {
    computeNpq,
    computePhiPsii,
    findPeaks,
    interpolateAtIndices,
    normalizeToMax,
  } from "$lib/simulations/pamAnalysis";
  import type { ProtocolStep } from "$lib/simulations/pam";
  import { simulate, type SimParams } from "$lib/simulations/pamSim";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import {
    LineChart,
    ParameterTable,
    type PhaseRegion,
  } from "@computational-biology-aachen/design";
  import type { SimulationResult } from "@computational-biology-aachen/mxlweb-core";

  let {
    protocol,
    params,
    kDeepoxV,
    kEpoxZ,
    phases,
    compare,
    yMax = 1.2,
  }: {
    protocol: ProtocolStep[];
    params: SimParams;
    kDeepoxV: number;
    kEpoxZ: number;
    phases: PhaseRegion[];
    compare: boolean;
    yMax?: number;
  } = $props();

  let currentResult = $state<SimulationResult | null>(null);
  let previousResult = $state<SimulationResult | null>(null);
  let currentParams = $state<SimParams | null>(null);
  let previousParams = $state<SimParams | null>(null);
  let loading = $state(false);
  let errorMsg = $state("");

  let runToken = 0;

  // Run a fresh simulation whenever the protocol or rate constants change.
  $effect(() => {
    const p = protocol;
    const kDV = kDeepoxV;
    const kEZ = kEpoxZ;
    const nextParams = params;

    const token = ++runToken;
    loading = true;
    errorMsg = "";

    simulate(p, kDV, kEZ)
      .then((result) => {
        if (token !== runToken) return;
        previousResult = currentResult;
        previousParams = currentParams;
        currentResult = result;
        currentParams = nextParams;
        loading = false;
      })
      .catch((e: unknown) => {
        if (token !== runToken) return;
        errorMsg = `Simulation error: ${e instanceof Error ? e.message : e}`;
        loading = false;
      });
  });

  // Fluo is appended after the 6 state variables → column index 6
  const FLUO_COL = 6;

  function extractFluo(result: SimulationResult | null): number[] {
    return result?.values.map((v) => v[FLUO_COL]) ?? [];
  }

  const showOld = $derived(compare && previousResult !== null);

  const resultTime = $derived(currentResult?.time ?? []);

  const fluoCurrent = $derived(normalizeToMax(extractFluo(currentResult)));
  const fluoPrev = $derived(normalizeToMax(extractFluo(previousResult)));

  const peaksCurrent = $derived(findPeaks(fluoCurrent, 0.2));
  const peaksPrev = $derived(findPeaks(fluoPrev, 0.2));

  const npqCurrent = $derived.by(() =>
    interpolateAtIndices(
      peaksCurrent,
      computeNpq(fluoCurrent, peaksCurrent),
      fluoCurrent.length,
      "akima",
    ),
  );
  const npqPrev = $derived.by(() =>
    interpolateAtIndices(
      peaksPrev,
      computeNpq(fluoPrev, peaksPrev),
      fluoPrev.length,
      "akima",
    ),
  );

  const phiCurrent = $derived.by(() =>
    interpolateAtIndices(
      peaksCurrent,
      computePhiPsii(fluoCurrent, peaksCurrent),
      fluoCurrent.length,
      "akima",
    ),
  );
  const phiPrev = $derived.by(() =>
    interpolateAtIndices(
      peaksPrev,
      computePhiPsii(fluoPrev, peaksPrev),
      fluoPrev.length,
      "akima",
    ),
  );

  const fluoData = $derived({
    labels: resultTime,
    datasets: [
      { label: ta(m.bio_fluo(), m.math_fluo()), data: fluoCurrent },
      ...(showOld ? [{ label: m.old_label(), data: fluoPrev }] : []),
    ],
  });
  const npqData = $derived({
    labels: resultTime,
    datasets: [
      { label: m.axis_npq(), data: npqCurrent },
      ...(showOld ? [{ label: m.old_label(), data: npqPrev }] : []),
    ],
  });
  const phiData = $derived({
    labels: resultTime,
    datasets: [
      { label: m.axis_phipsii(), data: phiCurrent },
      ...(showOld ? [{ label: m.old_label(), data: phiPrev }] : []),
    ],
  });

  const paramRows = $derived.by(() => {
    const cp = currentParams;
    const pp = previousParams;
    if (!cp) return [];
    return [
      { label: "AL [μmol m⁻² s⁻¹]", newVal: cp.AL, oldVal: pp?.AL },
      { label: "SP [μmol m⁻² s⁻¹]", newVal: cp.SP, oldVal: pp?.SP },
      {
        label: "CtZ [s⁻¹]",
        newVal: cp.CtZ.toFixed(5),
        oldVal: pp?.CtZ?.toFixed(5),
      },
      {
        label: "CtV [s⁻¹]",
        newVal: cp.CtV.toFixed(6),
        oldVal: pp?.CtV?.toFixed(6),
      },
    ];
  });
</script>

{#if errorMsg}
  <p class="error-msg">{errorMsg}</p>
{/if}

{#if currentResult}
  <div
    class="charts-grid"
    class:three-cols={audienceStore.audience === "4bio"}
  >
    <div class="chart-card">
      <p class="chart-label">{ta(m.bio_fluo(), m.math_fluo())}</p>
      <LineChart
        data={fluoData}
        phases={phases}
        loading={loading}
        yMax={yMax}
      />
    </div>

    {#if audienceStore.audience === "4bio"}
      <div class="chart-card">
        <p class="chart-label">{m.axis_npq()}</p>
        <LineChart
          data={npqData}
          phases={phases}
          loading={loading}
        />
      </div>

      <div class="chart-card">
        <p class="chart-label">{m.axis_phipsii()}</p>
        <LineChart
          data={phiData}
          phases={phases}
          loading={loading}
        />
      </div>
    {/if}
  </div>

  {#if paramRows.length > 0}
    <div class="param-table-wrap">
      <ParameterTable
        rows={paramRows}
        showOld={showOld && previousParams !== null}
        newLabel={m.new_label()}
        oldLabel={m.old_label()}
      />
    </div>
  {/if}
{/if}

<style>
  .error-msg {
    margin: var(--space-2, 8px) 0;
    color: var(--color-error, red);
  }
  .charts-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--space-4, 16px);
    margin: var(--space-4, 16px) 0;
    width: 100%;
  }
  .charts-grid.three-cols {
    grid-template-columns: repeat(3, 1fr);
  }
  .chart-card {
    display: flex;
    flex-direction: column;
    gap: var(--space-2, 8px);
  }
  .chart-label {
    margin: 0;
    font-weight: 500;
    font-size: 0.875rem;
  }
  .param-table-wrap {
    margin: var(--space-4, 16px) 0;
  }
</style>
