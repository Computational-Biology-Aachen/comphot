<script lang="ts">
  import { base } from "$app/paths";

  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import SimResultsGrid from "$lib/SimResultsGrid.svelte";
  import { buildMemoryProtocol } from "$lib/simulations/pam";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import { LOG_STEPS, SimState } from "$lib/stores/simState.svelte";
  import {
    Bold,
    Button,
    CompareCheckbox,
    Accordion as Expander,
    H1,
    InfoBox,
    LiteratureExpander,
    Main,
    Narrow,
    PageNav,
    Text,
    type PhaseRegion,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
  import ActivationSliders from "../../../../../packages/design/src/lib/SliderActivation.svelte";

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
  const totalTime = $derived(
    darkLength + trainingLength + relaxationLength + memoryLength,
  );

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
      [kDeepoxV, kEpoxZ],
    );
  }

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
</script>

<svelte:head>
  <title>Plant Light Memory</title>
</svelte:head>

<Main>
  <Narrow>
    <H1>
      {@html marked.parseInline(m.mem_headline_brain())}
    </H1>

    <InfoBox>
      <!-- FIXME: break message into smaller pieces -->
      {@html marked.parse(
        ta(m.bio_mem_learning_objectives(), m.math_mem_learning_objectives()),
      )}
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
    <Expander
      title={m.mem_guiding_expander()}
      open={false}
    >
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
    <div class="slider-section">
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
          />
        </label>
      </div>

      <div class="slider-row">
        <label class="slider-label">
          {@html m.fal_slider_darklength()}: <strong>{darkLength} s</strong>
          <input
            type="range"
            min="0"
            max="300"
            step="10"
            bind:value={darkLength}
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
          />
        </label>
      </div>

      <div class="slider-row three">
        <label class="slider-label">
          {@html m.mem_slider_training()}: <strong>{trainingLength} s</strong>
          <input
            type="range"
            min="0"
            max="600"
            step="30"
            bind:value={trainingLength}
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
          />
        </label>
      </div>

      <!-- 4bio: activation/deactivation sliders -->
      {#if audienceStore.audience === "4bio"}
        <div class="slider-row">
          <ActivationSliders
            bind:activationIdx={activationIdx}
            bind:deactivationIdx={deactivationIdx}
            activationLabel={m.slider_activation()}
            deactivationLabel={m.slider_deactivation()}
            activationMultiplier={activationMultiplier}
            deactivationMultiplier={deactivationMultiplier}
          />
        </div>
      {/if}
    </div>

    <!-- Run controls-->
    <div class="run-controls">
      <div class="run-btn-wrap">
        <Button
          loading={sim.loading}
          fullWidth
          onclick={runSimulation}
          >{sim.loading ? "Running…" : "Run simulation"}</Button
        >
      </div>
      <CompareCheckbox bind:checked={compareWithLast} />
    </div>

    {#if sim.errorMsg}
      <p class="error-msg">{sim.errorMsg}</p>
    {/if}

    <!-- Results ---------------------------------------- -->
    {#if sim.currentResult}
      <SimResultsGrid
        currentResult={sim.currentResult}
        previousResult={sim.previousResult}
        showOld={showOld}
        phases={phases}
        totalTime={totalTime}
        paramRows={paramRows}
        showOldParams={showOld && sim.previousParams !== null}
      />
    {/if}

    <LiteratureExpander />

    <PageNav
      base={base}
      prev={{ href: "/experiments", label: "Experiments in Silico" }}
      next={{ href: "/conclusion", label: "Conclusion" }}
    />
  </Narrow>
</Main>
