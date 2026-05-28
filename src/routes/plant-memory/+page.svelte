<script lang="ts">
  import { base } from "$app/paths";

  import { ta } from "$lib/i18n";
  import LiteratureExpander from "$lib/LiteratureExpander.svelte";
  import * as m from "$lib/paraglide/messages";
  import { buildMemoryProtocol } from "$lib/simulations/pam";
  import {
    computeNpq,
    computePhiPsii,
    findPeaks,
    interpolateAtIndices,
    normalizeToMax,
  } from "$lib/simulations/pamAnalysis";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import { LOG_STEPS, SimState } from "$lib/stores/simStore.svelte";
  import {
    Bold,
    CompareCheckbox,
    Accordion as Expander,
    H1,
    InfoBox,
    Li,
    LineChart,
    SectionMain as Main,
    PageNav,
    ParameterTable,
    Text,
    Ul,
    type PhaseRegion,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
  import { onMount } from "svelte";

  const sim = new SimState();
  sim.setup();

  // Slider state
  let lightIntensity = $state(100);
  let pulseInterval = $state(85);
  let darkLength = $state(30);
  let saturatingPulse = $state(5000);
  let trainingLength = $state(300);
  let relaxationLength = $state(300);
  let memoryLength = $state(300);
  let compareWithLast = $state(true);
  let showAnswers = $state(false);

  // Logspace sliders
  let activationIdx = $state(10); // LOG_STEPS[10] = 100
  let deactivationIdx = $state(10);
  const activationMultiplier = $derived(LOG_STEPS[activationIdx]);
  const deactivationMultiplier = $derived(LOG_STEPS[deactivationIdx]);

  function runSimulation() {
    const protocol = buildMemoryProtocol({
      lightIntensity,
      saturatingPulse,
      darkLength,
      pulseInterval,
      trainingLength,
      relaxationLength,
      memoryLength,
    });
    const kDeepoxV = 0.0024 * (activationMultiplier / 100);
    const kEpoxZ = 0.00024 * (deactivationMultiplier / 100);
    sim.run(
      protocol,
      { AL: lightIntensity, SP: saturatingPulse, CtZ: kDeepoxV, CtV: kEpoxZ },
      kDeepoxV,
      kEpoxZ,
    );
  }

  onMount(runSimulation);

  // Phase regions for 4-phase memory protocol
  const phases = $derived.by<PhaseRegion[]>(() => {
    const trainStart = darkLength;
    const relaxStart = trainStart + trainingLength;
    const memStart = relaxStart + relaxationLength;
    const end = memStart + memoryLength;
    const regions: PhaseRegion[] = [];

    if (darkLength > 0) {
      regions.push({
        start: 0,
        end: trainStart,
        color: "rgba(28, 91, 199, 0.25)",
        label: "",
      });
    }
    if (trainingLength > 0) {
      regions.push({
        start: trainStart,
        end: relaxStart,
        color: "rgba(207, 109, 12, 0.25)",
        label: m.mem_anno_training(),
      });
    }
    if (relaxationLength > 0) {
      regions.push({
        start: relaxStart,
        end: memStart,
        color: "rgba(28, 91, 199, 0.25)",
        label: m.mem_anno_relaxation(),
      });
    }
    if (memoryLength > 0) {
      regions.push({
        start: memStart,
        end,
        color: "rgba(209, 10, 13, 0.25)",
        label: m.mem_anno_memory(),
      });
    }
    return regions;
  });

  const showOld = $derived(compareWithLast && sim.previousResult !== null);

  const paramRows = $derived.by(() => {
    const cp = sim.currentParams;
    const pp = sim.previousParams;
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

  // ── Chart data ────────────────────────────────────────────────────────────
  const FLUO_COL = 8;

  function extractFluo(result: typeof sim.currentResult): number[] {
    return result?.values.map((v) => v[FLUO_COL]) ?? [];
  }

  const resultTime = $derived(sim.currentResult?.time ?? []);

  const fluoCurrent = $derived(normalizeToMax(extractFluo(sim.currentResult)));
  const fluoPrev = $derived(normalizeToMax(extractFluo(sim.previousResult)));

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
</script>

<svelte:head>
  <title>Plant Light Memory</title>
</svelte:head>

<Main
  width="narrow"
  align="start"
>
  <H1>
    {@html marked.parseInline(m.mem_headline_brain())}
  </H1>

  <InfoBox header="Learning objectives">
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_mem_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.math_mem_lo_2())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_mem_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.bio_mem_lo_2())}</Li>
        <Li>{@html marked.parseInline(m.bio_mem_lo_3())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <InfoBox header="What you need to know">
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_mem_prereq_1())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_mem_prereq_1())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <PageNav
    base={base}
    prev={{ href: "/experiments", label: "Experiments in Silico" }}
    next={{ href: "/conclusion", label: "Conclusion" }}
  />

  <!-- Explanation ------------------------------------ -->
  <Text>
    {@html marked.parseInline(
      ta(m.bio_mem_introduction_brain(), m.math_mem_introduction_brain()),
    )}
  </Text>

  <figure class="fig">
    <img
      src="{base}/pictures/NPQphotosynthesis.png"
      alt="Memory protocol diagram"
      class="protocol-img"
    />
    <figcaption>Memory protocol overview</figcaption>
  </figure>

  <!-- Guiding questions ------------------------------- -->
  <Expander open={false}>
    {#snippet header()}
      {@html marked.parseInline(m.mem_guiding_expander())}
    {/snippet}
    <Text>
      <Bold>{@html marked.parseInline(m.mem_guiding_header())}</Bold>
    </Text>
    <label class="toggle-label">
      <input
        type="checkbox"
        bind:checked={showAnswers}
      />
      {@html marked.parseInline(m.mem_guiding_toggle())}
    </label>
    {#if !showAnswers}
      <!-- FIXME: break message into smaller pieces -->
      {@html marked.parse(
        ta(m.bio_mem_guiding_questions(), m.math_mem_guiding_questions()),
      )}
    {:else}
      <!-- FIXME: break message into smaller pieces -->
      {@html marked.parse(
        ta(m.bio_mem_guiding_answers(), m.math_mem_guiding_answers()),
      )}
    {/if}
  </Expander>

  <!-- Sliders ---------------------------------------- -->

  <!-- Common sliders -->
  <div class="slider-row">
    <label class="slider-label">
      {@html m.slider_light()}: <strong>{lightIntensity}</strong>
      <input
        type="range"
        min="50"
        max="900"
        step="50"
        bind:value={lightIntensity}
        onchange={runSimulation}
      />
    </label>
    <label class="slider-label">
      {@html m.slider_pulses()}: <strong>{pulseInterval} s</strong>
      <input
        type="range"
        min="5"
        max="150"
        step="5"
        bind:value={pulseInterval}
        onchange={runSimulation}
      />
    </label>
    <label class="slider-label">
      {@html m.fal_slider_darklength()}: <strong>{darkLength} s</strong>
      <input
        type="range"
        min="0"
        max="300"
        step="10"
        bind:value={darkLength}
        onchange={runSimulation}
      />
    </label>
    <label class="slider-label">
      {@html m.fal_slider_saturate()}: <strong>{saturatingPulse}</strong>
      <input
        type="range"
        min="0"
        max="10000"
        step="500"
        bind:value={saturatingPulse}
        onchange={runSimulation}
      />
    </label>
    <label class="slider-label">
      {@html m.mem_slider_training()}: <strong>{trainingLength} s</strong>
      <input
        type="range"
        min="0"
        max="600"
        step="30"
        bind:value={trainingLength}
        onchange={runSimulation}
      />
    </label>
    <label class="slider-label">
      {@html m.mem_slider_relaxation()}:
      <strong>{relaxationLength} s</strong>
      <input
        type="range"
        min="0"
        max="600"
        step="30"
        bind:value={relaxationLength}
        onchange={runSimulation}
      />
    </label>
    <label class="slider-label">
      {@html m.mem_slider_memory()}: <strong>{memoryLength} s</strong>
      <input
        type="range"
        min="0"
        max="600"
        step="30"
        bind:value={memoryLength}
        onchange={runSimulation}
      />
    </label>
    <!-- 4bio: activation/deactivation sliders -->
    {#if audienceStore.audience === "4bio"}
      <label class="slider-label">
        {m.slider_activation()}: <strong>{activationMultiplier}</strong>
        <input
          type="range"
          min="0"
          max="20"
          step="1"
          bind:value={activationIdx}
          onchange={runSimulation}
        />
      </label>
      <label class="slider-label">
        {m.slider_deactivation()}: <strong>{deactivationMultiplier}</strong>
        <input
          type="range"
          min="0"
          max="20"
          step="1"
          bind:value={deactivationIdx}
          onchange={runSimulation}
        />
      </label>
    {/if}
  </div>

  <CompareCheckbox bind:checked={compareWithLast} />

  {#if sim.errorMsg}
    <p class="error-msg">{sim.errorMsg}</p>
  {/if}

  <!-- Results ---------------------------------------- -->
  {#if sim.currentResult}
    <div
      class="charts-grid"
      class:three-cols={audienceStore.audience === "4bio"}
    >
      <div class="chart-card">
        <p class="chart-label">{ta(m.bio_fluo(), m.math_fluo())}</p>
        <LineChart
          data={fluoData}
          phases={phases}
          loading={sim.loading}
        />
      </div>

      {#if audienceStore.audience === "4bio"}
        <div class="chart-card">
          <p class="chart-label">{m.axis_npq()}</p>
          <LineChart
            data={npqData}
            phases={phases}
            loading={sim.loading}
          />
        </div>

        <div class="chart-card">
          <p class="chart-label">{m.axis_phipsii()}</p>
          <LineChart
            data={phiData}
            phases={phases}
            loading={sim.loading}
          />
        </div>
      {/if}
    </div>

    {#if paramRows.length > 0}
      <div class="param-table-wrap">
        <ParameterTable
          rows={paramRows}
          showOld={showOld && sim.previousParams !== null}
          newLabel={m.new_label()}
          oldLabel={m.old_label()}
        />
      </div>
    {/if}
  {/if}

  <LiteratureExpander />

  <PageNav
    base={base}
    prev={{ href: "/experiments", label: "Experiments in Silico" }}
    next={{ href: "/conclusion", label: "Conclusion" }}
  />
</Main>

<style>
  .fig {
    width: 100%;
    text-align: center;
  }
  .fig img {
    max-width: 100%;
  }
  .fig figcaption {
    margin-top: var(--space-2, 8px);
    color: var(--color-text-muted, #666);
    font-size: 0.875rem;
  }
  .protocol-img {
    max-width: 100%;
  }

  .slider-label {
    display: flex;
    flex-direction: column;
    gap: var(--space-1, 4px);
    font-size: 0.9rem;
  }
  .slider-row {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    align-items: inherit;
    gap: var(--space-4, 16px);
    border-radius: var(--radius-lg);
    background-color: var(--color-surface);
    padding: 1.5rem;
    width: 100%;

    @media (min-width: 768px) {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr;
      align-items: center;
    }
  }

  .toggle-label {
    display: flex;
    align-items: center;
    gap: var(--space-2, 8px);
    cursor: pointer;
    margin: var(--space-2, 8px) 0;
  }

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
