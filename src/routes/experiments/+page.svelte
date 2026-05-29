<script lang="ts">
  import { base } from "$app/paths";

  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import PamResults from "$lib/components/PamResults.svelte";
  import { buildPamProtocol } from "$lib/simulations/pam";
  import { LOG_STEPS } from "$lib/simulations/pamSim";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import {
    Accordion,
    Bold,
    Code,
    CompareCheckbox,
    Figure,
    H1,
    H2,
    InfoBox,
    Li,
    Link,
    SectionMain as Main,
    Math,
    Ol,
    PageNav,
    type PhaseRegion,
    Pre,
    Text,
    Ul,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";

  // Slider state
  let lightIntensity = $state(100);
  let totalMinutes = $state(5);
  let pulseInterval = $state(85);
  let darkLength = $state(30);
  let saturatingPulse = $state(5000);
  let compareWithLast = $state(true);
  let showAnswers = $state(false);

  // Logspace sliders
  let activationIdx = $state(10); // LOG_STEPS[10] = 100
  let deactivationIdx = $state(10);
  const activationMultiplier = $derived(LOG_STEPS[activationIdx]);
  const deactivationMultiplier = $derived(LOG_STEPS[deactivationIdx]);
  const totalTime = $derived(totalMinutes * 60);

  const kDeepoxV = $derived(0.0024 * (activationMultiplier / 100));
  const kEpoxZ = $derived(0.00024 * (deactivationMultiplier / 100));
  const protocol = $derived(
    buildPamProtocol({
      lightIntensity,
      saturatingPulse,
      totalMinutes,
      darkLength,
      pulseInterval,
    }),
  );
  const simParams = $derived({
    AL: lightIntensity,
    SP: saturatingPulse,
    CtZ: kDeepoxV,
    CtV: kEpoxZ,
  });

  const phases = $derived.by<PhaseRegion[]>(() => [
    { start: 0, end: darkLength, color: "rgba(28, 91, 199, 0.18)" },
    { start: darkLength, end: totalTime, color: "rgba(207, 109, 12, 0.18)" },
  ]);

  // Model code constants (4math walkthrough)
  const CODE = {
    define: `import numpy as np\nfrom modelbase.ode import Model\n\nmodel = Model()`,
    params: `pars = {\n    "PSIItot": 2.5, "PQtot": 20, "APtot": 50, ...\n    "kDeepoxV": 0.0024,   # Activation of quenching\n    "kEpoxZ":   0.00024,  # Deactivation\n    # ... (see full parameter list on GitHub)\n}`,
    comps: `comps = ["P", "H", "E", "A", "Pr", "V"]`,
    addCompsPars: `model.add_parameters(pars)\nmodel.add_compounds(comps)`,
    definesim: `from modelbase.ode import Simulator\nsimulator = Simulator(model)`,
    initialisesim: `y0 = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}\nsimulator.initialise(y0)`,
  };
</script>

<svelte:head>
  <title>Experiments in Silico</title>
</svelte:head>

<Main
  width="90ch"
  align="start"
>
  <H1>{@html marked.parseInline(m.fal_headline_experiments())}</H1>

  <InfoBox header="Learning objectives">
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_fal_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.math_fal_lo_2())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_fal_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.bio_fal_lo_2())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <InfoBox
    header="What you need to know"
    variant="warning"
  >
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_fal_prereq_1())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_fal_prereq_1())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <PageNav
    base={base}
    prev={{ href: "/model", label: "Computational Models" }}
    next={{ href: "/plant-memory", label: "Plant Memory" }}
  />

  <!-- Model Construction ----------------------------- -->
  <H2>
    {@html marked.parseInline(m.fal_headline_model_construction())}
  </H2>

  <Text>
    {@html marked.parseInline(m.fal_construction_explanation_1())}
  </Text>

  <Figure
    src="{base}/pictures/NPQphotosynthesis.png"
    alt={m.fal_caption_model_npq()}
  >
    {#snippet caption()}{m.fal_caption_model_npq()}{/snippet}
  </Figure>

  <Text>{@html marked.parseInline(m.fal_construction_explanation_2())}</Text>
  <Text>{@html marked.parseInline(m.fal_rates_1())}</Text>
  <Text>{@html marked.parseInline(m.fal_rates_2())}</Text>
  <Text>{@html marked.parseInline(m.fal_rates_3())}</Text>
  <Text>{@html marked.parseInline(m.fal_rates_4())}</Text>
  <Text>{@html marked.parseInline(m.fal_rates_5())}</Text>
  <Text>{@html marked.parseInline(m.fal_rates_6())}</Text>

  <Accordion>
    {#snippet header()}
      {@html marked.parseInline(m.fal_components_explanation_header())}
    {/snippet}

    <h3 class="content-table-title">{m.fal_molecules_title()}</h3>
    <table class="content-table">
      <thead>
        <tr>
          <th>{m.fal_table_col_name()}</th>
          <th>{m.fal_table_col_description()}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{m.fal_molecules_pq_name()}</td>
          <td>{m.fal_molecules_pq_desc()}</td>
        </tr>
        <tr>
          <td>{m.fal_molecules_atp_name()}</td>
          <td>{m.fal_molecules_atp_desc()}</td>
        </tr>
        <tr>
          <td>{m.fal_molecules_xantophyll_name()}</td>
          <td>{m.fal_molecules_xantophyll_desc()}</td>
        </tr>
      </tbody>
    </table>

    <h3 class="content-table-title">{m.fal_enzymes_title()}</h3>
    <table class="content-table">
      <thead>
        <tr>
          <th>{m.fal_table_col_name()}</th>
          <th>{m.fal_table_col_description()}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{m.fal_enzymes_psii_name()}</td>
          <td>{m.fal_enzymes_psii_desc()}</td>
        </tr>
        <tr>
          <td>{m.fal_enzymes_psbs_name()}</td>
          <td>{m.fal_enzymes_psbs_desc()}</td>
        </tr>
        <tr>
          <td>{m.fal_enzymes_ptox_name()}</td>
          <td>{m.fal_enzymes_ptox_desc()}</td>
        </tr>
        <tr>
          <td>{m.fal_enzymes_cytb6f_name()}</td>
          <td>{m.fal_enzymes_cytb6f_desc()}</td>
        </tr>
        <tr>
          <td>{m.fal_enzymes_atpase_name()}</td>
          <td>{m.fal_enzymes_atpase_desc()}</td>
        </tr>
      </tbody>
    </table>
  </Accordion>

  <!-- 4math: ODE equations + code walkthrough -->
  {#if audienceStore.audience === "4math"}
    <H2>
      {@html marked.parseInline(m.math_fal_headline_model_equations())}
    </H2>
    <Text>
      {@html marked.parseInline(m.math_fal_model_equations_introduction())}
    </Text>

    <Math
      display
      tex={String.raw`\begin{aligned}
\frac{\mathrm{dPQH_2}}{\mathrm{d}t} &= v_\mathrm{PSII} - v_\mathrm{PQ_{ox}} \\
\frac{\mathrm{dATP}}{\mathrm{d}t} &= v_\mathrm{ATPsynthase} - v_\mathrm{ATPconsumption} \\
\frac{\mathrm{dATPase^{*}}}{\mathrm{d}t} &= F k_\mathrm{actATPase} \cdot \mathrm{H(PFD)} \cdot \mathrm{ATPase} - k_\mathrm{deactATPase} \cdot (1 - \mathrm{H(PFD)}) \cdot \mathrm{ATPase^{*}} \\
b_\mathrm{H} \cdot \frac{\mathrm{dH}}{\mathrm{d}t} &= 2 v_\mathrm{PSII} + 4 v_\mathrm{PQ_{ox}} - \tfrac{14}{3} v_\mathrm{ATPsynthase} - v_\mathrm{leak} \\
\frac{\mathrm{dPsbS}}{\mathrm{d}t} &= -v_\mathrm{Psbs^{p}} \\
\frac{\mathrm{dVx}}{\mathrm{d}t} &= -v_\mathrm{Xcyc}
\end{aligned}`}
    />

    <Accordion>
      {#snippet header()}
        {@html marked.parseInline(m.math_fal_reaction_rates())}
      {/snippet}
      <Text>{@html marked.parseInline(m.math_fal_rates_dynamic())}</Text>

      <Math
        display
        tex={String.raw`\begin{aligned}
v_{\mathrm{PSII}} &= k_2 \cdot 0.5 \cdot B_1 \\
v_\mathrm{Xcyc} &= k_\mathrm{DeepoxV} \cdot \frac{H^{nH_X}}{H^{nH_X} + pH_{\mathrm{inv}}(K_\mathrm{phSat})^{nH_X}} \cdot \mathrm{Vx} - k_\mathrm{EpoxZ} \cdot (\mathrm{X^{tot}} - \mathrm{Vx}) \\
Q &= \gamma_0 (1-\tfrac{Z}{Z+K_{ZSat}}) \mathrm{PsbS} + \gamma_1 (1-\tfrac{Z}{Z+K_{ZSat}}) \mathrm{PsbS^p} + \gamma_2 \tfrac{Z}{Z+K_{ZSat}} \mathrm{PsbS^p} + \gamma_3 \tfrac{Z}{Z+K_{ZSat}} \mathrm{PsbS}
\end{aligned}`}
      />
    </Accordion>

    <Accordion>
      {#snippet header()}
        {@html marked.parseInline(m.math_fal_model_code_expander())}
      {/snippet}
      <Text>
        {@html marked.parseInline(m.math_fal_construction_header())}
      </Text>
      <Text>{@html marked.parseInline(m.math_fal_construction_1())}</Text>
      <Code><Pre>{CODE.define}</Pre></Code>

      <Text>{@html marked.parseInline(m.math_fal_construction_2())}</Text>
      <details>
        <summary>Parameters</summary>
        <Code><Pre>{CODE.params}</Pre></Code>
      </details>
      <details>
        <summary>Compounds</summary>
        <Code><Pre>{CODE.comps}</Pre></Code>
      </details>

      <Text>{@html marked.parseInline(m.math_fal_construction_3())}</Text>
      <Code><Pre>{CODE.addCompsPars}</Pre></Code>

      <Text>{@html marked.parseInline(m.math_fal_simulation_header())}</Text>
      <Text>{@html marked.parseInline(m.math_fal_simulation_1())}</Text>
      <Code><Pre>{CODE.definesim}</Pre></Code>

      <Text>{@html marked.parseInline(m.math_fal_simulation_2())}</Text>
      <Code><Pre>{CODE.initialisesim}</Pre></Code>
    </Accordion>
  {/if}

  <!-- Implementation -->
  <H2>{@html marked.parseInline(m.fal_headline_implementation())}</H2>
  <Text>
    {@html marked.parseInline(
      ta(
        m.bio_fal_implementation_description(),
        m.math_fal_implementation_description(),
      ),
    )}
  </Text>
  {#if audienceStore.audience === "4bio"}
    <Text>{@html m.bio_fal_implementation_to_expert()}</Text>
  {/if}

  <!-- Analysis --------------------------------------- -->
  <H2>{@html marked.parseInline(m.fal_headline_analyse())}</H2>
  <Text>
    {@html marked.parseInline(
      ta(m.bio_fal_introduktion(), m.math_fal_introduktion()),
    )}
  </Text>

  <Text>{@html marked.parseInline(m.fal_headline_slider())}</Text>
  <Text>{@html marked.parseInline(m.fal_explanatnion())}</Text>

  <Accordion open={false}>
    {#snippet header()}
      {@html marked.parseInline(m.fal_graph_explanation_expander())}
    {/snippet}
    <Text>
      {@html marked.parseInline(m.fal_graph_explanation_header_single())}
    </Text>
    <Text>{@html marked.parseInline(m.fal_graph_explanation_1_intro())}</Text>
    <Ol>
      <Li>{@html marked.parseInline(m.fal_graph_explanation_1_phase1())}</Li>
      <Li>{@html marked.parseInline(m.fal_graph_explanation_1_phase2())}</Li>
      <Li>{@html marked.parseInline(m.fal_graph_explanation_1_phase3())}</Li>
    </Ol>
    <Math
      display={false}
      tex={"NPQ = \\dfrac{F_m - F_m'}{F_m'}"}
    />
    <Text>
      {@html ta(
        m.bio_fal_graph_explanation_2(),
        m.math_fal_graph_explanation_2(),
      )}
    </Text>
    <Text>
      {@html marked.parseInline(m.fal_graph_explanation_header_duo())}
    </Text>
    <Text>{@html marked.parseInline(m.fal_graph_explanation_duo())}</Text>
  </Accordion>

  <!-- Having trouble connecting -->
  <Accordion open={false}>
    {#snippet header()}
      {@html marked.parseInline(m.fal_guiding_expander())}
    {/snippet}
    <Text>{@html marked.parseInline(m.fal_guiding_header())}</Text>
    <label class="toggle-label">
      <input
        type="checkbox"
        bind:checked={showAnswers}
      />
      {@html marked.parseInline(m.fal_guiding_toggle())}
    </label>

    <Text>{@html marked.parseInline(m.fal_guiding_intro())}</Text>

    <!-- Q1 -->
    <Text
      ><Bold>1.</Bold>
      {@html marked.parseInline(m.fal_guiding_q1_prompt())}</Text
    >
    <Ul>
      {#if !showAnswers}
        <Li>{@html marked.parseInline(m.fal_guiding_q1_1())}</Li>
        <Li>{@html marked.parseInline(m.fal_guiding_q1_2())}</Li>
      {:else}
        <Li>{@html marked.parseInline(m.fal_guiding_a1_1())}</Li>
        <Li>{@html marked.parseInline(m.fal_guiding_a1_2())}</Li>
      {/if}
    </Ul>

    <!-- Q2 -->
    <Text
      ><Bold>2.</Bold>
      {@html marked.parseInline(m.fal_guiding_q2_prompt())}</Text
    >
    <Ul>
      {#if !showAnswers}
        <Li>{@html marked.parseInline(m.fal_guiding_q2_1())}</Li>
      {:else}
        <Li>{@html marked.parseInline(m.fal_guiding_a2_1())}</Li>
        <Li>{@html marked.parseInline(m.fal_guiding_a2_2())}</Li>
      {/if}
    </Ul>

    <!-- Q3 -->
    <Text
      ><Bold>3.</Bold>
      {@html marked.parseInline(m.fal_guiding_q3_prompt())}</Text
    >
    <Ul>
      {#if !showAnswers}
        <Li>{@html marked.parseInline(m.fal_guiding_q3_1())}</Li>
        <Li>{@html marked.parseInline(m.fal_guiding_q3_2())}</Li>
      {:else}
        <Li>{@html marked.parseInline(m.fal_guiding_a3_1())}</Li>
        <Li>{@html marked.parseInline(m.fal_guiding_a3_2())}</Li>
        <Li>{@html marked.parseInline(m.fal_guiding_a3_3())}</Li>
      {/if}
    </Ul>

    <!-- Q4 -->
    <Text
      ><Bold>4.</Bold>
      {@html marked.parseInline(m.fal_guiding_q4_prompt())}</Text
    >
    <Ul>
      {#if !showAnswers}
        <Li>{@html marked.parseInline(m.fal_guiding_q4_1())}</Li>
        <Li>{@html marked.parseInline(m.fal_guiding_q4_2())}</Li>
      {:else}
        <Li>{@html marked.parseInline(m.fal_guiding_a4_1())}</Li>
        <Li>{@html marked.parseInline(m.fal_guiding_a4_2())}</Li>
      {/if}
    </Ul>

    <!-- Q5-Q7: bio only -->
    {#if audienceStore.audience === "4bio"}
      <Text
        ><Bold>5.</Bold>
        {@html marked.parseInline(m.fal_guiding_q5_prompt())}</Text
      >
      <Ul>
        {#if !showAnswers}
          <Li>{@html marked.parseInline(m.fal_guiding_q5_1())}</Li>
          <Li>{@html marked.parseInline(m.fal_guiding_q5_2())}</Li>
        {:else}
          <Li>{@html marked.parseInline(m.fal_guiding_a5_1())}</Li>
          <Li>{@html marked.parseInline(m.fal_guiding_a5_2())}</Li>
          <Li>{@html marked.parseInline(m.fal_guiding_a5_3())}</Li>
          <Li>{@html marked.parseInline(m.fal_guiding_a5_4())}</Li>
        {/if}
      </Ul>

      <Text
        ><Bold>6.</Bold>
        {@html marked.parseInline(m.fal_guiding_q6_prompt())}</Text
      >
      <Ul>
        {#if !showAnswers}
          <Li>{@html marked.parseInline(m.fal_guiding_q6_1())}</Li>
        {:else}
          <Li>{@html marked.parseInline(m.fal_guiding_a6_1())}</Li>
        {/if}
      </Ul>

      <Text
        ><Bold>7.</Bold>
        {@html marked.parseInline(m.fal_guiding_q7_prompt())}</Text
      >
      <Ul>
        {#if !showAnswers}
          <Li>{@html marked.parseInline(m.fal_guiding_q7_1())}</Li>
          <Li>{@html marked.parseInline(m.fal_guiding_q7_2())}</Li>
          <Li>{@html marked.parseInline(m.fal_guiding_q7_3())}</Li>
        {:else}
          <Li>{@html marked.parseInline(m.fal_guiding_a7_1())}</Li>
          <Li>{@html marked.parseInline(m.fal_guiding_a7_2())}</Li>
        {/if}
      </Ul>
    {/if}
  </Accordion>

  <!-- Slider controls -------------------------------- -->

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
      {@html m.fal_slider_time()}: <strong>{totalMinutes} min</strong>
      <input
        type="range"
        min="1"
        max="15"
        step="1"
        bind:value={totalMinutes}
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

      <label class="slider-label">
        {@html m.fal_slider_darklength()}: <strong>{darkLength} s</strong>
        <input
          type="range"
          min="0"
          max={totalMinutes * 60}
          step="5"
          bind:value={darkLength}
        />
      </label>
      <label class="slider-label">
        {@html m.fal_slider_saturate()}:
        <strong>{saturatingPulse}</strong>
        <input
          type="range"
          min="0"
          max="10000"
          step="500"
          bind:value={saturatingPulse}
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
    prev={{ href: "/model", label: "Computational Models" }}
    next={{ href: "/plant-memory", label: "Plant Memory" }}
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
  .toggle-label {
    display: flex;
    align-items: center;
    gap: var(--space-2, 8px);
    cursor: pointer;
    margin: var(--space-2, 8px) 0;
  }

  details summary {
    cursor: pointer;
    padding: var(--space-2, 8px) 0;
    font-weight: 500;
  }

  .content-table-title {
    margin: var(--space-4, 16px) 0 var(--space-2, 8px);
    font-weight: 600;
    font-size: 1rem;
  }

  .content-table {
    margin-bottom: var(--space-4, 16px);
    border-collapse: collapse;
    width: 100%;
    font-size: 0.875rem;
  }

  .content-table th,
  .content-table td {
    vertical-align: top;
    border-bottom: 1px solid var(--color-border);
    padding: 0.4rem 0.75rem;
    text-align: left;
  }

  .content-table th {
    background: var(--color-surface);
    font-weight: 600;
    white-space: nowrap;
  }
</style>
