<script lang="ts">
  import { base } from "$app/paths";
  import PamResults from "$lib/components/PamResults.svelte";
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import { LOG_STEPS } from "$lib/simulations/pamSim";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import {
    Accordion,
    Bold,
    CompareCheckbox,
    Figure,
    H1,
    InfoBox,
    Li,
    Link,
    SectionMain as Main,
    Ol,
    PageNav,
    Text,
    Ul,
    type PhaseRegion,
  } from "@computational-biology-aachen/design";
  import { buildMemoryProtocol } from "@computational-biology-aachen/mxlweb-core/pam";
  import { marked } from "marked";

  // Slider state
  let lightIntensity = $state(100);
  let pulseInterval = $state(85);
  let darkLength = $state(30);
  let saturatingPulse = $state(5000);
  let trainingLength = $state(300);
  let relaxationLength = $state(300);
  let memoryLength = $state(300);
  let compareWithLast = $state(true);

  // Logspace sliders
  let activationIdx = $state(10); // LOG_STEPS[10] = 100
  let deactivationIdx = $state(10);
  const activationMultiplier = $derived(LOG_STEPS[activationIdx]);
  const deactivationMultiplier = $derived(LOG_STEPS[deactivationIdx]);

  const kDeepoxV = $derived(0.0024 * (activationMultiplier / 100));
  const kEpoxZ = $derived(0.00024 * (deactivationMultiplier / 100));
  const protocol = $derived(
    buildMemoryProtocol({
      lightIntensity,
      saturatingPulse,
      darkLength,
      pulseInterval,
      trainingLength,
      relaxationLength,
      memoryLength,
    }),
  );
  const simParams = $derived({
    AL: lightIntensity,
    SP: saturatingPulse,
    CtZ: kDeepoxV,
    CtV: kEpoxZ,
  });

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
</script>

<svelte:head>
  <title>Plant Light Memory</title>
</svelte:head>

<Main
  width="90ch"
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

  <InfoBox
    header="What you need to know"
    variant="warning"
  >
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

  <Figure
    src="{base}/pictures/NPQphotosynthesis.png"
    alt="Memory protocol diagram"
  >
    {#snippet caption()}Memory protocol overview{/snippet}
  </Figure>

  <!-- Guiding questions ------------------------------- -->
  <Accordion open={false}>
    {#snippet header()}
      {@html marked.parseInline(m.mem_guiding_expander())}
    {/snippet}
    <Text>
      <Bold>{@html marked.parseInline(m.mem_guiding_header())}</Bold>
    </Text>

    {#if audienceStore.audience === "4math"}
      <Text>{@html marked.parseInline(m.math_mem_guiding_intro())}</Text>
    {/if}

    <!-- Q1 -->
    <Text>
      <Bold>1.</Bold>
      {#if audienceStore.audience === "4bio"}
        {@html marked.parseInline(m.bio_mem_guiding_q1_prompt())}
      {:else}
        {@html marked.parseInline(m.math_mem_guiding_q1_prompt())}
      {/if}
    </Text>
    <Ul>
      <Li>{@html marked.parseInline(m.mem_guiding_q1_1())}</Li>
      <Li>{@html marked.parseInline(m.mem_guiding_q1_2())}</Li>
      <Li>{@html marked.parseInline(m.mem_guiding_q1_3())}</Li>
    </Ul>

    <!-- Q2 -->
    <Text
      ><Bold>2.</Bold>
      {@html marked.parseInline(m.mem_guiding_q2_prompt())}</Text
    >
    <Ul>
      <Li>{@html marked.parseInline(m.mem_guiding_q2_1())}</Li>
      <Li>{@html marked.parseInline(m.mem_guiding_q2_2())}</Li>
    </Ul>

    <!-- Q3: bio only -->
    {#if audienceStore.audience === "4bio"}
      <Text
        ><Bold>3.</Bold>
        {@html marked.parseInline(m.bio_mem_guiding_q3_prompt())}</Text
      >
      <Ul>
        <Li>{@html marked.parseInline(m.bio_mem_guiding_q3_1())}</Li>
        <Li>{@html marked.parseInline(m.bio_mem_guiding_q3_2())}</Li>
        <Li>{@html marked.parseInline(m.bio_mem_guiding_q3_3())}</Li>
        <Li>{@html marked.parseInline(m.bio_mem_guiding_q3_4())}</Li>
      </Ul>
    {/if}

    <!-- Last Q: bio Q4 / math Q3 -->
    {#if audienceStore.audience === "4bio"}
      <Text
        ><Bold>4.</Bold>
        {@html marked.parseInline(m.mem_guiding_last_prompt())}</Text
      >
    {:else}
      <Text
        ><Bold>3.</Bold>
        {@html marked.parseInline(m.mem_guiding_last_prompt())}</Text
      >
    {/if}
  </Accordion>

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
        />
      </label>
    {/if}
  </div>

  <CompareCheckbox bind:checked={compareWithLast} />

  <!-- Results ---------------------------------------- -->
  <PamResults
    protocol={protocol}
    params={simParams}
    kDeepoxV={kDeepoxV}
    kEpoxZ={kEpoxZ}
    phases={phases}
    compare={compareWithLast}
  />

  <Accordion title={m.literature()}>
    <Text>{@html marked.parseInline(m.literature_onpage())}</Text>
    <Ol>
      <Li>
        Matuszyńska, A., Heidari, S., Jahns, P., &amp; Ebenhöh, O. (2016). A
        mathematical model of non-photochemical quenching to study short-term
        light memory in plants.
        <em>Biochimica et Biophysica Acta (BBA) - Bioenergetics</em>, 1857(12),
        1860-1869.
        <Link href="https://doi.org/10.1016/j.bbabio.2016.09.003"
          >https://doi.org/10.1016/j.bbabio.2016.09.003</Link
        >
      </Li>
    </Ol>
  </Accordion>

  <PageNav
    base={base}
    prev={{ href: "/experiments", label: "Experiments in Silico" }}
    next={{ href: "/conclusion", label: "Conclusion" }}
  />
</Main>

<style>
  .slider-label {
    display: flex;
    flex-direction: column;
    justify-content: end;
    gap: var(--space-1, 4px);
    height: 100%;
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
</style>
